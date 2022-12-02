import re
from mongo_handler import MongoHandler, GetQueries

class Classifier(object):
    def __init__(self):
        self.mongo_handler = MongoHandler()
        # https://stackoverflow.com/a/33344929
        self.lookups = [  # (regex, question, answer)
            (
                '^.*(watchers|watches).*$',
                'What repository has the most watchers?',
                'The repository "{full_name}" has the most watchers, with a total of {count}.'.format_map(self.mongo_handler.get_query(GetQueries.ALL_TIME_WATCHERS_COUNT))
            ),
            (
                '^(?!.*today).*issues.*$',
                'What repository has the largest number of open issues?',
                'The repository "{full_name}" has the largest number of open issues, with a total of {count}.'.format_map(self.mongo_handler.get_query(GetQueries.ALL_TIME_OPEN_ISSUES_COUNT))
            ),
            (
                '^(?!.*issues).*largest.*$',
                'What is the largest repository?',
                'The repository "{full_name}" is the largest, with a size of {count} bytes.'.format_map(self.mongo_handler.get_query(GetQueries.ALL_TIME_SIZE))
            ),
            (
                '^(?!.*today).*language.*$',
                'Which language is most used?',
                'The language "{full_name}" is the most used, with a total of {count} occurrences.'.format_map(self.mongo_handler.get_query(GetQueries.ALL_TIME_LANGUAGE_COUNT))
            ),
            (
                '^.*active.*$',
                'What is the most active repository?',
                'The repository "{full_name}" is the most active, with a total of {count} commits.'.format_map(self.mongo_handler.get_query(GetQueries.ALL_TIME_TOTAL))
            ),
            (
                '^(?!.*today).*forked.*$',
                'What is the most forked repository?',
                'The repository "{full_name}" is the most forked, with a total of {count} forks.'.format_map(self.mongo_handler.get_query(GetQueries.ALL_TIME_FORKS_COUNT))
            ),
            (
                '^.*language.*today|today.*language.*$',
                'What is the most popular language today?',
                'The language "{full_name}" is the most popular today, with a total of {count} occurrences.'.format_map(self.mongo_handler.get_query(GetQueries.LATEST_LANGUAGE_COUNT))
            ),
            (
                '^.*forked.*today|today.*forked.*$',
                'Which repository is most forked today?',
                'The repository "{full_name}" is the most forked today, with a total of {count} forks.'.format_map(self.mongo_handler.get_query(GetQueries.LATEST_FORKS_COUNT))
            ),
            (
                '^.*issues.*(today|to day)|(today|to day).*issues.*$',
                'Which repository has the most new issues today?',
                'The repository "{full_name}" has the most new issues today, with a total of {count}.'.format_map(self.mongo_handler.get_query(GetQueries.LATEST_OPEN_ISSUES_COUNT))
            ),
            (
                '^.*additions.*$',
                'What repository has the most new additions today?',
                'The repository "{full_name}" has the most new additions today, with a total of {count}.'.format_map(self.mongo_handler.get_query(GetQueries.LATEST_ADDITIONS))
            ),
            (
                '^.*deletions.*$',
                'What repository has the most new deletions today?',
                'The repository "{full_name}" has the most new deletions today, with a total of {count}.'.format_map(self.mongo_handler.get_query(GetQueries.LATEST_DELETIONS))
            )
        ]
        self.possible_quuestions_string = 'Possible questions are:\n* ' + '\n* '.join([lookup[1] for lookup in self.lookups])

    def classify(self, text):
        answer_tuple = None
        for lookup in self.lookups:
            if re.match(lookup[0], text):
                answer_tuple = lookup
                break

        if answer_tuple is not None:
            return f'Interpreted "{text}" as "{answer_tuple[1]}"\nAnswer: {answer_tuple[2]}'
        elif re.match('^.*help.*$', text):
            return f'Interpreted "{text}. {self.possible_quuestions_string}'
        else:
            return f'Could not interpret "{text}" as a question.\nSay "help" for a list of possible questions to ask!'
            #return f'Could not interpret "{text}" as a question.\n{self.possible_quuestions_string}'
