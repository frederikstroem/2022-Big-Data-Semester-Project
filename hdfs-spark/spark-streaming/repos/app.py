from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import col, collect_list, desc, explode_outer, from_json, lit, max, rank, row_number, struct, to_json, udf
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

def count_language(df, epoch_id):
    df2 = df.groupBy(df.category, df.language) \
            .count()
    w = Window.partitionBy("category").orderBy(desc("count"))
    df2 = df2.withColumn("placement", row_number().over(w))
    df2 = df2.filter( \
        ((df2.placement <= 3) & (df2.category == "all time")) | \
            ((df2.placement == 1) & (df2.category == "latest")))
    df2 = df2.groupBy(df2.category) \
            .agg(collect_list(struct("placement", "language", "count")).alias("placements")) \
            .withColumn("type", lit("languages_count"))  
    write_micro_batch_to_kafka_topic(df2)

def top3_counts(df, epoch_id):
    # Watchers count
    df2 = partition_df(df, "watchers_count")
    write_micro_batch_to_kafka_topic(df2)

    # Forks count
    df2 = partition_df(df, "forks_count")
    write_micro_batch_to_kafka_topic(df2)

    # Open issues
    df2 = partition_df(df, "open_issues_count")
    write_micro_batch_to_kafka_topic(df2)

    # Size
    df2 = partition_df(df, "size")
    write_micro_batch_to_kafka_topic(df2)

def partition_df(df, field):
    w = Window.partitionBy("category").orderBy(desc(field))
    df2 = df.withColumn("placement", rank().over(w))
    df2 = df2.filter( \
        ((df2.placement <= 3) & (df2.category == "all time")) | \
            ((df2.placement == 1) & (df2.category == "latest")))   
    df2 = df2.select(
        df2.category, 
        df2.placement, 
        df2.full_name, 
        col(field).alias("count")
    ) \
        .withColumn("type", lit(field))
    df2 = df2.groupBy(df2.category, df2.type) \
             .agg(collect_list(struct("placement", "full_name", "count")).alias("placements"))      
    return df2

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

    df2 = df.withColumn("category", get_date_category_udf(df.pushed_at))

    batch_write_to_kafka_topic(df2, top3_counts)
    batch_write_to_kafka_topic(df2, count_language)

    spark.streams.awaitAnyTermination()
    spark.stop()