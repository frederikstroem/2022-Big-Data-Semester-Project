docker build -t spark-streaming-test .
docker run --rm -e ENABLE_INIT_DAEMON=false --net=host --name pyspark spark-streaming-test