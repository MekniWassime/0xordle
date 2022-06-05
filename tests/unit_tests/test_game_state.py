
#from app import calculate_factorial, get_user
from unittest import TestCase, main
from unittest.mock import patch
from models.game_state import game_state
#import mymod


class TestGameState(TestCase):
    def test_play(self):
        state = game_state("ABCDEF")
        with self.assertRaises(Exception):
            state.play("ABCDE")     #length too short
        with self.assertRaises(Exception):
            state.play("ABCDEFA")   #length too long
        with self.assertRaises(Exception):
            state.play("ABCXEB")    #invalid format
        nbr_attempts_before_playing = len(state.attempts)
        state.play("AABBCC")
        nbr_attempts_after_playing = len(state.attempts)
        assert(nbr_attempts_after_playing == nbr_attempts_before_playing + 1)

    def test_generate_board(self):
        state = game_state("ABBBCD")
        state.play("BBBCDF") #B wrong position, #B matches, #B matches, #C wrong position, #D wrong position, #F wrong
        state.play("BBBB12") #B wrong, #B matches, #B matches, #B matches, #1 wrong, #2 wrong
        board = state.get_board()
        first_guess = board[0]
        assert( first_guess[0]["status"] == 'exists' and
                first_guess[1]["status"] == 'match' and
                first_guess[2]["status"] == 'match' and
                first_guess[3]["status"] == 'exists' and
                first_guess[4]["status"] == 'exists' and
                first_guess[5]["status"] == 'wrong')
        
        second_guess = board[1]
        assert( second_guess[0]["status"] == 'wrong' and
                second_guess[1]["status"] == 'match' and
                second_guess[2]["status"] == 'match' and
                second_guess[3]["status"] == 'match' and
                second_guess[4]["status"] == 'wrong' and
                second_guess[5]["status"] == 'wrong')
    # def test_hello(self):
    #     assert "hello" == "hello"

    # def test_factorial(self):
    #     assert calculate_factorial(3) == 6

    # @patch("app.sqlite3")
    # def test_get_user(sel f, mock_class):
    #     # given
    #     mock_class.connect().execute().fetchone.return_value = (1, 'wassim')

    #     expected_user = {
    #         "user_id": 1,
    #         "name": "wassim"
    #     }

    #     # when
    #     item = get_user(1)

    #     # then
    #     assert item == expected_user


if __name__ == '__main__':
    main()