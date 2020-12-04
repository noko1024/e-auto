import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import lxml
import getpass
import time
import re

basePath = os.path.split(os.path.realpath(__file__))[0]

#ユーザー情報の入力待機
chromedriver_path = "D:\download\chrome\chromedriver.exe"#input("chromedriverpath>")#Chromedriverのディレクトリパス
user_id = input("id>")#e-LeaningのID
user_pass = getpass.getpass("pass>")#e-Leaningのパスワード

#Chromeの起動
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
browser = webdriver.Chrome(chromedriver_path,options=options)
browser.implicitly_wait(1)

root_URL = "https://www.brains-el.jp"

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

#lessonの進捗度100%じゃないもののURLのリストを返す関数
def LessonDataGet():
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

		lesson_list = lesson.select(".list-group.subject_list")

		lesson_URL_list = []

		for lesn in lesson_list:
			percent = LessonProgressGet(lesn)
			if percent != "100" and percent is not None:
				lesson_URL_list.append(LessonURLGet(lesn))

		break

	return lesson_URL_list

#lessonの進捗度を取得する関数
def LessonProgressGet(lesson):

	if lesson is None:
		return None

	progress_div = lesson.find("div",{"class":"progress_rate"})

	percent = progress_div.find("span")
	percent = re.search(r"\d+",percent.get_text())
	if percent is None:
		return None

	return percent.group()

#lessonのURLを取得する関数
def LessonURLGet(lesson):

	lesson_URL = lesson.find("a",{"class":"list-group-item clearfix"})

	lesson_URL = lesson_URL.get("href")
	if lesson_URL is None:
		return ""

	return lesson_URL

def AutoQuestionSelect(lesson_URL):
	while True:
		browser_source = browser.page_source
		#ページソースがなければ==読み込みに失敗したら一秒待ってF5
		if not browser_source:
			time.sleep(1)
			browser.refresh()
			continue

		soup = BeautifulSoup(browser_source,"lxml")
		question_list = soup.select(".each_step")

		if question_list is None:
			break

		for question in question_list:
			btn_chk = question.select(".class_button.btn.btn_warning")
			if btn_chk is None:
				continue
			question_type = question.find("span",{"class":"step_name"}).get_text()
			break

		if not question_type:
			break

		btn = browser.find_element_by_css_selector(".class_button.btn.btn-warning")
		btn.click()

		print(question_type)

		#ここで自動解答関数を呼ぶ

		#これはすぐ飛ばないようにする為
		time.sleep(30)
		#これは多分解答後に自動的に戻されるはずなのでいらないかも(自動解答出来上がるまでは必須)
		browser.get(root_URL+lesson_URL)

def main():
	login()
	btn = browser.find_element_by_css_selector(".button.btn.btn-large.btn-.learning.text-center.center-block.blue_green")
	time.sleep(1)
	btn.click()
	lesson_URL_list = LessonDataGet()
	for lesson_URL in lesson_URL_list:
		browser.get(root_URL+lesson_URL)
		AutoQuestionSelect(lesson_URL)
		#これはすぐ飛ばないようにする為
		time.sleep(10)


if __name__ == "__main__":
	main()
