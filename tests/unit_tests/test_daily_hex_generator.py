from unittest import TestCase, main
from unittest.mock import patch
from datetime import datetime
from utility.daily_hex_generator import get_hex_of_the_day
import re
validate_regex = re.compile("^[0-9A-Fa-f]{6}$") #hex string of length 6


class TestLeaderboardRepo(TestCase):
    @patch("utility.daily_hex_generator.datetime")
    def test_fetch_records(self, mock_class):
        for i in range(12):
            mock_class.now.return_value = datetime(2020 + i, 1 + i, 15 + i) #seemingly random dates
            mock_class.return_value = datetime(2020,1,1)
            hex_string = get_hex_of_the_day()
            validate_regex.search(hex_string) != None #check if the returned string is valid

# if __name__ == '__main__':
#     main()