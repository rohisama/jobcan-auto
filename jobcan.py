import sys
import os
from selenium import webdriver
import chromedriver_binary
import time
from jobcan_settings import EMAIL, PASSWORD


LOGINURL = "https://id.jobcan.jp/users/sign_in?app_key=atd"
TIMECARDURL = "https://ssl.jobcan.jp/employee"


class Jobcan:
    @classmethod
    def __open_page(cls, url=LOGINURL):
        print(url)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument('--lang=ja')

        #cls.driver = webdriver.Chrome(options=options)
        cls.driver = webdriver.Chrome()
        cls.driver.get(url)
        cls.driver.set_window_size(1500,1000)

    @classmethod
    def __login(cls):
        cls.__open_page()
        cls.driver.find_element_by_id('user_email').send_keys(EMAIL)
        cls.driver.find_element_by_id('user_password').send_keys(PASSWORD)
        
        cls.driver.find_element_by_xpath('//*[@id="new_user"]/input[4]').click()
        time.sleep(3)

        if(cls.driver.current_url != TIMECARDURL):
            cls.driver.find_element_by_xpath('//*[@id="jbc-app-links"]/ul/li[2]/a').click()
            # Change window
            handle_array = cls.driver.window_handles
            cls.driver.switch_to.window(handle_array[1])

    @classmethod
    def work_start(cls):
        cls.__login()
        status = cls.driver.find_element_by_xpath('//*[@id="working_status"]').get_attribute("textContent")
        if(status == "退室中"):
            cls.driver.find_element_by_id('adit-button-push').click()
            print("出勤しました")
        else:
            print('退勤してません')
        cls.driver.quit()

    @classmethod
    def work_end(cls):
        cls.__login()
        status = cls.driver.find_element_by_xpath('//*[@id="working_status"]').get_attribute("textContent")
        if(status == "入室中"):
            cls.driver.find_element_by_id('adit-button-push').click()
            print("退勤しました")
        else:
            print('出勤してません')
        cls.driver.quit()


if __name__ == "__main__":
    args = sys.argv
    if (args[1] == "start"):
        Jobcan.work_start()
    elif (args[1] == "end"):
        Jobcan.work_end()

