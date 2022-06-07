import pytest
from app import create_app
from unittest.mock import patch
import os
from bs4 import BeautifulSoup


# @pytest.fixture(scope="session", autouse=True)
# def create_test_database(tmp_path_factory):
#     tmp_dir = tmp_path_factory.mktemp("tmp")
#     database_filename = tmp_dir / "test_database.db"
#     create_db(database_filename)
#     os.environ["DATABASE_FILENAME"] = str(database_filename)


@pytest.fixture(scope='function') #set to function because the client uses cookies
def test_client():
    flask_app = create_app(__name__)
    testing_client = flask_app.test_client(use_cookies=True)
    context = flask_app.app_context()
    context.push()
    yield testing_client
    context.pop()
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
    
    
    
    
    # Given
#     request_payload = {
#         "username": "foulen",
#         "fullname": "Foulen Ben Foulen"
#     }

#     expected_body = {
#         "username": "foulen",
#         "full_name": "Foulen Ben Foulen"
#     }
#     expected_status_code = 200

#     expected_body_keys = ["user_id", "username", "full_name"]

#     # When
#     response = test_client.post('/users', json=request_payload)

#     # Then
#     assert expected_status_code == response.status_code
#     assert response.json | expected_body == response.json
#     assert set(expected_body_keys) == response.json.keys()
#     assert int == type(response.json["user_id"])


# def test_create_user2(test_client):
#     # Given
#     request_payload = {
#         "username": "amine",
#         "fullname": "Amine Haj Ali"
#     }

#     expected_body = {
#         "username": "amine",
#         "full_name": "Amine Haj Ali"
#     }
#     expected_status_code = 200

#     expected_body_keys = ["user_id", "username", "full_name"]

#     # When
#     response = test_client.post('/users', json=request_payload)

#     # Then
#     assert expected_status_code == response.status_code
#     assert response.json | expected_body == response.json
#     assert set(expected_body_keys) == response.json.keys()
#     assert int == type(response.json["user_id"])


# def test_get_all_users(test_client):
#     # Given
#     expected_response = [
#         {
#             "user_id": 1,
#             "username": "foulen",
#             "full_name": "Foulen Ben Foulen"
#         },
#         {
#             "user_id": 2,
#             "username": "amine",
#             "full_name": "Amine Haj Ali"
#         }
#     ]

#     # When
#     response = test_client.get("/users")

#     # Then
#     assert 200 == response.status_code
#     assert expected_response == response.json


# def test_delete_existing_user(test_client):
#     # Given
#     user_id_to_delete = 1
#     expected_body = {
#         "message": "User deleted successfully"
#     }

#     # When
#     response = test_client.delete(f'/users/{user_id_to_delete}')

#     # Then
#     assert expected_body == response.json


# def test_delete_already_deleted_user(test_client):
#     # Given
#     user_id_to_delete = 1
#     expected_body = {
#         "message": "User not deleted successfully"
#     }

#     # When
#     response = test_client.delete(f'/users/{user_id_to_delete}')

#     # Then
#     assert expected_body == response.json


# def test_delete_not_existing_user(test_client):
#     # Given
#     user_id_to_delete = 70
#     expected_body = {
#         "message": "User not deleted successfully"
#     }

#     # When
#     response = test_client.delete(f'/users/{user_id_to_delete}')

#     # Then
#     assert expected_body == response.json


# def test_get_users_after_delete(test_client):
#     # Given
#     expected_response = [
#         {
#             "user_id": 2,
#             "username": "amine",
#             "full_name": "Amine Haj Ali"
#         }
#     ]

#     # When
#     response = test_client.get("/users")

#     # Then
#     assert 200 == response.status_code
#     assert expected_response == response.json