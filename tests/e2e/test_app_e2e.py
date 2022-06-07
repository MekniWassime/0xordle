from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
import os
import sqlite3
import time
import multiprocessing
from app import main
from webdriver_manager.chrome import ChromeDriverManager
from utility.daily_hex_generator import get_hex_of_the_day
os.environ["DATABASE_FILENAME"] = "test_database.db"
class AppE2E(TestCase):

    @classmethod
    def setUpClass(inst):
        inst.app_process = multiprocessing.Process(target=main)
        inst.app_process.start()
        time.sleep(1)
        inst.start = time.time()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--disable-gpu')
        #inst.driver = webdriver.Chrome(ChromeDriverManager().install())
        inst.driver = webdriver.Chrome(options=chrome_options)
        inst.driver.implicitly_wait(1)
        inst.driver.get('http://localhost:5000')
        inst.driver.save_screenshot('./tests/e2e/screenshots/home.png')

    def click_element(self ,id):
        element = self.driver.find_element(by=By.ID, value=id)
        element.click()

    def write_input(self, id, keys):
        input = self.driver.find_element(by=By.ID, value=id)
        input.send_keys(keys)

    def take_screenshot(self, file_name):
        self.driver.save_screenshot('./tests/e2e/screenshots/'+ file_name + '.png')

    def test_winning_and_check_leaderboard(self):
        self.driver.get("http://localhost:5000")
        self.click_element("daily_hex")
        self.take_screenshot("board_empty")
        
        wrong_attempt = "AABBCC"
        self.write_input("user_input", wrong_attempt)
        self.click_element("user_submit")
        self.take_screenshot("one_attempt")
        
        winning_string = get_hex_of_the_day()
        self.write_input("user_input", winning_string)
        self.click_element("user_submit")
        self.take_screenshot("winner_screen")
        assert self.driver.find_element(by=By.ID, value="win_message")

        self.click_element("logo")
        self.take_screenshot("home2")
        self.click_element("leaderboard")
        self.take_screenshot("leaderboard")
        


    # def test_01_register(self):
    #     pass
    #     self.driver.get("http://localhost:5000")
    #     self.driver.implicitly_wait(10)

    #     register_link = self.driver.find_element(by=By.ID, value='signup')
    #     self.driver.implicitly_wait(1)

    #     register_link.click()
    #     username_input = self.driver.find_element(by=By.NAME, value='username')

    #     username_input.send_keys('test')
    #     self.driver.implicitly_wait(1)

    #     password_input = self.driver.find_element(by=By.NAME, value='password')
    #     password_input.send_keys('test')
    #     self.driver.implicitly_wait(1)

    #     submit_button = self.driver.find_element(by=By.ID, value='submit_signup')
    #     submit_button.click()
    #     self.driver.implicitly_wait(1)

    #     expected_title = 'Registered'
    #     result_title = self.driver.find_element(by=By.ID, value='success')
    #     self.driver.save_screenshot('./Tests/E2E/Screenshots/registred.png')

    #     assert expected_title == result_title.text

    # def test_02_signin(self):
    #     pass
    #     self.driver.get("http://localhost:5000")
    #     self.driver.implicitly_wait(10)

    #     username_input = self.driver.find_element(by=By.NAME, value='username')
    #     username_input.send_keys('test')
    #     self.driver.implicitly_wait(1)

    #     password_input = self.driver.find_element(by=By.NAME, value='password')
    #     password_input.send_keys('test')
    #     self.driver.implicitly_wait(1)

    #     submit_button = self.driver.find_element(by=By.ID, value='submit_signin')
    #     submit_button.click()
    #     self.driver.implicitly_wait(1)

    #     expected_title = "Connected"
    #     result_title = self.driver.find_element(by=By.ID, value='success')
    #     self.driver.save_screenshot('./Tests/E2E/Screenshots/loggedin.png')

    #     assert expected_title == result_title.text

    # def test_03_add_Note(self):
    #     pass
    #     self.driver.get("http://localhost:5000")
    #     self.driver.implicitly_wait(10)

    #     add_note_button = self.driver.find_element(by=By.ID, value='add_new_note')
    #     add_note_button.click()
    #     self.driver.implicitly_wait(1)
    #     print("hello")
    #     title_input = self.driver.find_element(by=By.ID, value='title')
    #     title_input.send_keys('test')
    #     self.driver.implicitly_wait(1)

    #     details_input = self.driver.find_element(by=By.ID, value='details')
    #     details_input.send_keys('test')
    #     self.driver.implicitly_wait(1)

    #     self.driver.save_screenshot('./Tests/E2E/Screenshots/formAddNote.png')

    #     submit_button = self.driver.find_element(by=By.ID, value='add_note_button')
    #     submit_button.click()
    #     self.driver.implicitly_wait(1)

    #     expected_title = "Note added"
    #     result_title = self.driver.find_element(by=By.ID, value='success')
    #     self.driver.save_screenshot('./Tests/E2E/Screenshots/noteAdded.png')

    #     assert expected_title == result_title.text

    @classmethod
    def tearDownClass(inst):
        inst.end = time.time()
        elapsedtime = inst.end - inst.start
        print("Duration of test ", "{:.2f}".format(elapsedtime), "seconds")
        inst.driver.quit()
        inst.app_process.terminate()