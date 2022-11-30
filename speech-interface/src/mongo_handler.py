# https://www.mongodb.com/languages/python

from pymongo import MongoClient
from enum import Enum
import time

class GetQueries(Enum):
    ALL_TIME_WATCHERS_COUNT = {
        "category": "all_time",
        "type": "watchers_count"
    }
    LATEST_LANGUAGE_COUNT = {
        "category": "latest",
        "type": "language_count"
    }
    ALL_TIME_LANGUAGE_COUNT = {
        "category": "all time",
        "type": "language_count"
    }
    LATEST_FORKS_COUNT = {
        "category": "latest",
        "type": "forks_count"
    }
    ALL_TIME_FORKS_COUNT = {
        "category": "all time",
        "type": "forks_count"
    }
    LATEST_OPEN_ISSUES_COUNT = {
        "category": "latest",
        "type": "open_issues_count"
    }
    ALL_TIME_OPEN_ISSUES_COUNT = {
        "category": "all time",
        "type": "open_issues_count"
    }
    ALL_TIME_SIZE = {
        "category": "all time",
        "type": "size"
    }
    ALL_TIME_TOTAL = {
        "category": "all time",
        "type": "total"
    }
    LATEST_ADDITIONS = {
        "category": "latest",
        "type": "additions"
    }
    LATEST_DELETIONS = {
        "category": "latest",
        "type": "deletions"
    }

class MongoHandler(object):
    def __init__(self):
        start_time = time.time()
        print("Connecting to MongoDB...", end=" ")

        CONNECTION_STRING = "mongodb://localhost:27017"
        self.mongo_client = MongoClient(CONNECTION_STRING)

        print("Done. Took {} milliseconds.".format(round((time.time() - start_time) * 1000, 2)))

    def get_query(self, query):
        start_time = time.time()
        print("Querying MongoDB...", end=" ")

        col = self.mongo_client["answer_db"]["answer_col"]
        result = list(col.find(
            {"category": query.value["category"], "type": query.value["type"]},
        ))

        print("Done. Took {} milliseconds.".format(round((time.time() - start_time) * 1000, 2)))

        # We are only interested in two fields
        return {
            "full_name": result[0]["placements"][0]["full_name"],
            "count": result[0]["placements"][0]["count"]
        }
