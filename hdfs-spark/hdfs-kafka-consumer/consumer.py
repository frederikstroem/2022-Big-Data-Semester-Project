from hdfs import InsecureClient
from kafka import KafkaConsumer

from datetime import datetime
import time


def printer(str):
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")
    print(f"[{date}] [+] {str}")


printer("Kafka consumer init")

client = InsecureClient("http://namenode:9870", user="root")
consumer = KafkaConsumer(
    "temp",
    bootstrap_servers=["kafka-1:19092", "kafka-2:29092", "kafka-3:39092"],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="group1",
    value_deserializer=lambda x: x.decode("utf-8"),
)

for message in consumer:
    start = time.time()

    printer(f"Message received: {message}")

    value = message.value

    if value == "EOF":
        break

    with client.write("/test.txt", encoding="utf-8", overwrite=True) as writer:
        writer.write(value)

    duration = time.time() - start
    printer(f"Processed message in {round(duration, 2)} seconds.")
