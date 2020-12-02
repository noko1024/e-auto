import os
import requests
from selenium import webdriver
import bs4
import lxml
import getpass

basePath = os.path.split(os.path.realpath(__file__))[0]

chromedriver_path = input("chromedriverpath>")#Chromedriverのディレクトリパス
user_id = input("id>")#e-LearningのID
user_pass = getpass.getpass("pass>")#e-Leaningのパスワード

#初期設定
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
browser = webdriver.Chrome(chromedriver_path,chrome_options=options)
browser.implicitly_wait(1)

def login():
    url_login = "https://www.brains-el.jp/"
    browser.get(url_login)
    element = browser.find_element_by_xpath('//*[@data-name="login_id"]')
    element.clear()
    element.send_keys(user_id)
    element = browser.find_element_by_xpath('//*[@data-name="password"]')
    element.clear()
    element.send_keys(user_pass)
    btn = browser.find_element_by_css_selector('button.btn.btn-default.pull-right')
    btn.click()


def main():
    login()
    btn = browser.find_element_by_css_selector('button.button.btn.btn-large.btn-.learning.text-center.center-block.blue_green')
    btn.click()


if __name__ == "__main__":
    main()
