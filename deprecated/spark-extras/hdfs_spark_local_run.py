from pyspark.sql.functions import udf, explode, explode_outer, from_json, col, to_json
from pyspark.sql.types import ArrayType, BooleanType, IntegerType, MapType, StringType, StructField, StructType, TimestampType

commits_schema = StructType([
    StructField("_id", StructType([
        StructField("_id", StructType([
            StructField("$oid", StringType(), True)
        ])),
        StructField("copyingData", BooleanType(), True)
    ])),
    StructField("operationType", StringType(), True),
    StructField("documentKey", StructType([
        StructField("_id", StructType([
            StructField("$oid", StringType(), True)
        ]))
    ])),
    StructField("fullDocument", StructType([
        StructField("_id", StructType([
            StructField("$oid", StringType(), True)
        ])),
        StructField("sha", StringType(), True),
        StructField("commit", StructType([
            StructField("author", StructType([
                StructField("name", StringType(), True),
                StructField("email", StringType(), True),
                StructField("date", StringType(), True)
            ])),
            StructField("committer", StructType([
                StructField("name", StringType(), True),
                StructField("email", StringType(), True),
                StructField("date", StringType(), True)
            ])),
            StructField("message", StringType(), True),
            StructField("tree", StructType([
                StructField("sha", StringType(), True),
                StructField("url", StringType(), True)
            ])),
            StructField("url", StringType(), True),
            StructField("comment_count", IntegerType(), True),
        ])),
        StructField("url", StringType(), True),
        StructField("html_url", StringType(), True),
        StructField("comments_url", StringType(), True),
        StructField("author", StructType([
            StructField("login", StringType(), True),
            StructField("id", IntegerType(), True),
            StructField("avatar_url", StringType(), True),
            StructField("gravatar_url", StringType(), True),
            StructField("url", StringType(), True),
            StructField("html_url", StringType(), True),
            StructField("followers_url", StringType(), True),
            StructField("following_url", StringType(), True),
            StructField("gists_url", StringType(), True),
            StructField("starred_url", StringType(), True),
            StructField("subscriptions_url", StringType(), True),
            StructField("organizations_url", StringType(), True),
            StructField("repos_url", StringType(), True),
            StructField("events_url", StringType(), True),
            StructField("received_events_url", StringType(), True),
            StructField("type", StringType(), True)
        ])),
        StructField("committer", StructType([
            StructField("login", StringType(), True),
            StructField("id", IntegerType(), True),
            StructField("avatar_url", StringType(), True),
            StructField("gravatar_url", StringType(), True),
            StructField("url", StringType(), True),
            StructField("html_url", StringType(), True),
            StructField("followers_url", StringType(), True),
            StructField("following_url", StringType(), True),
            StructField("gists_url", StringType(), True),
            StructField("starred_url", StringType(), True),
            StructField("subscriptions_url", StringType(), True),
            StructField("organizations_url", StringType(), True),
            StructField("repos_url", StringType(), True),
            StructField("events_url", StringType(), True),
            StructField("received_events_url", StringType(), True),
            StructField("type", StringType(), True)
        ])),
        StructField("parents", ArrayType(
            StructType([
                StructField("sha", StringType(), True),
                StructField("url", StringType(), True),
                StructField("html_url", StringType(), True)
            ])
        )),
        StructField("stats", StructType([
            StructField("total", IntegerType(), True),
            StructField("additions", IntegerType(), True),
            StructField("deletions", IntegerType(), True)
        ])),
        StructField("files", ArrayType(
            StructType([
                StructField("sha", StringType(), True),
                StructField("filename", StringType(), True),
                StructField("status", StringType(), True),
                StructField("additions", IntegerType(), True),
                StructField("deletions", IntegerType(), True),
                StructField("changes", IntegerType(), True),
                StructField("blob_url", StringType(), True),
                StructField("raw_url", StringType(), True),
                StructField("content_url", StringType(), True),
                StructField("patch", StringType(), True)
            ])
        ))
    ]))
])

