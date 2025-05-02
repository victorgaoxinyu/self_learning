## Scalability & High Availability
- Vertical Scalability
  - increase size of instance
    - junior operator
    - senior operator
  - for non distributed system like DB
  - RDS, ElastiCache are services that can scale vertically
  - usually a hardware limit
- Horizontal Scalability
  - increase number of instances/system
    - 1 operator
    - 6 operator
  - implies distributed systems
  - common web applications
- High Availability
  - linked with horizontal scalability but not the same
  - run apply in at least 2 data centers (Availability Zones)
  - goal is to survive a data center loss
  - Auto Scaling Group with Multi AZ
  - Load Balancer with Multi AZ

## ELB: Elastic Load Balancing
- load balancers are servers that forward traffic to multipel servers downstream

### why LB
- spread load
- expose a single point of access DNS to application
- handle failures of downstream instances
- do regular health check to instances
- provide SSL termination HTTPS 
- enforce stickiness with cookies
- high availability
- seperate public traffic from private traffic

### why ELB
- ELB is a managed load balancer
  - AWS take care of most things
  - only a few config needed
  - integrated into other aws services

### Health Checks
- endpoint: /health
- if not return 200 then do not send traffic to instance

### Types
- CLB: Classic
- ALB: Application
  - HTTP, HTTPS
- NLB: Network
  - TCP, UDP, TLS
    - ultra high performance
- GWLB: Gateway
  - operates at layer 3 (network layer) IP protocol
  - for security, firewall.

Some load balancers can be setup as internal or external ELBs

### Security Group
```
User --> HTTPS/HTTP from anywhere -->  Load Balancer --> HTTP Restricted to Load balancer --> EC2
```
EC2 Security Group: Allow traffic only from Load Balancer

### ELB: ALB, Application Load Balancer
- Layer 7, HTTP
- load balancing to multiple http applications across machines (target group)
- load balancing to mutliple apps on the same machine, contianers
- support http/2 and websocket
- support redirects, http -> https
- routing tables to different target groups
  - based on path in URL
    - example.com/users & example.com/post
  - based on hostname
  - based on Query String, Headers
    - example.com/endpoint?platform=mobile --> target group 1
    - example.com/endpoint?platform=desktop --? target group 2
- Great for micro services and container based apps

#### Target Groups
- EC2 instances - HTTP
- ECS tasks - HTTP
- lambda functions - HTTP req translated into JSON event
- IP Address - must be private IPs

ALB can route to multiple target groups
Health checks are at target group level


```
Client IP <---> Load Balancer IP <---> EC2 Instance
```
If EC2 instance wish to see true clientIP, Port, Proto, they are all in the header

#### Advanced topic
security
  - only allow traffic from load balancer
  - edit the inbound rules

### ELB: NLB, Network Load Balancer
- Layer 4, TCP, UDP
- extreme performance
- one static IP per AZ, and supports assigning Elastic IP

#### Target Groups
- EC2 instances
- IP Addresses - must be private IPs
- Application Load Balancer
  - put NLB in front of ALB
- Health checks support the TCP, HTTP and HTTPS Protocols

### ELB: GLB, Gateway Load Balancer
- Layer 3, Network Layer, IP Packets
- Deploy, scale and manage a fleet of 3rd party network virtual appliances in AWS
- firewalls, intrusion detection and prevention systems...
- functions
  - transparent network gateway
    - single entry/exit for all traffic
  - load balancer
    - distributes traffic
- use GENEVE protocol on port 6081
```
User --> GLB --> Target Group --> GLB --> Application
                    ^
                    |
                    3rd party security appliances
```
#### Target Groups
- EC2 instances
- IP addresses - must be private IP

### Sticky sessions
- same client is always redirected to the same instnce behind load balancer
- works for classic, ALB and NLB
- use cookie
- may bring imbalance to the group

Cookie
- Application-based Cookies
- Duration-based Cookies

### Cross Zone Load Balancing
- enable: distributes evenly across all instances in all AZ
- disable: distributed in the instances of the node of ELB
  - 2 AZ, then each get 50%, regardless of how many instances we got in each AZ

ALB:
- enabled by default
- no charge for inter AZ data transfer

NLB and GLB
- disabled by default
- charge for inter AZ

## SSL/TLS
- in-flight encryption, allow traffic between clients and load balancer to be encrypted in transit
- SSL: Secure Sockets Layer
- TLS: Transport Layer Security, a newer version of SSL
  - TLS are mainly used now, but refer as SSL

### Load Balancer - SSL
```
Users --> HTTPS --> Load Balancer --> HTTP over Pricate VPC --> EC2
```
- Use X.509 Cert
- Manage cert using ACM, AWS Certificate Manager
- Upload own cert
- HTTPS listner:
  - default cert
  - add optional list
  - Client can use SNI (Server Name Indication) to specify the hostname they reach.

### SNI
- loading multiple SSL certs onto one web server, to server multiple websites.
- requires the client to indicate hostname of target server in inital SSL handshake
- server will then find the correct cert, or return default
- ALB & NLB only
    - CLB: should use multiple CLB for multiple hostname with multiple SSL certs

## Connection Draining
- Connection Draining - for CLB
- Deregistration Delay - for ALB & NLB

- Time to complete in-flight requests while instance is de-registering or unhealthy
- stop sending new requests to EC2 which is de-registering
- can be disabled, or set period.
  - set to a low value if requests are short
  - set to high if requests are long like file upload etc
    - EC2 will turned off once period is done

## Auto Scaling Group
- scale out and in to match increase/decrease load
- set min and max number of running ec2
- register new instance to load balancer
- re-create ec2 is one is unhealthy

