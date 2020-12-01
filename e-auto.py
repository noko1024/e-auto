import os
import requests
from selenium import webdriver
import bs4
import lxml
import getpass

basePath = os.path.split(os.path.realpath(__file__))[0]

chromedriver_path = input("chromedriverpath>")
user_id = input("id>")
user_pass = getpass.getpass("pass>")

#初期設定
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
browser = webdriver.Chrome("chromedriver_path",chrome_options=options)
browser.implicitly_wait(1)

def login():
    url_login = "https://www.brains-el.jp/"
    browser.get(url_login)
    e = browser.find_element_by_xpath('//*[@data-name="login_id"]')
    e.clear()
    e.send_keys(user_id)
    e = browser.find_element_by_xpath('//*[@data-name="password"]')
    e.clear()
    e.send_keys(user_pass)
    btn = browser.find_element_by_css_selector('button.btn.btn-default.pull-right')
    btn.click()

login()
