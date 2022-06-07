# 0xordle
this project was created for the software testing and devops courses lab, it contains unit/integration/e2e tests, and a CI/CD pipeline that deploys to an ECS cluster
#### Project overview
Just like the hit puzzle game wordle, this game shows you a color and you have to guess it's html #RRGGBB hex color string
from the home page you can click dailyhex to enter the game or check the leaderboards

#Tests
- unit tests: 
  - test_leaderboard_repo: this performs a unit test on the repository reponsible for saving and fetching leaderboard data, the database is mocked and we test the result of a fetch (some treatement is done on the data extracted from the database before it's sent to the app in order to make it easier to show to the client)
  - test_game_state: game state is responsible for holding the state of the game and every action possible has to go through this state (all the validations are in this class)
    - test_creation: tests the validation of 3 invalid goals (the string that the player has to guess) possible invalid values are too short, too long or contain non hex characters (0-9a-z)
    - test_play: tests the validation of 3 inputs that the user can play, these have the same invalid values as the previous test, it also enters a valid value and checks if it has been saved in the attempts array that is shown to the player
    - test_generate_board: just like wordle the board shows if a character is a match (green), wrong (black)or in the wrong position(orange), this function goes through all attempts made by the player and generates structured data that can be shown to the player in the format that was explained. the test picks a goal, inserts two user attempts and checks if the correct board has been generated
    - 
