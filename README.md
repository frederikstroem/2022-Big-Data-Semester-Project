# 2022-Big-Data-Semester-Project

<!--- These are examples. See https://shields.io for others or to customize this set of shields. You might want to include dependencies, project status and licence info here --->
![GitHub repo size](https://img.shields.io/github/repo-size/frederikstroem/2022-Big-Data-Semester-Project)
![GitHub contributors](https://img.shields.io/github/contributors/frederikstroem/2022-Big-Data-Semester-Project)

This project investigates and implements a `big data pipeline` integraded with a `speech interface` and is a mandatory part of the 1st semester of MSc in Software Engineering at ![SDU](https://www.sdu.dk/en/uddannelse/kandidat/softwareengineering). 

The data pipeline builds upon Apache Kafka, Spark, and Hadoop.


## Spinning up the data pipeline
Spin up the Kafka and Zookeeper instances on each node (replace `X` with node index):
```
docker compose -f kafka/nodeX.docker-compose.yaml up -d
```
Spin up Kafka Connect and Redpanda webui on Node1:
```
docker compose -f kafka/node1-connect.docker-compose.yaml up -d
```
Lastly, spin up HDFS and Spark
```
docker compose -f hdfs-spark/nodeX.docker-compose.yaml up -d
```

## Troubleshooting
Check if Kafka and Zookeeper are running on each node:
```
docker logs zk-X
docker logs kafka-X | grep started
```
Zookeeper instances will be running the logs contain `INFO Committing global session`

Check if HDFS instances are up and running (namenode runs on Node2):
```
docker logs datanode-X
docker logs namenode
```
The datanodes logs will contain `INFO datanode.DataNode: Got finalize command for block pool` if they spun up successfully.

Check if Spark is running through the master on Node1:
```
docker logs spark-master
```
Two entries corresponding to the the workers should be visible in the logs.
