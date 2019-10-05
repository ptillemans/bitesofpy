from csv import DictReader
from os import path
from urllib.request import urlretrieve
from collections import Counter

DATA = path.join('/tmp', 'bite_output_log.txt')
if not path.isfile(DATA):
    urlretrieve('https://bit.ly/2HoFZBd', DATA)


class BiteStats:

    def _load_data(self, data) -> list:
        with open(data) as f:
            return list(DictReader(f))

    def __init__(self, data=DATA):
        self.rows = self._load_data(data)

    @property
    def number_bites_accessed(self) -> int:
        """Get the number of unique Bites accessed"""
        unique_bites = {d['bite'] for d in self.rows}
        return len(unique_bites)

    @property
    def number_bites_resolved(self) -> int:
        """Get the number of unique Bites resolved (completed=True)"""
        solved_bites = {d['bite']
            for d in self.rows 
            if d['completed'] == 'True'}
        return len(solved_bites)

    @property
    def number_users_active(self) -> int:
        """Get the number of unique users in the data set"""
        unique_users = {d['user'] 
            for d in self.rows}
        return len(unique_users)

    @property
    def number_users_solving_bites(self) -> int:
        """Get the number of unique users that resolved
           one or more Bites"""
        unique_solving_users = { d['user'] 
            for d in self.rows 
            if d['completed'] == 'True'}
        return len(unique_solving_users)

    @property
    def top_bite_by_number_of_clicks(self) -> str:
        """Get the Bite that got accessed the most
           (= in most rows)"""
        bite_cntr = Counter([d['bite'] for d in self.rows])
        most_accessed = bite_cntr.most_common(1)[0]
        return most_accessed[0]

    @property
    def top_user_by_bites_completed(self) -> str:
        """Get the user that completed the most Bites"""
        user_cntr = Counter([d['user']
            for d in self.rows
            if d['completed'] == 'True'])
        most_completed = user_cntr.most_common(1)[0]
        return most_completed[0]