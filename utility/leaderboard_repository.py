import sqlite3
from datetime import datetime
import os

def mm_ss(duration):
    seconds = int(duration/1000)
    minutes = int(seconds/60)
    seconds -= minutes*60
    return f"{minutes}:{seconds}"

def date_str(milliseconds):
    seconds = milliseconds/1000
    date = datetime.fromtimestamp(seconds)
    return str(date)

class leaderboard_repository:
    def __init__(self):
        self.database_name = os.environ.get('DATABASE_FILENAME', 'leaderboard.db')
        con = sqlite3.connect(self.database_name)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS leaderboard
                (start_date INTEGER, end_date INTEGER, goal TEXT, attempts INTEGER)''')
        con.commit()
        cur.close()
        con.close()
        pass

    def add_record(self, start_time, end_time, goal, nb_attempts):
        con = sqlite3.connect(self.database_name)
        cur = con.cursor()
        cur.execute("INSERT INTO leaderboard VALUES (?, ?, ?, ?)", (start_time, end_time, goal, nb_attempts))
        con.commit()
        cur.close()
        con.close()

    def fetch_records(self):
        con = sqlite3.connect(self.database_name)
        cur = con.cursor()
        cur.execute("select * from leaderboard ORDER BY attempts")
        result = []
        for row in cur.fetchall():
            start_time, end_time, goal, attempts = row
            result.append({
                'start_time': date_str(start_time),
                'time_taken': mm_ss(end_time - start_time),
                'goal': goal,
                'attempts': attempts
                })
        return result
        cur.close()
        con.close()
