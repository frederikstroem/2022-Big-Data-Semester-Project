from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, explode_outer, collect_set, from_json
from pyspark.sql.types import StringType, MapType
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

# Create SparkSession
spark = SparkSession.builder.appName('initialTest') \
    .config('spark.master','spark://spark-master:17077') \
    .config('spark.executor.cores', 1) \
    .config('spark.cores.max', 2) \
    .config('spark.executor.memory', '1g') \
    .config('spark.sql.streaming.checkpointLocation','hdfs://namenode:9000/stream-checkpoint/') \
    .getOrCreate()

# Read from Kafka topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka-1:19092,kafka-2:29092,10.kafka-3:39092") \
    .option("startingOffsets", "earliest")\
    .option("subscribe", "msr14.repos") \
    .load()

# Transform DF
cols = ["id", "name", "size", "description", "language", "watchers_count", "forks_count", "open_issues_count"]

df1 = df.selectExpr("CAST(value AS STRING)")
df2 = df1.select(explode_outer(from_json(df1.value,MapType(StringType(),StringType()))))
df2 = df2.select(df2.key.alias("key1"), df2.value.alias("value1"), explode_outer(from_json(df2.value,MapType(StringType(),StringType()))))
df2 = df2.filter(df2.key1 == "payload")
df2 = df2.select(df2.value1.alias("id"), explode_outer(from_json(df2.value,MapType(StringType(),StringType()))))
df2 = df2.filter(df2.key.isin(cols))
df2 = df2.withColumn("tmp", to_string_udf(df2.key, df2.value))

result = df2.groupBy("id").agg(collect_set("tmp").alias("res"))
result = result.withColumn("value", to_json_udf(result.res))

# Write to Kafka topic
result.select("value")\
    .writeStream\
    .format('kafka')\
    .option("kafka.bootstrap.servers", "kafka-1:19092,kafka-2:29092,kafka-3:39092") \
    .option("topic", "msr14.repos.processed") \
    .outputMode("complete") \
    .start() \
    .awaitTermination()

