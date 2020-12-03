import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
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
        browser_source = browser.page_source
        #ページソースがなければ==読み込みに失敗したら一秒待ってF5
        if not browser_source:
            time.sleep(1)
            browser.refresh()
            continue

        soup = BeautifulSoup(browser_source,"lxml")
        lesson = soup.find("div",{"class":"panel panel-success"})
        
        if lesson is None:
            break
        
        progress_div_list = lesson.select("div.progress_rate")

        for progress in progress_div_list:
            percent = progress.find("span")
            print(percent.get_text())

        break


def main():
    login()
    btn = browser.find_element_by_css_selector(".button.btn.btn-large.btn-.learning.text-center.center-block.blue_green")
    time.sleep(1)
    btn.click()
    LessonProgressGet()


if __name__ == "__main__":
    main()
