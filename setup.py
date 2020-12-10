import os
import sys
import platform
import subprocess
import zipfile
import time
import re
import urllib.request
from pip import _internal
from pip._internal import main as pipcom
import importlib

basePath = os.path.split(os.path.realpath(__file__))[0]
elog_path = os.path.join(basePath,"error.txt")

def WinSetup():
    #クロームのバージョンを検出 (x86ユーザーもいたので…)
    try:
        res = subprocess.check_output('dir /B/O-N "C:\Program Files\Google\Chrome\Application" |findstr "^[0-9].*¥>',shell=True)
    except:
        res = subprocess.check_output('dir /B/O-N "C:\Program Files (x86)\Google\Chrome\Application" |findstr "^[0-9].*¥>',shell=True)
    ver = res.decode("utf-8")[0:2]
    return ver


def MacSetup():
    #クロームのバージョンを検出
    res = subprocess.check_output("/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version",shell=True)
    ver = re.search(r'\d+.*',res.decode("utf-8")).group()[0:2]
    return ver


def LiSetup():
    #クロームのバージョンを検出
    res = subprocess.check_output("google-chrome sssssssss --version|grep -o [0-9].*",shell=True)
    ver = res.decode("utf-8")[0:2]
    return ver


def seleniumDownload(OS,version):
    
    downloadPath = os.path.join(basePath,"temp.zip")
    
    #クロームのバージョンに応じたseleniumの最新バージョンを取得
    req = urllib.request.Request("https://chromedriver.storage.googleapis.com/LATEST_RELEASE_"+version)
    with urllib.request.urlopen(req) as res:
        seleniumVer = res.read().decode("utf-8")
    
    seleniumVer = re.search(r'\d+.*',seleniumVer)
    
    if seleniumVer is None:
        print("現在インストールされている Google Chrome はサポート対象外です。\n他のバーションでお試し下さい")
        return 1
    else:
        seleniumVer = seleniumVer.group()
    
    #seleniumのzipをダウンロード

    urllib.request.urlretrieve("https://chromedriver.storage.googleapis.com/"+seleniumVer+"/chromedriver_"+OS+".zip",downloadPath)

    seleniumPath = os.path.join(basePath,"lib")
    
    #既にlibフォルダがあるときはmkdirをスキップ
    try:
        os.mkdir(seleniumPath)
    except:
        pass

    #ZIPファイルを解凍しlibファイルに格納
    with zipfile.ZipFile(downloadPath) as existing_zip:
        existing_zip.extractall(seleniumPath)

    os.remove(downloadPath)

    return 0

def pipInstall():
    install_list = ["selenium","bs4","lxml","requests"]
    for lib_name in install_list:
        pipcom(["install",lib_name])

    return 0

def Install():
    print("e-Learning自動回答プログラム <e-auto> セットアップシステムです。")
    print("Google Chromeが必要です。予めご準備ください。\n")
    time.sleep(3)

    #プラットフォーム取得
    print("プラットフォーム検出中…")
    time.sleep(2)
    pf = platform.system()

    if  pf == "Windows":
        print("プラットフォーム検出:Windows")
        try:
            ver = WinSetup()
            print("seleniumをダウンロードしています…")
            seleniumDownload("win32",ver)
            print("seleniumのダウンロード完了")
        
        except Exception as e:
            with open(elog_path,mode="a",encoding="utf_8") as f:
                print(str(e))
                print("\n")
                f.write(str(e))                
            print("セットアップ中に問題が発生しました。\nエラーログを参照して下さい。")
            return 1


    elif pf == "Darwin":
        print("プラットフォーム検出:macOS")
        try:
            ver = MacSetup()
            print("seleniumをダウンロードしています…")
            seleniumDownload("mac64",ver)
            print("seleniumのダウンロード完了")

        except Exception as e:
            with open(elog_path,mode="a",encoding="utf_8") as f:
                f.write(str(e))  
            print("セットアップ中に問題が発生しました。\nエラーログを参照して下さい。")
            return 1


    elif pf =="Linux":
        print("プラットフォーム検出:Linux")
        try:
            ver = LiSetup()
            print("seleniumをダウンロードしています…")
            seleniumDownload("linux64",ver)
            print("seleniumのダウンロード完了")

        except Exception as e:
            print("セットアップ中に問題が発生しました。\nエラーログを参照して下さい。")
            with open(elog_path,mode="a",encoding="utf_8") as f:
                f.write(str(e))  
            return 1
    
    #ライブラリインストール
    try:
        print("必要なライブラリをインストール中…\n")
        pipInstall()
        print("\nライブラリのインストール完了")
    except Exception as e:
        print("ライブラリのインストール中に問題が発生しました。\nエラーログを参照して下さい。")
        with open(elog_path,mode="a",encoding="utf_8") as f:
            f.write(str(e))
        return 1
    
    print("セットアップは正常に終了しました。")
    time.sleep(1)
    input("Press Enter key")

#内部向け呼び出し用
def _InternalInstall(installMode=None):
    pf = platform.system()
    if installMode is None:
        if  pf == "Windows":
            seleniumDownload("win32",WinSetup())
        elif pf == "Darwin":
            seleniumDownload("mac64",MacSetup())
        elif pf =="Linux":
            seleniumDownload("linux64",LiSetup())
        pipInstall()

    elif installMode == "selenium":
        if pf == "Windows":
            seleniumDownload("win32",WinSetup())
        elif pf == "Darwin":
            seleniumDownload("mac64",MacSetup())
        elif pf =="Linux":
            seleniumDownload("linux64",LiSetup())

    elif installMode == "pip":
        pipInstall()
    
    return 0

#引数パターン
# setup.py internal [all or selenium or pip]
if len(sys.argv) == 3:
    #内部向け呼び出し時
    if sys.argv[1] == "internal":
        if sys.argv[2] == "all":
            _InternalInstall()
        if sys.argv[2] == "selenium":
            _InternalInstall("selenium")
        if sys.argv[2] == "pip":
            _InternalInstall("pip")

else:
    Install()
