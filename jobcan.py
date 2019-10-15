import sys
import os
from selenium import webdriver
import chromedriver_binary
import time
from jobcan_settings import EMAIL, PASSWORD


LOGINURL = "https://id.jobcan.jp/users/sign_in?app_key=atd"
TIMECARDURL = "https://ssl.jobcan.jp/employee"
STATUS_WORKING = "入室中"
STATUS_OUTOFFICE = "退室中"
STATUS_NOTWORK = "未出勤"


class Jobcan:
    @classmethod
    def __open_page(cls, url=LOGINURL):
        print(url)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument('--lang=ja')

        cls.driver = webdriver.Chrome(options=options)
        #cls.driver = webdriver.Chrome()
        cls.driver.get(url)
        cls.driver.set_window_size(1500,1000)

    @classmethod
    def __login(cls, email=EMAIL, password=PASSWORD):
        cls.__open_page()
        cls.driver.find_element_by_id('user_email').send_keys(email)
        cls.driver.find_element_by_id('user_password').send_keys(password)
        
        cls.driver.find_element_by_xpath('//*[@id="new_user"]/input[4]').click()
        time.sleep(3)

        if(cls.driver.current_url != TIMECARDURL):
            cls.driver.find_element_by_xpath('//*[@id="jbc-app-links"]/ul/li[2]/a').click()
            # Change window
            handle_array = cls.driver.window_handles
            cls.driver.switch_to.window(handle_array[1])

    @classmethod
    def __logout(cls):
        cls.driver.find_element_by_id('jbcid-dropdown-button').click()
        cls.driver.find_element_by_xpath('//*[@id="jbcid-user-menu"]/ul/li[2]/a').click()


    @classmethod
    def work_start(cls, email, password):
        cls.__login(email, password)
        status = cls.driver.find_element_by_xpath('//*[@id="working_status"]').get_attribute("textContent")
        if(status == STATUS_NOTWORK):
            cls.driver.find_element_by_id('adit-button-push').click()
            res = "出勤しました"
        elif(status == STATUS_OUTOFFICE):
            res = '退勤済みです'
        elif(status == STATUS_WORKING):
            res = "出勤済みです"

        cls.__logout()
        cls.driver.quit()
        return res

    @classmethod
    def work_end(cls, email, password):
        cls.__login(email, password)
        status = cls.driver.find_element_by_xpath('//*[@id="working_status"]').get_attribute("textContent")

        if(status == STATUS_WORKING):
            cls.driver.find_element_by_id('adit-button-push').click()
            cls.driver.find_element_by_xpath('//*[@id="jbcid-user-menu"]/ul/li[2]/a').click()
            res = "退勤しました"
        elif(status == STATUS_OUTOFFICE):
            res = '退勤済みです'
        elif(status == STATUS_NOTWORK):
            res = "出勤してません"

        cls.__logout()
        cls.driver.quit()
        return res


if __name__ == "__main__":
    args = sys.argv
    if (args[1] == "start"):
        Jobcan.work_start()
    elif (args[1] == "end"):
        Jobcan.work_end()
    else:
        print('引数("start" or "end")を設定してください')

