
#from app import calculate_factorial, get_user
from unittest import TestCase, main
from unittest.mock import patch
from models.game_state import game_state
#import mymod


class TestGameState(TestCase):
    def test_creation(self):
        with self.assertRaises(Exception):
            game_state("ABCDE")     #length too short
        with self.assertRaises(Exception):
            game_state("ABCDEFA")   #length too long
        with self.assertRaises(Exception):
            game_state("ABCXEB")    #invalid format
        assert(game_state("ABCDEF"))#valid creation

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
        assert( 
            first_guess[0]["status"] == 'exists' and
            first_guess[1]["status"] == 'match' and
            first_guess[2]["status"] == 'match' and
            first_guess[3]["status"] == 'exists' and
            first_guess[4]["status"] == 'exists' and
            first_guess[5]["status"] == 'wrong'
        )
        
        second_guess = board[1]
        assert(
            second_guess[0]["status"] == 'wrong' and
            second_guess[1]["status"] == 'match' and
            second_guess[2]["status"] == 'match' and
            second_guess[3]["status"] == 'match' and
            second_guess[4]["status"] == 'wrong' and
            second_guess[5]["status"] == 'wrong'
        )

if __name__ == '__main__':
    main()