data = """
{
    "schema": {
        "type": "string",
        "optional": false
    },
    "payload": "{\"_id\": {\"_id\": {\"$oid\": \"5234b621bd35433fe6000b31\"}, \"copyingData\": true}, \"operationType\": \"insert\", \"documentKey\": {\"_id\": {\"$oid\": \"5234b621bd35433fe6000b31\"}}, \"fullDocument\": {\"_id\": {\"$oid\": \"5234b621bd35433fe6000b31\"}, \"sha\": \"4131958a0e72bae459077f5ac2e5adbd812f6460\", \"commit\": {\"author\": {\"name\": \"Hylke Bons\", \"email\": \"hylkebons@gmail.com\", \"date\": \"2011-04-27T16:44:59Z\"}, \"committer\": {\"name\": \"Hylke Bons\", \"email\": \"hylkebons@gmail.com\", \"date\": \"2011-04-27T16:44:59Z\"}, \"message\": \"repo: don't fetch changes when we're busy adding files\", \"tree\": {\"sha\": \"2a5b9b18a7e6c5f7a288927cb485b289f58d2ee2\", \"url\": \"https://api.github.com/repos/hbons/SparkleShare/git/trees/2a5b9b18a7e6c5f7a288927cb485b289f58d2ee2\"}, \"url\": \"https://api.github.com/repos/hbons/SparkleShare/git/commits/4131958a0e72bae459077f5ac2e5adbd812f6460\", \"comment_count\": 0}, \"url\": \"https://api.github.com/repos/hbons/SparkleShare/commits/4131958a0e72bae459077f5ac2e5adbd812f6460\", \"html_url\": \"https://github.com/hbons/SparkleShare/commit/4131958a0e72bae459077f5ac2e5adbd812f6460\", \"comments_url\": \"https://api.github.com/repos/hbons/SparkleShare/commits/4131958a0e72bae459077f5ac2e5adbd812f6460/comments\", \"author\": {\"login\": \"hbons\", \"id\": 103326, \"avatar_url\": \"https://0.gravatar.com/avatar/3e8eee17a5d6c6a20b073af0d2b2b48b?d=https%3A%2F%2Fidenticons.github.com%2F2e5fadcaa4eb3bf4dc17469427bf475b.png\", \"gravatar_id\": \"3e8eee17a5d6c6a20b073af0d2b2b48b\", \"url\": \"https://api.github.com/users/hbons\", \"html_url\": \"https://github.com/hbons\", \"followers_url\": \"https://api.github.com/users/hbons/followers\", \"following_url\": \"https://api.github.com/users/hbons/following{/other_user}\", \"gists_url\": \"https://api.github.com/users/hbons/gists{/gist_id}\", \"starred_url\": \"https://api.github.com/users/hbons/starred{/owner}{/repo}\", \"subscriptions_url\": \"https://api.github.com/users/hbons/subscriptions\", \"organizations_url\": \"https://api.github.com/users/hbons/orgs\", \"repos_url\": \"https://api.github.com/users/hbons/repos\", \"events_url\": \"https://api.github.com/users/hbons/events{/privacy}\", \"received_events_url\": \"https://api.github.com/users/hbons/received_events\", \"type\": \"User\"}, \"committer\": {\"login\": \"hbons\", \"id\": 103326, \"avatar_url\": \"https://0.gravatar.com/avatar/3e8eee17a5d6c6a20b073af0d2b2b48b?d=https%3A%2F%2Fidenticons.github.com%2F2e5fadcaa4eb3bf4dc17469427bf475b.png\", \"gravatar_id\": \"3e8eee17a5d6c6a20b073af0d2b2b48b\", \"url\": \"https://api.github.com/users/hbons\", \"html_url\": \"https://github.com/hbons\", \"followers_url\": \"https://api.github.com/users/hbons/followers\", \"following_url\": \"https://api.github.com/users/hbons/following{/other_user}\", \"gists_url\": \"https://api.github.com/users/hbons/gists{/gist_id}\", \"starred_url\": \"https://api.github.com/users/hbons/starred{/owner}{/repo}\", \"subscriptions_url\": \"https://api.github.com/users/hbons/subscriptions\", \"organizations_url\": \"https://api.github.com/users/hbons/orgs\", \"repos_url\": \"https://api.github.com/users/hbons/repos\", \"events_url\": \"https://api.github.com/users/hbons/events{/privacy}\", \"received_events_url\": \"https://api.github.com/users/hbons/received_events\", \"type\": \"User\"}, \"parents\": [{\"sha\": \"ef89629e7c0a4f37ec4abaf48a89b53de701b5d3\", \"url\": \"https://api.github.com/repos/hbons/SparkleShare/commits/ef89629e7c0a4f37ec4abaf48a89b53de701b5d3\", \"html_url\": \"https://github.com/hbons/SparkleShare/commit/ef89629e7c0a4f37ec4abaf48a89b53de701b5d3\"}], \"stats\": {\"total\": 12, \"additions\": 7, \"deletions\": 5}, \"files\": [{\"sha\": \"6fe5bfe6a600c104ca2ad0ac434de3495fcb451b\", \"filename\": \"SparkleLib/SparkleRepo.cs\", \"status\": \"modified\", \"additions\": 7, \"deletions\": 5, \"changes\": 12, \"blob_url\": \"https://github.com/hbons/SparkleShare/blob/4131958a0e72bae459077f5ac2e5adbd812f6460/SparkleLib/SparkleRepo.cs\", \"raw_url\": \"https://github.com/hbons/SparkleShare/raw/4131958a0e72bae459077f5ac2e5adbd812f6460/SparkleLib/SparkleRepo.cs\", \"contents_url\": \"https://api.github.com/repos/hbons/SparkleShare/contents/SparkleLib/SparkleRepo.cs?ref=4131958a0e72bae459077f5ac2e5adbd812f6460\", \"patch\": \" \"}]}, \"ns\": {\"db\": \"msr14\", \"coll\": \"commits_limit100k\"}}"
}
"""

@udf
def clean_udf(value):
    value = value.replace("\"payload\": \"{", "\"payload\": {", 1)
    index = value.rfind("\"")
    return value[:index] + value[index + 1:]

df = spark.createDataFrame([(1, data)],["key","value"])
df2 = df.withColumn("cleaned", clean_udf(df.value))
df2 = df2.select(explode_outer(from_json(df2.cleaned,MapType(StringType(),StringType()))))
df2 = df2.filter(df2.key == "payload").select(from_json(df2.value, commits_schema).alias("payload")).select("payload.*")
df2.select("fullDocument.commit.committer.date", "fullDocument.stats.additions", "fullDocument.stats.deletions").show()
