# Observability
<div style="text-align: center;"><img src="../images/observability.png" alt="three-tier design" width="800 " height="450" style="border-radius: 15px;"></div>  

# CloudWatch
- Collection of monitoring tools:  ***Logs, Metrics, Events, Alarms, Dashboards***
<div style="text-align: center;"><img src="../images/CloudWatch.png" alt="three-tier design" width="850 " height="350" style="border-radius: 15px;"></div>


## **Metrics**
- It's the watch of a values/variables over points of time for specific resource. ex: CPUUtilization
- `Metric Intervals`: How often metrics will be sent to you
- `Metric Resolution`: How often metrics will be collected from target
- ***Ex:*** Basic Monitoring(5m) with High Resolution(1s)
    - collect metrics every second but send all collected every 5m
- not all ec2 metrics are tracked without an agent (need to install cloudwatch agent on Ec2)
- Each metric has a namespace that fall into.


## **Alarm**:
- It's used to trigger an action based on  
- alarm state trigger 
    - INSUFFICIENT **->** no enough data is available. 
    - OK **->** metric is within the defined threshold.
    - IN ALARM **->** metric is outside of the defined threshold.
- threshold 
    - threshold types **->** `Static & Anomaly`
    - Condition **->** (Greater, Greater/Equal, Lower/Equal, Lower)
- Action (Notifications, ASG, EC2 Actions, Lambda)

## **Logs**
- The actual Text logs produced by application (Access Logs, App Logs, Execution Logs)
- Mainly used for Centralized Logging: Logs, Logs Groups, Log Streams
    - Log Group as a Folder 
    - Log Stream as a File 
    - Log Events (logs) as Text lines
- **Turn logs → metrics** `==` **Metrics Filter**
    - A Metric Filter watches your logs and turns matching lines into numbers.
    - How many times did this text appear in my logs?
    - use it with alarms 

- Collect Logs Automatically -> ✅ CloudWatch Agent 
- Custom application sends logs directly -> ✅PutLogEvents API / SDK (boto3)
- logs has to be in order then we should use:
    - **DescribeLogStreams API**: to know the last log sequence tokens and the existence of the log stream
    - **PutLogEvents API**: Send logs api

| Code Part            | AWS Concept       |
| -------------------- | ----------------- |
| describe_log_streams | Read stream state |
| uploadSequenceToken  | Enforce ordering  |
| put_log_events       | Send logs         |
| logGroupName         | Container         |
| logStreamName        | Source            |
| logEvents            | Actual logs       |

---


<div style="text-align: center;"><img src="../images/eventbridge.png" alt="three-tier design" width="800" height="450" style="border-radius: 15px;"></div>

## **EventsBridge**:
- Event
- Producer
- Event Bus (Place that contain events)
- Rules (determine what events to deliver)
- Targets (the target consume events)
- common use case: (Trigger DB Backup everyday)

# CLoudTrail
- Monitor API calls and Actions
- we use it to identify:
    - who User, UserAgent
    - Where Source IP Address
    - When EventTime
    - What Region, resource

- It tracks:
    - Management Events (Default): login, configure IAM & etc.
    - Data Events: track specific events for aws service like S3 & Lambda
    - ***`Enable log file validation (detect tampering)`***

```txt
CloudTrail = the service
Event = “Someone did something” (e.g., DeleteBucket)
Trail = the rule that says:
“Record these events and store them here”
```