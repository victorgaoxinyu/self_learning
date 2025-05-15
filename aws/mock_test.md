### Lambda
#### non-proxy / custom integration

Client -> Method request -> integration request -> Lambda function
Client <- Method response <- integration response <- Lambda function

#### Layer
A layer is a ZIP archive that contains libraries, a custom runtime, or other dependencies. With layers, you can use libraries in your function without needing to include them in your deployment package.

#### 504
INTEGRATION_FAILURE is aws lambda integration does not work
INTEGRATION_TIMEOUT timeout at 29sec

#### Internet connection
- attach it only to private subnets with Internet access through a NAT instance or add a NAT gateway to your VPC.
- also ensure that the associated security group of the Lambda function allows outbound connections

### CloudFormation

#### StackSets
- create, update, delete stacks across multiple accounts and regions with a single operation.


#### Helper
- cfn-init
  - retrieve and interpret resource metadata, install pokgs, create files, and start services
- cfn-signal
  - sync other resources in stack
- cfn-get-metadata
  - get metadata
- cfn-hup
  - check for updates and exec custom hooks


Transform
- The Transform section specifies the version of the AWS Serverless Application Model (AWS SAM) to use.

Parameters
- part of template that contains values to pass

Resources
- specify stack resources and properties

Mappings
- k, v pairs for conditional parameter values, similar to lookup table


### SAM CLI
- sam init
- sam publish: publish app to aws serverless application repo
- sam sync: syncing of local changes to AWS, for rapid development
- sam build: resolve dependencies and construct deployment artifacts
- sam deploy: deploy application with specified CloudFormation stack
  - zip code, upload to s3, and produce packaged AWS SAM template file

### DynamoDB
- in DynamoDB Streams, data older than 24 hours is susceptible to trimming (removal) at any moment.

### Amazon Kinesis Data Streams
You split shards to increase the capacity (and cost) of your stream. You merge shards to reduce the cost (and capacity) of your stream.

### AWS X-Ray
#### AWS X-Ray SDK
- does not send trace data direcly to AWS X-Ray. To avoid calling service every time your app serves a request, SDK sends trace data to daemon.
- install X-Ray daemon by using a user data script, this will install and run daemon automatically when you launch instance


#### API
- `GetTraceSummaries`: generate queryable trace summaries
  - get the list of trace IDs of the application
- `BatchGetTraces`: full traces
  - retrieve the list of traces


#### Environment variables
AWS Lambda uses environment variables to facilitate communication with the X-Ray daemon and configure the X-Ray SDK.

- `_X_AMZN_TRACE_ID`: tracing header which includes
  - sampling decision
  - trace ID
  - parent segment ID

- `AWS_XRAY_CONTEXT_MISSING`: X-Ray SDK uses this var to determine its behaviour in the event that your function tries to record X-Ray data, but tracing header is not available. Lambda sets this to `LOG_ERROR`
- `AWS_XRAY_DAEMON_ADDRESS`: 
  - exposes X-Ray daemon's address in `IP_ADDRESS:PORT` format. 
  - can use this address to send trace data to X-Ray daemon directly without using SDK


#### X-Ray daemon
- software application listens for traffic on UDP port 2000

Annotations:
- simple k, v pairs
- indexed for use with `filter expression`
- Use annotations to record data that you want to use to group traces in the console or when calling the GetTraceSummaries API. X-Ray indexes up to 50 annotations per trace

Metadata:
- k, v pairs with values of any type, including objects and lists
- not indexed
- use metadata to record data to store but dont need for searching

Trace Segment
- records information about the original request
- information about work that app does locally.

Trace Subsegment
- information about downstream calls that app make to AWS recources
- optional fields
  - `namespace`: `aws` for AWS SDK calls, `remote` for other downstream calls
  - `http`: http object with info about outgoing HTTP call
  - `aws`: aws object with info about downstream AWS resource
  - `error, throttle, fault, cause` 
  - `annotation`
  - `metadata`
  - `subsegments`: array of subsegment objs
  - `precursor_ids`
#### filter out from trace
- Use filter expressions in console
- using GetTraceSummaries API retrieves IDs and annotations for traces available

### Elastic Beanstalk

#### Deployment
- update env platform version
  - update to latest platform version
  - no change in runtime
- blue/green deployment
  - change in runtime

Types
- all at once
  - all instances simultaneously
  - use least time
- rolling
  - reduce env capacity by number of instance in batch
- rolling with additional batch
  - add new batch before take out existing for deploy
- immutable
  - deploy to a fresh group of instances

Dockerrun.aws.json
- multi-antainer Docker env

env.yaml
- config env name, solution stack

appspec.yml
- manage each app deployment as a series of lifecycle

cron.yam
- define periodic tasks

### CORS Cross-origin resource sharing
AllowedOrigin: Specifies domain origins that you allow to make cross-domain requests.
AllowedMethod: type of request you allow (GET, PUT, POST, DELETE, HEAD)
AllowedHeader: headers allowed in preflight request
MaxAgeSeconds: amount of time in secs that browser caches Amazon s3 response to preflight OPTIONS request
ExposeHeader: identifies response headers


### RDS
#### Enhanced Monitoring
- Enhanced Monitoring gathers its metrics from an agent on the instance.
    - percentage of CPU bandwidth and total memory consumed by each db process
- CloudWatch Monitoring gathers metrics about CPU utilization from hypervisor for a DB instance.

### CloudWatch
- namespace:
  - a container for CloudWatch metrics
  - metrics in different namespaces are isolated from each other
- alarm:
  - watches a single metric
- event:
  - deliver a near real-time stream of system events
- dimentions
  - only a name/value pair that is part of a metric


#### Metrics
- IntegrationLatency: responsiveness of the backend
- Latency: overall responsiveness of API calls
- CacheHitCount and CaheMissCount: cache capacities for desired performance

### CodeDeploy
- in-place
- canary
  - lambda/ECS
  - shifted in two increments
- linear
  - lambda/ECS
  - equal increments with equal number of min between each increment
- all-at-once
  - lambda/ECS
  - all traffic shifted from original to new

#### Lifecycle
- BeforeAllowTraffic
  - run tasks before traffic is shifted
- AfterAllowtraffic
  - run tasks after

### Task placement strategy
- binpack
  - least available amount of CPU or memory
- random
- spread
  - evenly based on specified value


AWS CloudFormation
  - cannot locally build, test, and debug
AWS Serverless Application Model (AWS SAM)
  - can locally ^
AWS Elastic Beanstalk
  - not for serverless application

### RCU
eventually consistency
    - / 4KB
strongly consistent
    - / 8KB

### DynamoDB
- Global secondary index
  - index with partition key and sort key can diff from base table
- Local secondary index
  - index with same partition key but diff sort key from base table

### S3
- CloudFront
  - serve static content
- Amazon s3 Transfer Acceleration
  - transfer accelerator

Multi part upload
- begin upload before know the final size
- pause and resume
- quick recover
- upload in parallel

### ECS
- Service scheduler: long running stateless application
- Container Agent: allow container instances connect to your cluster
- Task Definition
  - config port mapping

### Sync
- AppSync
  - sync app data cross platform
  - multiple user sync and collab in RT on shared Data
- Cognito Sync
  - not multiple user