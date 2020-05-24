import boto3
from datetime import datetime, timedelta
import time
import sys

help = '''
NAME
    qaws -- Query AWS CloudWatch logs
SYNOPSIS
    qaws    [-g groups...]
            [-t starttime | starttime endtime]
            [-q query]
            [-s recordseparator]
DESCRIPTION
    -g --groups groups ...
        Specify 1 to N logging groups like "/ecs/someservice1"
    -t --time starttime | starttime endtime
        Specify starttime in history to more recent endtime in present.
        Possible formats for time specification is:
            ISO time:           "2000-01-01T00:00:00"
            Epoch in seconds:   "1590314700"
            Time relative to Now:      
                "1h"                    1 hour ago
                "1h 60m"                2 hours ago
                "1h 60m 3600s"          3 hours ago
                "3600s 60m 1h"          3 hours ago as well (order doesn't matter)
                "3600s 3600s 3600s"     3 hours ago as well (items are repeatable)
                "1y 1mo 1w 1d 1h 1m 1s" is possible as well
    -g --query query
        Query exactly as it is usually written in AWS CloudWatch Insights in Web Console:
            fields @timestamp, @message 
            | filter @message like 'event' 
            | limit 10"
    -s --separator recordseparator
        Optional parameter. Records will be separated by recordseparator symbol.
        
    - It can take few minutes (~2 minutes) until logs appears in CloudWatch and therefore fetching logs 
        with '-t "1m"' may not return any results
    - Even if you set '|limit 1' in --query then CloudWatch will anyway search over entire specified e.g. '-t "10d"' 
        history which can take lot of time
EXAMPLES
    qaws
        --groups      "/ecs/myservice0"
        --time        "1h"
        --query       "fields @message"
    qaws
        --groups      "/ecs/myservice0" "/ecs/myservice1" "/ecs/myservice2"
        --time        "1h 30m"
        --query       "fields @message"
    qaws
        --groups      "/ecs/myservice0"
        --time        "5h" "1h"
        --query       "fields @timestamp @message | filter @message like 'event' | limit 15"
    qaws
        --groups      "/ecs/myservice0"
        --time        "2020-05-24T00:00:00" "2020-05-24T12:00:00"
        --query       "fields @message | filter @message like 'event'"
    qaws
        --groups      "/ecs/myservice0"
        --time        "1y" "2020-05-24T00:00:00"
        --query       "fields @message | filter @message like 'event'"
    qaws
        --groups      "/ecs/myservice0"
        --time        "2020-05-24T00:00:00" "5h"
        --query       "fields @message | filter @message like 'event' | limit 15"
AUTHORS
    Jiri Kacirek (kacirek.j@gmail.com) 2020
IMPLEMENTATION
    Python 3.8
'''

class TimeParser:

    def __init__(self, today=datetime.now()):
        self.today = today

    def parse(self, string: str, else_return=None) -> datetime:
        if not string:
            return else_return

        return self._parse_isodatetime(string) \
               or self._parse_relative_time(string) \
               or self._parse_timestamp(string) \
               or else_return \

    def _parse_timestamp(self, string: str) -> datetime:
        if string.isdigit():
            return datetime.fromtimestamp(float(string))

    def _parse_isodatetime(self, string: str):
        if all(char in string for char in ['-', ':']):
            return datetime.fromisoformat(string)

    def _parse_relative_time(self, string: str):
        if any(char in string for char in 'y mo w d h m s'):
            return self._get_datetime_from_relative(string)

    def _get_num_from_str(self, string: str):
        num = ''
        for ch in string:
            if ch.isdigit():
                num += ch
        return int(num)

    def _get_datetime_from_relative(self, relative: str):
        seconds = 0
        split = relative.split(' ')
        for s in split:
            if 'y' in s:
                seconds += self._get_num_from_str(s) * 3600 * 24 * 365
            elif 'mo' in s:
                seconds += self._get_num_from_str(s) * 3600 * 24 * 30
            elif 'w' in s:
                seconds += self._get_num_from_str(s) * 3600 * 24 * 7
            elif 'd' in s:
                seconds += self._get_num_from_str(s) * 3600 * 24
            elif 'h' in s:
                seconds += self._get_num_from_str(s) * 3600
            elif 'm' in s:
                seconds += self._get_num_from_str(s) * 60
            elif 's' in s:
                seconds += self._get_num_from_str(s)
            else:
                raise Exception(f"Can't parse {relative}")

        return self.today - timedelta(seconds=seconds)


def main(argv=None):

    argv = sys.argv
    if len(argv) < 7:
        print(help)
        exit()

    # Parse input arguments

    arg_groups_names = []
    arg_time = []
    arg_query = []
    arg_separator = []
    _switch_pointer = []

    for idx, item in enumerate(argv):
        if item in ['--groups', '-g']:
            _switch_pointer = arg_groups_names
            continue
        if item in ['--time', '-t']:
            _switch_pointer = arg_time
            continue
        if item in ['--query', '-q']:
            _switch_pointer = arg_query
            continue
        if item in ['--separator', '-s']:
            _switch_pointer = arg_separator
            continue

        _switch_pointer.append(item)


    # Parse time

    client = boto3.client('logs')

    timeparser = TimeParser()
    arg_time_start = arg_time[0]
    try:
        arg_time_end = arg_time[1]
    except:
        arg_time_end = None

    time_start = timeparser.parse(arg_time_start, else_return=timeparser.today)
    time_end = timeparser.parse(arg_time_end, else_return=timeparser.today)

    print(f'Search for logs from {time_start.isoformat()} to {time_end.isoformat()}.')

    # Execute AWS Query

    start_query_response = client.start_query(
        logGroupNames=arg_groups_names,
        startTime=int(time_start.timestamp()),
        endTime=int(time_end.timestamp()),
        queryString=arg_query[0],
    )

    query_id = start_query_response['queryId']

    # Wait for query result

    response = None

    while response == None or response['status'] == 'Running':
        print('Waiting for query to complete ...')
        time.sleep(3)
        response = client.get_query_results(
            queryId=query_id
        )

    # Print query result
    statistics = response["statistics"]
    print(f'Records matched {statistics["recordsMatched"]}, Records scanned: {statistics["recordsScanned"]}')

    for res in response['results']:
        line = []
        for r in res:
            if '@ptr' not in r['field']:
                line.append(r['value'].strip())

        line = ', '.join(line)
        if len(arg_separator) != 0:
            line = arg_separator[0] + line
        print(line)

    return 0


if __name__ == "__main__":
    main()
