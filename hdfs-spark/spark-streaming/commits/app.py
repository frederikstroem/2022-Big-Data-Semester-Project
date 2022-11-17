from pyspark.sql import SparkSession
from pyspark.sql.functions import explode_outer, from_json, lit, max, struct, to_json, udf
from pyspark.sql.types import MapType, StringType
from datetime import date
import schemas

def get_html_url(value):
    index = rfind("/commit"/)
    return value[:index]

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

@udf
def get_date_category_udf(value):
    if value is not None:
        latest = date.fromisoformat("2013-08-10") # Latest date in data set
        if latest == value.date():
           return "latest"
    return "all time"

@udf
def get_html_url(value):
    # Discard everything after commit in html_url
    index = value.rfind("/commit/")
    return value[:index]


if __name__ == '__main__':
    APP_NAME = "repos-job"
    TOPIC = "msr14.repos_limit100k"
    HIST_TOPIC = TOPIC + ".historical"
    ANSWER_TOPIC = "answers"
    SCHEMA = schemas.commits_schema

    spark = create_spark_session(APP_NAME)
    df = subscribe_to_kafka_topic(spark, TOPIC)
    df = apply_schema(df, SCHEMA)

    # Query data.
    df = df.select(
        df.fullDocument.date.alias("date"),
        df.fullDocument.html_url.alias("html_url"),
        df.fullDocument.stats.total.alias("total"),
        df.fullDocument.stats.additions.alias("additions"),
        df.fullDocument.stats.deletions.alias("deletions")
    )

#df2.select("fullDocument.html_url", "fullDocument.commit.comitter.date", "fullDocument.stats.additions", "fullDocument.stats.deletions").show(1, False)
#df2.select("fullDocument.*").show()
#df3 = df2.select("fullDocument.html_url", "fullDocument.commit.committer.date", "fullDocument.stats.additions", "fullDocument.stats.deletions")
#df4 = df3.withColumn("formatted_url", get_html_url(df3.html_url))

    df2 = df1.withColumn(formatted_url, get_html_url(df3.html_url))

    # df2 = df.withColumn("tmp", lit("A")) \
    #         .withColumn("category", get_date_category_udf(df.pushed_at))
    # df2 = df2.groupBy(df2.tmp, df2.category).agg(
    #         max(struct("watchers_count", "full_name", "category")).alias("watchers"),
    #         max(struct("forks_count", "full_name", "category")).alias("forks"),
    #         max(struct("open_issues_count", "full_name", "category")).alias("open_issues"),
    #         max(struct("size", "full_name", "category")).alias("size")
    #     ).drop("tmp", "category")

    write_to_kafka_topic(df, HIST_TOPIC, "append")
    write_to_kafka_topic(df2, ANSWER_TOPIC, "complete")

    spark.streams.awaitAnyTermination()
    spark.stop()
