
#from app import calculate_factorial, get_user
from unittest import TestCase, main
from unittest.mock import patch
from utility.leaderboard_repository import leaderboard_repository


class TestLeaderboardRepo(TestCase):
    @patch("utility.leaderboard_repository.sqlite3")
    def test_fetch_records(self, mock_class):
        mock_class.connect().cursor().fetchall.return_value = [
            (1654431010000, 1654431019000, 'a8c2d6', 2),
            (1654431050000, 1654431050000, 'a8c2d6', 5)
        ]
        expected_value = [
            {'start_time': '2022-06-05 13:10:10', 'time_taken': '0:9', 'goal': 'a8c2d6', 'attempts': 2},
            {'start_time': '2022-06-05 13:10:50', 'time_taken': '0:0', 'goal': 'a8c2d6', 'attempts': 5}
        ]
        result = leaderboard_repository.fetch_records()
        assert(result)
        assert(result == expected_value)

if __name__ == '__main__':
    main()