import sqlite3
from datetime import datetime
con = sqlite3.connect('leaderboard.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS leaderboard
                (start_date INTEGER, end_date INTEGER, goal TEXT, attempts INTEGER)''')

con.commit()
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
    def add_record(start_time, end_time, goal, nb_attempts):
        con = sqlite3.connect('leaderboard.db')
        cur = con.cursor()
        cur.execute("INSERT INTO leaderboard VALUES (?, ?, ?, ?)", (start_time, end_time, goal, nb_attempts))
        con.commit()
        cur.close()
        con.close()

    def fetch_records():
        con = sqlite3.connect('leaderboard.db')
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
