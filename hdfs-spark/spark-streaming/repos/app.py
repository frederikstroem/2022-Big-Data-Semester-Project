from pyspark.sql import SparkSession
from pyspark.sql.functions import explode_outer, from_json, lit, max, struct, to_json
from pyspark.sql.types import MapType, StringType
import schemas

def create_spark_session(app_name):
    spark = SparkSession.builder.appName(app_name) \
        .config("spark.master","spark://spark-master:17077") \
        .config("spark.executor.cores", 1) \
        .config("spark.cores.max", 2) \
        .config("spark.executor.memory", "2g") \
        .config("spark.sql.streaming.checkpointLocation","hdfs://namenode:9000/stream-checkpoint/") \
        .getOrCreate()
    return spark

def subscribe_to_kafka_topic(spark_session, topic):
    df = spark_session \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka-1:19092,kafka-2:29092,10.kafka-3:39092") \
        .option("startingOffsets", "earliest")\
        .option("subscribe", topic) \
        .load()
    return df

def apply_schema(df, schema):
    df1 = df.selectExpr("CAST(value AS STRING)")
    df2 = df1.select(explode_outer(from_json(df1.value,MapType(StringType(),StringType()))))
    df2 = df2.filter(df2.key == "payload").select(from_json(df2.value, schema).alias("payload")).select("payload.*")
    return df2

def write_to_kafka_topic(df, topic, mode):
    df.select(to_json(struct([df[x] for x in df.columns])).alias("value")).select("value") \
        .writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka-1:19092,kafka-2:29092,kafka-3:39092") \
        .option("topic", topic) \
        .outputMode(mode) \
        .start() \

if __name__ == '__main__':
    APP_NAME = "repos-job"
    TOPIC = "msr14.repos_limit100k"
    HIST_TOPIC = TOPIC + ".historical"
    ANSWER_TOPIC = "answers"
    SCHEMA = schemas.repos_schema
    DATE = "2013-07-30"

    spark = create_spark_session(APP_NAME)
    df = subscribe_to_kafka_topic(spark, TOPIC)
    df = apply_schema(df, SCHEMA)

    # Query data.
    df = df.select(
        df.fullDocument.id.alias("id"),
        df.fullDocument.full_name.alias("full_name"), 
        df.fullDocument.description.alias("description"), 
        df.fullDocument.size.alias("size"), 
        df.fullDocument.watchers_count.alias("watchers_count"), 
        df.fullDocument.forks_count.alias("forks_count"), 
        df.fullDocument.open_issues_count.alias("open_issues_count"), 
        df.fullDocument.pushed_at.alias("pushed_at"), 
        df.fullDocument.updated_at.alias("updated_at")
    )

    df2 = df.withColumn("tmp", lit("A"))
    df2 = df2.groupBy(df2.tmp).agg(
            max(struct("watchers_count", "full_name")).alias("watchers"),
            max(struct("forks_count", "full_name")).alias("forks"),
            max(struct("open_issues_count", "full_name")).alias("open_issues"),
            max(struct("size", "full_name")).alias("size")
        ).drop("tmp")

    write_to_kafka_topic(df, HIST_TOPIC, "append")
    write_to_kafka_topic(df2, ANSWER_TOPIC, "complete")


    spark.streams.awaitAnyTermination()
    spark.stop()
