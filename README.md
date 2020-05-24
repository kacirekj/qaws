# saws
Search AWS CloudWatch logs


NAME:
        saws.py -- Search AWS CloudWatch logs
    SYNOPSIS
        saws.py [-g groups...] \
                [-t starttime | starttime endtime] \
                [-q query]
                   
    DESCRIPTION
        -g --groups groups ...
            Specify 1 to N logging groups like "/ecs/someservice1"
        -t --time starttime | starttime endtime
            Specify starttime in history to more recent endtime in present.
            Possible formats for time specification is:
                ISO time:                           "2000-01-01T00:00:00"
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
                
        - It can take few minutes (~2 minutes) until logs appears in CloudWatch and therefore fetching logs 
            with '-t "1m"' may not return any results
        - Even if you set '|limit 1' in --query then CloudWatch will anyway search over entire specified '-t "10d"' 
            history which can take lot of time
    EXAMPLES
        saws.py \
            --groups      "/ecs/someservice0" "/ecs/someservice1" "/ecs/someserviceN" \
            --time        "1h" \
            --query       "fields @message | filter @message like 'event' | limit 15"
                    
