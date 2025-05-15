## Lambda
- functions, no server
- limtied by time, short executions
- on-demand
- auto scale

Benifits
- Easy Pricing
- high integrated
    - aws
    - languages
    - lambda container image
      - image must implement lambda runtime api
      - ecs/fargate is preferred for running arbitrary docker image

### Pricing
- Pay per calls
- Pay per duration
- very cheap

### Lambda - Limits - per region
- Execution
  - memory allocation 128MB - 10GB
  - max exec time, 15min
  - env var, 4KB
  - disk capacity, (/tmp) 512MB to 10G
  - concurrency exec, 1000+

- Deployment
  - compressed deployment size 50MB
  - uncompressed deployment, code + dep 250MB
  - use /tmp to load other files
  - env var, 4KB

### Concurrency and Throttling
- 1000
- reserved concurrency, aka limit
  - invocation over limit will trigger a `Throttle`
    - synchronous invocation -> return ThrottleError 429
    - asynchronous invocation -> retry and then go to DLQ
- need a higher limit, raise support ticket

Cold start
- new instance, init is large, this process can take some time
- first request served by new instance has higher latency than the rest

Provisioned Concurrency
- concurrency is allocated before function invoked
- cold start never happens and all invocations have low latency
- application auto scaling can manage concurrency

### Snap start
pre-initialised state
  - when publish a new version
  - lambda init your function
  - take a snapshot of memory and disk state of init function
  - snapshot is cached for low-latency access

### Edge function
- a code that you write and attach to CloudFront distributions
- close to users to minimise latency

CloudFront Functions & Lambda@Edge

### Sync Invocation
- result returned right away
- error handling on client side

### Integration with ALB
Expose lambda function as HTTP(s) endpoint
- use ALB or API Gateway

ALB to Lambda, HTTP to JSON
- Query string param as k,v pairs
- header as k,v pairs
- body
- isBase64encoded

JSON to HTTP
- Header as k,v pairs
- body
- isBase64Encoded

ALB Multi-Value Headers
- http://example.com/path?name=foo&name=bar
- JSON:
  - "queryStringParamters": {"name": ["foo", "bar"]}
  - array

### Async Invocation
S3, SNS, CoutWatch Events, EventBridge
- events are placed in an Event Queue
- lambda retry 3 times, 1 min, 2min
- make sure process is idempotent
  - retry wont change result
- if is retried, will see duplicated logs
- can define a DLQ (dead letter queue) SNS or SQS, for failed processing
  - need correct IAM

### CloudWatch Events / EventBridge
CRON or Rate EventBridge Rule -> trigger every 1 hr
CodePipeline EventBridge Rule -> trigger on state changes

### S3 Event Notifications
s3 connect to:
- SNS -> fan out -> SQS queues
- SQS -> lambda
- lambda (async)
  - DLQ

s3 -> new file event -> lambda: update metadata table -> Table in RDS
                                                      -> DynamoDB Table

### Event Source Mapping
- Kineis Data Streams
- SQS & SQS FIFO queue
- DynamoDB Streams

#### Streams and Queues
#####  Streams, Kinesis & DynamoDB
- event source mapping creates iterator for each shard
- start with new items, from beginning or from ts
- processed items are not removed
- low traffic: use batch window to accumate records before processing
- process multiple batches in parallel
  - 10 batches per shard
  - in-order processing

Error handling
- By default, if function returns an error, the entire batch is reprocessed until function succeeds, or the items in the batch expire
- to ensure in-order, processing for affeted shard is paused until error is resolved

##### Queues, SQS and SQS FIFO
- SQS:
  - Long polling
  - batch size 1-10 msg
  - timeout to 6x
  - DLQ
    - set up on SQS queue, not lambda
    - or use lambda destination for failures

### Event Source Mapping Scaling
- Kinesis Data Streams & Dynamo DB Streams
  - one lambda invocation per stream shard
  - parallelisation, up to 10 batches per shard
- SQS Standard
  - lambda adds 60 more instances per min
  - up to 1000
- SQS FIFO
  - msg with same groupid will be processed in order
  - scales to number of active msg groups

### Lambda Event and Context Object
- Event Object
  - JSON formated doc
  - contains data for function to process
  - contains info from invoking service
- Context Object
  - provide methods and properties about the invocation

### Lambda Destinations
- Async
  - define destination for successful and failed event
    - SQS, SNS, Lambda, EventBridgeBus

### Lambda IAM Role
resource based policies

### Lambda Logging and Monitoring
- IAM policy to write to CloudWatch

### Lambda Tracing with X-Ray
- enable, Active Tracing
- X-Ray daemon
- use X-Ray SDK in code
- ensure right IAM role
  - AWSXRayDaemonWriteAccess
- env var to communicate with X-Ray
  - _X_AMZN_TRACE_ID: tracing header
  - AWS_XRAY_CONTEXT_MISSING: log error
  - AWS_XRAY_DAEMON_ADDRESS: Daemon IP:Port

### Lambda in VPC
- by default lambda function is launched **outside** your own VPC (in AWS owned VPC)
- it cannot access resources in your VPC

to make it work
- define VPC ID, subnets and security groups
- lambda will create ENI Elastic Network Interface in your subnet
- AWSLambdaVPCAccessExecutionRole

by default lambda in your VPC
- does not have internet
- deploying a lambda function in a **public** subnet does not give it internet access or public IP
- deploying lambda function in a **private** subnet gives it internet access if you have a NAT Gateway/instance


### Lambda function config
RAM
- the more RAM you get, more vCPU you get
- at 1792, one full vVPU
- after 1792, get more than 1, but need multi-threading
- if application is cpu-bound, increase RAM

timeout
- 3 sec, max to 15min

### LAmbda Execution context
- execution context is a temp runtime env, init any external dep
- next function invocation can `re-use` context
- include `/tmp` dir
  - need big file to work
  - need diskspace to perform operations
  - max 10G
  - for perm store, use 3
  - for encrypt, use KMS Data Keys

### Layers
- custom runtimes
  - cpp
  - rust
- externalize dep to re-use

### Lambda FS mounting
- can access EFS if running in a VPC
- config lambda to mount EFS to local dir during init
- must leverage EFS Access Point
- cconnection limit, and connection burst limit

### Lambda Function Dependencies
- install the package alongside your code and zip it
- upload zip to lambda if less 50MB, otherwie S3

### Lambda and CloudFormation
- inline: for simple function
- through s3: 
  - store zip in s3
  - refer s3 location in CloudFormation code
    - s3bucket
    - s3key
    - s3objectversion

Through s3 multiple accounts
account 1: with code
    - allow get & list to s3 bucket from account2&3
    - allow pricipal: account id
account2&3: cloudformation with execution role

### Lambda Container Images
- Base Image must implement the lambda runtime API
- Strat
  - Use aws provided base image
  - use multi stage builds
  - build from stable to freq changing
  - use single repo for functions with large layers
- use docker image to upload large lambda functions, up to 10G

### Lambda Versions
versions
- $LATEST - mutable
- v1, after publish - immutable

alias
- pointer to lambda func versions
- dev, test, prod etc.
- alias a mutable
- alias cannot reference aliases
- enable canary deployment by assigning weights, 
  - 95% to v1
  - 5% to v2
