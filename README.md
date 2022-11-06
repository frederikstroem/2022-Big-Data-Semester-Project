# 2022-Big-Data-Semester-Project


# Setup
There are two folders which contain a subset of the docker compose services for each node
- kafka
- hdfs-spark

### Starting Kafka and Zookeeper services
`cd kafka`

Start the docker compose services on each node. Remember to replace `X` with the node index
`docker-compose -f nodeX.docker-compose.yaml up -d`

`docker logs zk-X`
Zookeeper is up and running if it prints `...INFO Committing global session..."`
Kafka is up and running if `docker logs kafka-X | grep started` returns a string

Deploy connect to node1
`docker-compose -f node1-connect.docker-compose.yaml up -d`

### Starting HDFS and Spark
`cd hdfs-spark`

Start the docker compose services on each node. Remember to replace `X` with the node index
`docker-compose -f nodeX.docker-compose.yaml up -d`

Data nodes are running if the logs print the following ` INFO datanode.DataNode: Got finalize command for block pool...`
The Spark master will show two registered workers