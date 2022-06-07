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
  - test_daily_hex_generator: this class is responsible for generating a random hex each day, in this test we mocked `datetime.now()` and tested 12 seemingly random dates and checked if the output is a valid hex string with 6 characters
- integration tests:
  - test_app: these tests create a temporary test database and a test client the only thing that is mocked is the daily_hex_generator because we have to test what happens if the goal string changes mid game and that can only be simulated if we mock the generator
    - test_home: this just gets home and checks if the status code is 200
    - test_dailyhex_changing_mid_game: this test plays a couple of rounds of the game, triggers a goal change, and checks if the round has been reset with the new goal string as intended
    - test_winning_adding_record_to_db: this plays the winning string that matches the goal and checks if it has been added to the leaderboard
- e2e tests
  - this test uses selenium and does a full run of the app, it clicks the daily hex button to enter the game, plays a few attempts, plays the winning string, goes back to home and from there it checks the leaderboard. the test takes a screenshot at each state and also performs asserts
# CI/CD pipleline
in this section we create the required files in order to implement a full CI/CD pipeline that deploys to AWS's ECS
- CI:
  - in order to perform tests the pipeline loads in the code from github, sets up python environement, installs all dependencies within requirements.txt and runs the tests described above, and reports the resulting code coverage
  - it also creates a docker image and uploads it to my personal docker hub account that will be later deployed on ECS
- CD:
  - we configured task definitions that use the docker container created earlier and also made the required configuration to create a cluster and a service that uses elastic load balancing. we also configured security groups to expose the app on port 5000
![image](https://user-images.githubusercontent.com/60438665/172498661-7adc9cb9-57ce-447b-9cb0-19819565f31b.png)

