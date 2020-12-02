import os
import requests
from selenium import webdriver
import bs4
import lxml
import getpass

basePath = os.path.split(os.path.realpath(__file__))[0]

#ユーザー情報の入力待機
chromedriver_path = input("chromedriverpath>")
user_id = input("id>")
user_pass = getpass.getpass("pass>")

#初期設定
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
browser = webdriver.Chrome("chromedriver_path",chrome_options=options)
browser.implicitly_wait(1)

#ログイン用の関数
def login():
    #ログインのURL
    url_login = "https://www.brains-el.jp/"
    browser.get(url_login)
    #ユーザー情報の送信
    e = browser.find_element_by_xpath('//*[@data-name="login_id"]')
    e.clear()
    e.send_keys(user_id)
    e = browser.find_element_by_xpath('//*[@data-name="password"]')
    e.clear()
    e.send_keys(user_pass)
    #ログインボタンのクリック
    btn = browser.find_element_by_css_selector('button.btn.btn-default.pull-right')
    btn.click()

login()
