import pytest
from app import create_app
from unittest.mock import patch
import os
from bs4 import BeautifulSoup


@pytest.fixture(scope="session", autouse=True)
def create_test_database(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("tmp")
    database_filename = tmp_dir / "test_database.db"
    os.environ["DATABASE_FILENAME"] = str(database_filename)

@pytest.fixture(scope='function') #set to function because the client uses cookies
def test_client():
    flask_app = create_app(__name__)
    testing_client = flask_app.test_client(use_cookies=True)
    return testing_client
    # context = flask_app.app_context()
    # context.push()
    # yield testing_client
    # context.pop()

@pytest.fixture(scope='function')
def mock_daily_hex(mocker):
    mocked = mocker.patch("app.get_hex_of_the_day")
    mocked.return_value = "ABCDEF"
    return mocked

def test_home(test_client):
    response = test_client.get('/')
    assert response.status_code == 200

def test_dailyhex_post(test_client):
    response = test_client.get('/dailyhex')
    assert True

#test when the day ends while the player is playing (new daily hex every day) 
#should reset the board and all attempts made by the player
def test_dailyhex_changing_mid_game(mock_daily_hex, test_client):
    ### check if board is ussing the current mocked daily hex tring "ABCDEF"
    # Given
    expected_goal = mock_daily_hex.return_value
    # Where
    response = test_client.get('/dailyhex')
    # Then
    assert response.status_code == 200
    parsed_html = BeautifulSoup(response.data, 'html.parser')
    assert expected_goal.lower() in parsed_html.find(id="goal_color").attrs['style'].lower() #goal is used as color
    ### play one turn to change the game state so that we can check if it rest when the day switched
    # Given
    request_payload = {'user_input':'123456'}
    # Where
    response = test_client.post('/dailyhex', data= request_payload, follow_redirects=True)
    # Then
    assert response.status_code == 200
    parsed_html = BeautifulSoup(response.data, 'html.parser')
    assert len(parsed_html.select('#attempts_table > tr')) == 2 #table that shows attemps should contain two rows after he played 1 round
    ### now we are going to change the daily hex to simulate the day ending while the player is playing
    # Given
    new_expected_goal = "FEDCBA"
    mock_daily_hex.return_value = new_expected_goal
    # Where
    response = test_client.get('/dailyhex')
    # Then
    assert response.status_code == 200
    parsed_html = BeautifulSoup(response.data, 'html.parser')
    assert new_expected_goal.lower() in parsed_html.find(id="goal_color").attrs['style'].lower()
    assert len(parsed_html.select('#attempts_table > tr')) == 1 #this will only be true if the board reset as expected
    
def test_winning_adding_record_to_db(test_client, mock_daily_hex):
    ### check that the leaderboard is empty
    # Given no games have been won yet
    # Where
    response = test_client.get('/leaderboard')
    # Then
    assert response.status_code == 200
    parsed_html = BeautifulSoup(response.data, 'html.parser')
    assert len(parsed_html.select('#leaderboard_table > tr')) == 1 #only header <tr>
    ### play and win in two attempts
    # Given
    first_attempt = {'user_input': 'ABD2F1'}
    winning_attempt = {'user_input': 'ABCDEF'} #matches goal
    # Where
        # Where
    response = test_client.post('/dailyhex', data = first_attempt, follow_redirects=True)
        # Then
    assert response.status_code == 200
    parsed_html = BeautifulSoup(response.data, 'html.parser')  
    assert len(parsed_html.select('#win_message')) == 0 #didn't win yet
        # Where
    response = test_client.post('/dailyhex', data = winning_attempt, follow_redirects=True)
        # Then
    assert response.status_code == 200
    parsed_html = BeautifulSoup(response.data, 'html.parser')  
    assert len(parsed_html.select('#win_message')) == 1 #won the game, should be saved in leaderboard db
    ## check if the win was added in the leaderboard
    # Given one player won one game
    # Where
    response = test_client.get('/leaderboard')
    # Then
    assert response.status_code == 200
    parsed_html = BeautifulSoup(response.data, 'html.parser')
    assert len(parsed_html.select('#leaderboard_table > tr')) == 2 #header plus one entry for the win