import os
import requests
from selenium import webdriver
import bs4
import lxml
import getpass
import time

basePath = os.path.split(os.path.realpath(__file__))[0]

#ユーザー情報の入力待機
chromedriver_path = input("chromedriverpath>")#Chromedriverのディレクトリパス
user_id = input("id>")#e-LeaningのID
user_pass = getpass.getpass("pass>")#e-Leaningのパスワード

#Chromeの起動
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
browser = webdriver.Chrome(chromedriver_path,options=options)
browser.implicitly_wait(1)

#ログイン用の関数
def login():
    #ログインのURL
    url_login = "https://www.brains-el.jp/"
    browser.get(url_login)
    #ユーザー情報の送信
    e = browser.find_element_by_xpath("//*[@data-name=\"login_id\"]")
    e.clear()
    e.send_keys(user_id)
    e = browser.find_element_by_xpath("//*[@data-name=\"password\"]")
    e.clear()
    e.send_keys(user_pass)
    #ログインボタンのクリック
    btn = browser.find_element_by_css_selector(".btn.btn-default.pull-right")
    btn.click()

def LessonProgressGet():
    while True:
        if not browser.page_source:
            time.sleep(1)
            browser.refresh()
            continue
        
        soup = bs4(browser.page_source,"lxml")
        lesson = soup.find_all("div",{"class":"panel panel-success"})
        if not lesson:
            break
        lessonList=lesson.select("")


def main():
    login()
    browser.get("https://www.brains-el.jp/dashboard/")
    btn = browser.find_element_by_css_selector(".button.btn.btn-large.btn-.learning.text-center.center-block.blue_green")
    btn.click()


if __name__ == "__main__":
    main()
