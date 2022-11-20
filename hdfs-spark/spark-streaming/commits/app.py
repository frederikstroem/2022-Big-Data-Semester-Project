from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import col, collect_list, desc, explode_outer, from_json, lit, max, rank, row_number, struct, sum, to_json, udf
from pyspark.sql.types import MapType, StringType
from datetime import date
import schemas

global ANSWER_TOPIC

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

def batch_write_to_kafka_topic(df, foreach_batch_function):
    df.writeStream \
        .outputMode("append") \
        .foreachBatch(foreach_batch_function) \
        .start()

def write_micro_batch_to_kafka_topic(df):
    df.select(to_json(struct([df[x] for x in df.columns])).alias("value")).select("value") \
        .write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka-1:19092,kafka-2:29092,kafka-3:39092") \
        .option("topic", ANSWER_TOPIC) \
        .mode("append") \
        .save()

def sum_stats(df, epoch_id):
    # Total
    df2 = partition_df(df, "total")
    write_micro_batch_to_kafka_topic(df2)

    # Additions
    df2 = partition_df(df, "additions")
    write_micro_batch_to_kafka_topic(df2)

    # Deletions
    df2 = partition_df(df, "deletions")
    write_micro_batch_to_kafka_topic(df2)

def partition_df(df, field):
    field2 = "sum({})".format(field)
    df2 = df.groupBy(df.category, df.repo) \
            .sum()
    w = Window.partitionBy("category").orderBy(desc(field2))
    df2 = df2.withColumn("placement", rank().over(w))
    df2 = df2.filter( \
        ((df2.placement <= 3) & (df2.category == "all time")) | \
            ((df2.placement == 1) & (df2.category == "latest")))   
    df2 = df2.select(
        df2.category, 
        df2.placement, 
        df2.repo, 
        col(field2).alias("sum")
    ) \
        .withColumn("type", lit(field))
    df2 = df2.groupBy(df2.category, df2.type) \
             .agg(collect_list(struct("placement", "repo", "sum")).alias("placements"))      
    return df2

@udf
def get_date_category_udf(value):
    if value is not None:
        latest = date.fromisoformat("2013-08-10") # Latest date in data set
        if latest == value.date():
           return "latest"
    return "all time"

@udf
def get_repo_udf(value):
    # Discard everything after commit in html_url
    index = value.rfind("/commit/")
    return value[19:index]


if __name__ == '__main__':
    APP_NAME = "commits-job"
    TOPIC = "msr14.commits_limit100k"
    HIST_TOPIC = TOPIC + ".historical"
    ANSWER_TOPIC = "answers"
    SCHEMA = schemas.commits_schema

    spark = create_spark_session(APP_NAME)
    df = subscribe_to_kafka_topic(spark, TOPIC)
    df = apply_schema(df, SCHEMA)

    # Query data.
    df = df.select(
        df.fullDocument.commit.committer.date.alias("commit_date"),
        df.fullDocument.html_url.alias("html_url"),
        df.fullDocument.stats.total.alias("total"),
        df.fullDocument.stats.additions.alias("additions"),
        df.fullDocument.stats.deletions.alias("deletions")
    ) \
        .withColumn("repo", get_repo_udf(df.html_url))

    df2 = df.withColumn("category", get_date_category_udf(df.commit_date))
    write_to_kafka_topic(df, HIST_TOPIC, "append")
    batch_write_to_kafka_topic(df2, sum_stats)

    spark.streams.awaitAnyTermination()
    spark.stop()