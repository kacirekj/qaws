# qaws - Query AWS Logs
Command line utility for search in AWS CloudWatch Logs with Insights queries and flexible time ranges.

1. Install latest via pip: https://pypi.org/project/qaws.
2. Execute "qaws" in your command line.

## Status

### Versions
- Version 0.3 is stable, used by me on daily bases

### Improvement proposals
1. qaws should be able to list all groups in AWS
2. qaws should be able to take group list as stdin parameter
3. qaws could totaly neglect switchers like '-g', because each group starts with "/" and each query contains "fiELDs"
4. So the result could be: 'qaws --groups | qaws "1y" "6mo" "fields @message"'

```
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
```
