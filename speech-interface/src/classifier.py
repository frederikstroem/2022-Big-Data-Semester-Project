from mongo_handler import MongoHandler, GetQueries

class Classifier(object):
    def __init__(self):
        self.mongo_handler = MongoHandler()
        # https://stackoverflow.com/a/33344929
        self.lookups = [  # (regex, question, answer)
            (
                'watchers',
                'What repository has the most watchers?',
                'The repository "{full_name}" has the most watchers, with a total of {count}.'.format_map(self.mongo_handler.get_query(GetQueries.ALL_TIME_WATCHERS_COUNT))
            ),
        ]
