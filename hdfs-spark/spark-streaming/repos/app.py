from pyspark.sql import SparkSession
from pyspark.sql.functions import explode_outer, from_json, lit, max, struct, to_json, udf
from pyspark.sql.types import MapType, StringType
from datetime import date
import schemas

# Workaround of passing a function as parameter.
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

def count_language(df, epoch_id):
    df2 = df.groupBy(df.tmp, df.category, df.language) \
            .count() \
            .groupBy(df.category) \
            .agg(max(struct("count", "language", "category")).alias("language_count")) \
            .drop("category")
    df2.select(to_json(struct([df2[x] for x in df2.columns])).alias("value")).select("value") \
        .write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka-1:19092,kafka-2:29092,kafka-3:39092") \
        .option("topic", ANSWER_TOPIC) \
        .mode("append") \
        .save()


@udf
def get_date_category_udf(value):
    if value is not None:
        latest = date.fromisoformat("2013-08-10") # Latest day in data set
        if latest == value.date():
           return "latest"
    return "all time"

if __name__ == '__main__':
    APP_NAME = "repos-job"
    SOURCE_TOPIC = "msr14.repos_limit100k"
    HIST_TOPIC = SOURCE_TOPIC + ".historical"
    ANSWER_TOPIC = "answers"
    SCHEMA = schemas.repos_schema

    spark = create_spark_session(APP_NAME)
    df = subscribe_to_kafka_topic(spark, SOURCE_TOPIC)
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
        df.fullDocument.updated_at.alias("updated_at"),
        df.fullDocument.language.alias("language")
    )

    df2 = df.withColumn("tmp", lit("A")) \
            .withColumn("category", get_date_category_udf(df.pushed_at))
    df3 = df2.groupBy(df2.tmp, df2.category).agg(
            max(struct("watchers_count", "full_name", "category")).alias("watchers"),
            max(struct("forks_count", "full_name", "category")).alias("forks"),
            max(struct("open_issues_count", "full_name", "category")).alias("open_issues"),
            max(struct("size", "full_name", "category")).alias("size")
        ).drop("tmp", "category")

    write_to_kafka_topic(df, HIST_TOPIC, "append")
    write_to_kafka_topic(df3, ANSWER_TOPIC, "complete")

    # Using foreach_bach to execute multiple aggregations on dataframe.
    batch_write_to_kafka_topic(df2, count_language)

    spark.streams.awaitAnyTermination()
    spark.stop()