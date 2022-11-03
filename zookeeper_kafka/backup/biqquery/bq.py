from google.cloud import bigquery
from google.oauth2 import service_account
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='192.168.159.10:29092')
key_path = "/sa.json"
credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

query = """SELECT *
            FROM `bigquery-public-data.github_repos.sample_repos`
            LIMIT 50000
        """
print("Running query")
query_job = client.query(query)

print("Sending to kafka topic")
for row in query_job:
    producer.send('sample_repos', str.encode("repo_name={}, watch_count={}".format(row[0], row[1])))