# RDS
- Relational Database Service
- Create DB in cloud managed by AWS
  - Postgres

### Advantage and disadvantage
- Auto provisioning, OS patching
- backup and restore
- monitoring
- read replicas for read performance
- multi AZ for DR (Disaster Recovery)
- Maintenance windows for upgrades
- Scaling
- Storage backed by EBS

Dis
- Cannot SSH into instance

### RDS - Storage Auto Scaling
- set Max storage threshold
- auto modify storage if
  - free storage less than 10%
  - low storage last 5+ mins
  - 6hrs have passed since last modification
- useful for apps with unpredicable workloads

### RDS - Read Replicas for read scalability
- up to 15 read replicas
- within AZ, cross AZ, Cross Region
- Replication is ASYNC
- Replicas can be promoted to their own DB

### RDS - Network Cost
- RDS Read Replicas within the same region, free
- Cross Region will incur data transfer fee

### RDS - Multi AZ Disaster Recovery
- SYNC replication from Master DB to standby DB
- one DNS name - auto app failover to standby
- increase availability
- Failover in case of loss of AZ, loss of nextwork, instance or storage failure.
- Not used for scaling
- Read Replica can also be setup as Multi AZ DR

### RDS - From single AZ to multi AZ
- Zero downtime operation
- just click `modify`
  - a snapshot of Master DB is taken
  - a new DB is restored from the snapshot in a new AZ
  - Sync is established between two DB

## Amazon Aurora
- Prop tech for aws, not open source
- Postgres and MySQL are both supported
- AWS cloud optimized
- storage auto grows up to 128TB
- up to 15 replicas and faster replication, sub 10ms lag
- High availablility native
- cost more than RDS, 20%

## Aurora - High Availability and Read Scaling
- 6 copies of your data across 3 AZ
  - 4/6 needed for writes
  - 3/6 need for reads
  - self healing with p2p replication
  - storage striped across 100s of volumes
- One Aurora instance takes writes (master)
  - auto failover for master in less 30 sec
- Master + up to 15 read replicas
- Support Cross Region Replication

```
Client ----------------------------- Reader Endpoint
    \                              points to all read replicas
     \                              Connection load balanced
Writer Endpoint                               |
pointing to the master                        |
       \                                      |
        \                                     |
         \                                    |
       Master                          <Read replicas>  Auto Scaling
```

## RDS & Aurora Security
- At-rest encryption
  - master and replicas encryption using AWS KMS
    - defined at launch time
  - if master not encrypted, read replicas cannot be encrypted
  - to encrypt an un-encrypted db
    - db snapshot & restore as encrypted
- In-flight encryption
  - TLS-ready by default, use the AWS TLS root cert client side
- IAM auth
- Security Groups
  - control network access
- No SSH except on RDS custom
- Audit logs can be enabled and send to CloudWatch

## RDS Proxy
- Why?
  - pool and share DB connections established with the DB
- improve db efficiency by reduce stress on db resource and minimise open connections.
- Serverless, autoscaling, high available
- reduce failover time by 66%
- support
  - MySQL
  - PostgreSQL
  - MariaDB
  - MSSQL
  - Aurora
    - MySQL
    - PostgreSQL
- enforce IAM auth for DB

## ElastiCache
- managed Redis or Memcached
- in-memory db with high performance, low latency
- reduce load off db for read intensive workloads
- help make app stateless
- involves **heavy application code change**

### Solution architecture
- app queries ElasticCache first
  - if not available, get from RDS, and store in ElastiCache
- Cache must have invalidation strategy to make sur only the most current data is used.

### User Session store
```
User --> app --> write session --> Amazon ElastiCache

User --> app < -- retrieve session <-- Amazon ElastiCache
```

### ElastiCache - Redis vs Memcached
Redis
- Multi AZ
- Read Replicas
- Backup and restore
- Supports Sets and Sorted Sets

Memcached
- Multinode for partitioning of data (sharding)
- No replica
- Non presistent
- Backup and restore (serverless)
- Multi-thread arch
  - better performance?

### ElasticCache - Strategy
- is it safe? might be out of date
- is it effective?
  - pattern: data change slowly, few keys are freq needed
  - anti-pattern: data changing rapidly, all large key space needed
- is data structured well for caching?
  - kv pair is good

#### Strat 1: Lazy Loading / Cache-Aside / Lazy Population
- try ElasticCache first,
  - if Cache hit, get value
  - else Cache miss
    - read from DB
    - write to Cache
- Cons:
  - Cache miss penalty results in 3 round trips, delay
  - Stale data, data can be updated in db but outdated in cache


#### Strat 2: Write through
- add or update cache when db is updated
- Pros:
  - data in cache never stale, reads are quick
  - write penalty vs read penalty, each write requires 2 calls.
    - user care about read penalty more so this is good
- Cons:
  - Missing data until it is added/updated in the db
    - usually combined with lazy loading
  - cache churn, a lot of data in cache will never be read

### Cache Evications and Time to live, TTL
- evication
  - delete item explicitly in cache
  - memory is full, and it is not recently used.
  - time-to-live
    - secs -> days

### Amazon MemoryDB for Redis
- Redis compatible, durable, inmemory db service
- fast
- multi AZ
- scalable