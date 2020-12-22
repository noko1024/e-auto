import os
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import lxml
import getpass
import time
import re
import json
import random

basePath = os.path.split(os.path.realpath(__file__))[0]

#ユーザー情報の入力待機
chromedriver_path = "" #Chromedriverのディレクトリパス
if os.name == "nt":
	chromedriver_path=os.path.join(*[basePath,"lib","chromedriver.exe"])
else:
	chromedriver_path = os.path.join(*[basePath,"lib","chromedriver"])

user_id = input("id>")#e-LeaningのID
user_pass = getpass.getpass("pass>")#e-Leaningのパスワード

#Chromeの起動
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
browser = webdriver.Chrome(chromedriver_path,options=options)
browser.implicitly_wait(5)

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
		#TAG
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
			btn_chk = question.select(".class_button.btn.btn-warning")
			if not btn_chk:
				continue
			break

		#lessson_num:lessonいくつかを取得
		#course_num : courseを取得(通常レッスンとランダム演習の判定に利用)

		btn = browser.find_element_by_css_selector(".class_button.btn.btn-warning")
		btn.click()

		print(question_type)
		time.sleep(1)
		#ここで自動解答関数を呼ぶ
		while True:
			stop_time = random.randint(1,6)#元(3,40)テスト推奨(7,20)
			print("sleep in",stop_time)
			time.sleep(stop_time)
			print("sleep out")
			get_bool,question_type,question_japanese,question_text = GetAns()
			print(get_bool)
			if not get_bool:
				break
			AutoAns(question_type,question_japanese,question_text)

		#これはすぐ飛ばないようにする為
		time.sleep(3)
		#これは多分解答後に自動的に戻されるはずなのでいらないかも(自動解答出来上がるまでは必須)
		#browser.get(root_URL+lesson_URL)

def GetAns():

	count = 1
	get_bool = True
	while True:
		try:
			soup = BeautifulSoup(browser.page_source,"lxml")
			question_text = soup.find("p",{"class":"blanked_text"}).get_text()
			question_text: str = re.sub("-+","",question_text)
			question_japanese: str = soup.find("p",{"class":"hint_japanese"}).get_text().strip()
			question_type: str = soup.find("div",{"class":"pull-left"}).get_text().split()[2]
			question_type_index = question_type.find("（")
			question_type = question_type[:question_type_index]
			break
		except:
			if count == 2:
				get_bool = False
				question_text = question_japanese = question_type = None
				break
			else:
				count += 1
				print(count)
				browser.refresh()
				time.sleep(1)
				continue
	print("question")
	print(question_type,question_japanese,question_text)
	print("----")

	return get_bool,question_type,question_japanese,question_text

def AutoAns(question_type,question_japanese,question_text):

	#jsonFileの読み込み
	with open(os.path.join(basePath,"lesson.json"), encoding='utf-8') as f:
		ans_json = json.load(f)

	answer: list = (ans_json[question_japanese]).split()#jsonfileからの英文
	print(answer)
	question: list = question_text.split()#webページからの英文

	#解答に必要なリストを取得
	result: list  = AutoAnsExtraction(list(answer),list(question))
	result = [res.strip(".").strip("?").strip("!") for res in result]#jsonとwebから導いた解答の英単語
	print(result)
	soup = BeautifulSoup(browser.page_source,"lxml")

	if question_type == "択一問題":

		ans_list = soup.select(".each_choice")

		for ans in ans_list:
			ans_word = ans.get("data-answer")

			print("ans_word:",ans_word)
			print("word:"+" ".join(result))

			if ans_word == " ".join(result):
				ans_btn = f"//a[@data-answer=\"{ans_word}\"]/span/button"
				print(ans_btn)
				break
		try:
			btn = browser.find_element_by_xpath(ans_btn)
			btn.click()
		except:
			time.sleep(1)
			btn = browser.find_element_by_xpath(ans_btn)
			btn.click()

	elif question_type =="並べ替え問題":

		ans_list = soup.select(".each_choice.ui-draggable.ui-draggable-handle")

		ans_btns = []

		while True:

			for ans in ans_list:
				#選択肢の中身
				ans_word : str = ans.get("data-answer").split()#下に転がってる解答するためのボタンの中の英文

				print("ans_word:",ans_word)
				print("word:",result)

				if len(ans_word) == 1:
					ans_word = "".join(ans_word)
					if ans_word == result[0]:
						result.remove(ans_word)
						ans_btns.append(f"//a[@data-answer=\"{ans_word}\"]")
						print(ans_word)
						break
				elif len(ans_word) > 1:
					hw_long = len(result) - len(ans_word)
					if len(AutoAnsExtraction(result,ans_word)) == hw_long :
						result.remove(ans_word[:hw_long])
						ans_word = " ".join(ans_word)
						ans_btns.append(f"//a[@data-answer=\"{ans_word}\"]")
						print(ans_word)
						break
				elif not result:
					break

		for ans_btn in ans_btns:
			btn = browser.find_element_by_xpath(ans_btn)
			btn.click()

		btn = browser.find_element_by_css_selector(".answer.btn.btn-warning")
		btn.click()

	elif question_type == "空所記入問題":
		for ans in result:
			ans_form = browser.find_element_by_xpath("//*[@class=\"blank_container\"]/input")
			ans_form.clear()
			ans_form.send_keys(ans)
			time.sleep(0.5)

		btn = browser.find_element_by_css_selector(".answer.btn.btn-warning")
		btn.click()

	stop_time = random.randint(1,3)
	time.sleep(stop_time)

	btn = browser.find_element_by_css_selector(".btn.btn-default.next_question")
	btn.click()




def AutoAnsExtraction(answer,question):#answer = jsonfileから読み取った英文　question = webページから受け取った英文
	for ques in question:
		if ques in answer:
			answer.remove(ques)
		else:
			continue

	return answer

"""
def AutoSelect():
    quest =
"""

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
	input("PLEASE PRESS ENTER")
