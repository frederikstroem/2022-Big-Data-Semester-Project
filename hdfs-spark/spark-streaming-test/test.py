from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,MapType,StringType
from pyspark.sql.functions import explode, split, to_json, array, col, from_json, struct, udf

import locale
locale.getdefaultlocale()
locale.getpreferredencoding()

@udf
def additions_UDF(value):
    start = value.find("additions")
    end = value.find("deletions")
    return value[start:end]

# Create SparkSession and configure it
spark = SparkSession.builder.appName('initialTest') \
    .config('spark.master','spark://spark-master:17077') \
    .config('spark.executor.cores', 1) \
    .config('spark.cores.max', 1) \
    .config('spark.executor.memory', '1g') \
    .config('spark.sql.streaming.checkpointLocation','hdfs://namenode:9000/stream-checkpoint/') \
    .getOrCreate()
    
# Create a read stream from Kafka and a topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka-1:19092,kafka-2:29092,10.kafka-3:39092") \
    .option("startingOffsets", "earliest")\
    .option("subscribe", "temp") \
    .load()

df1 = df.selectExpr("CAST(value AS STRING)")
df2 = df1.withColumn("addition", additions_UDF(df1.value))
df.printSchema()
df2.select(to_json(struct("value", "addition")).alias('value')) \
    .writeStream\
    .format('kafka')\
    .option("kafka.bootstrap.servers", "kafka-1:19092,kafka-2:29092,kafka-3:39092") \
    .option("topic", "additions") \
    .outputMode("append") \
    .start().awaitTermination()
