import re
from collections import Counter
from datetime import datetime
validate_regex = re.compile("^[0-9A-Fa-f]{6}$")
class game_state:

    def __init__(self, goal, attempts = [], max_attempts = 6, did_win = False, start_time=0, end_time = -1):
        assert(game_state.validate_input(goal))
        self.attempts = attempts
        self.goal = goal.lower()
        self.max_attempts = max_attempts
        self.did_win = did_win
        self.start_time = start_time
        self.end_time = end_time
    
    
    def write_state_to_session(self, session):
        session['attempts'] = self.attempts
        session['goal'] = self.goal
        session['max_attempts'] = self.max_attempts
        session['did_win'] = self.did_win
        session['start_time'] = self.start_time
        session['end_time'] = self.end_time
    
    @staticmethod
    def read_state_from_session(session):
        return game_state(goal=session['goal'] ,attempts=session['attempts'], max_attempts=session['max_attempts'], did_win=session['did_win'], start_time=session['start_time'], end_time=session['end_time'])
    
    def attempts_remaining(self):
        return self.max_attempts - len(self.attempts)
    @staticmethod
    def validate_input(input):
        return validate_regex.search(input) != None

    def play(self, new_attempt):
        new_attempt = new_attempt.lower()
        self.attempts.append(new_attempt)
        if(new_attempt == self.goal):
            self.did_win = True
            self.end_time = datetime.now().timestamp() * 1000

    def get_board(self):
        count = Counter()
        result = []
        for attempt in self.attempts:
            count.update(self.goal)
            row = []
            for index, char in enumerate(attempt):
                if(char == self.goal[index]):
                    row.append({"char":char, "status": "match"})
                    count.subtract(char)
                else:
                    row.append({"char":char, "status": "wrong"})
            for char in row:
                if(char['status']=="wrong" and count[char['char']]>0):
                    char['status'] = "exists"
                    count.subtract(char['char'])
            count.clear()
            result.append(row)
        return result

    def __str__(self):
        return f"goal={self.goal} attempts={self.attempts} max_attemtps={self.max_attempts} did_win={self.did_win}"