from pyspark.sql import SparkSession
from pyspark.sql.functions import collect_set, explode_outer, from_json, udf
from pyspark.sql.types import MapType, StringType
import locale

locale.getdefaultlocale()
locale.getpreferredencoding()

@udf
def clean_udf(value):
    value = value.replace("\"payload\": \"{", "\"payload\": {", 1)
    index = value.rfind("\"")
    return value[:index] + value[index + 1:]

@udf
def to_string_udf(key, value):
    return  "\"{}\": \"{}\"".format(key, value)

@udf
def to_json_udf(value):
    temp = ", ".join(map(str, reversed(value)))
    return "{ \"type\": \"repo\", " + temp + " }"

def create_spark_session():
    spark = SparkSession.builder.appName("initialTest") \
        .config("spark.master","spark://spark-master:17077") \
        .config("spark.executor.cores", 1) \
        .config("spark.cores.max", 2) \
        .config("spark.executor.memory", "2g") \
        .config("spark.sql.streaming.checkpointLocation","hdfs://namenode:9000/stream-checkpoint/") \
        .getOrCreate()
    return spark

def read_from_kafka_topic(spark_session, topic):
    df = spark_session \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka-1:19092,kafka-2:29092,10.kafka-3:39092") \
        .option("startingOffsets", "earliest")\
        .option("subscribe", topic) \
        .load()
    return df

def split_data(df, date):
    df1 = df.selectExpr("CAST(value AS STRING)")
    df2 = df1.select(explode_outer(from_json(df1.value,MapType(StringType(),StringType()))))
    df2 = df2.select(df2.key.alias("key1"), df2.value.alias("value1"), explode_outer(from_json(df2.value,MapType(StringType(),StringType()))))
    df2 = df2.filter(df2.key1 == "payload")
    df2 = df2.select(df2.value1.alias("id"), explode_outer(from_json(df2.value,MapType(StringType(),StringType()))))
    # Get date field.
    df_date = df2.filter(df2.key == "pushed_at")
    df_h = df_date.filter("value < date'{}'".format(date))
    df_l = df_date.filter("value >= date'{}'".format(date))
    return (df_h, df_l)

# Spark streaming does not support append mode with aggregations. 
# Spark streaming does not support joins with append mode.
# Must flatten again.
def transform_data(df, cols):
    df = df.select(df.id, explode_outer(from_json(df.id,MapType(StringType(),StringType()))))
    df = df.select(df.id, explode_outer(from_json(df.value,MapType(StringType(),StringType()))))
    df = df.filter(df.key.isin(cols))
    df = df.withColumn("tmp", to_string_udf(df.key, df.value))
    df = df.groupBy("id").agg(collect_set("tmp").alias("res"))
    df = df.withColumn("value", to_json_udf(df.res))
    return df

def write_to_kafka_topic(df, topic):
    df.select("value")\
        .writeStream\
        .format("kafka")\
        .option("kafka.bootstrap.servers", "kafka-1:19092,kafka-2:29092,kafka-3:39092") \
        .option("topic", topic) \
        .outputMode("complete") \
        .start() \

if __name__ == '__main__':
    topic = "msr14.repos"
    historical_topic = topic + ".historical"
    live_topic = topic + ".live"
    date = "2013-07-30"
    cols = ["id", "name", "description", "size", "watchers_count", "forks_count", "open_issues_count", "pushed_at", "updated_at"]

    # Create, read, and split into historical and live data frames
    spark = create_spark_session()
    df = read_from_kafka_topic(spark, topic)
    dfs = split_data(df, date)

    # Transform DF.   
    df_h = transform_data(dfs[0], cols)
    df_l = transform_data(dfs[1], cols)

    # Write histocal and live dataframes to kafka topics
    write_to_kafka_topic(df_h, historical_topic)
    write_to_kafka_topic(df_l, live_topic)

    spark.streams.awaitAnyTermination()
    spark.stop()
