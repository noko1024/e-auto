import os
import platform
import subprocess
import zipfile
import time
import re
import urllib.request
from pip._internal import main as pipcom
import importlib

basePath = os.path.split(os.path.realpath(__file__))[0]
elog_path = os.path.join(basePath,"error.log")

def main():
    print("e-Learning自動回答プログラム <e-auto> セットアップシステムです。")
    print("Google Chromeが必要です。予めご準備ください。\n")
    time.sleep(3)

    #プラットホーム取得
    print("プラットホーム検出中…")
    time.sleep(2)
    pf = platform.system()

    if  pf == "Windows":
        try:
            ver = WinSetup()
            seleniumDownload("win32",ver)
        
        except Exception as e:
            with open(elog_path,mode="a") as f:
                f.write(str(e))                
            print("セットアップ中に問題が発生しました。\nエラーログを参照して下さい。")
            return 1


    elif pf == "Darwin":
        try:
            ver = MacSetup()
            seleniumDownload("mac64",ver)

        except Exception as e:
            with open(elog_path,mode="a") as f:
                f.write(str(e))  
            print("セットアップ中に問題が発生しました。\nエラーログを参照して下さい。")
            return 1


    elif pf =="Linux":
        try:
            ver = LiSetup()
            seleniumDownload("linux64",ver)

        except Exception as e:
            print("セットアップ中に問題が発生しました。\nエラーログを参照して下さい。")
            with open(elog_path,mode="a") as f:
                f.write(str(e))  
            return 1
    
    #ライブラリインストール
    try:
        pipInstall()
    except Exception as e:
        print("ライブラリのインストール中に問題が発生しました。\nエラーログを参照して下さい。")
        with open(elog_path,mode="a") as f:
            f.write(str(e))
        return 1
    
    print("セットアップは正常に終了しました。")
    time.sleep(1)
    input("Press Enter key")

def WinSetup():
    print("プラットホーム検出:Windows")
    path = ""
    print("セットアップ中…")

    #クロームのバージョンを検出 (x86ユーザーもいたので…)
    try:
        res = subprocess.check_output('dir /B/O-N "C:\Program Files\Google\Chrome\Application" |findstr "^[0-9].*¥>',shell=True)
    except:
        res = subprocess.check_output('dir /B/O-N "C:\Program Files(x86) \Google\Chrome\Application" |findstr "^[0-9].*¥>',shell=True)
    ver = res.decode("utf-8")[0:2]
    return ver


def MacSetup():
    print("プラットホーム検出:macOS")
    #クロームのバージョンを検出
    res = subprocess.check_output("/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version",shell=True)
    ver = re.search(r'\d+.*',res.decode("utf-8")).group()[0:2]
    return ver


def LiSetup():
    print("プラットホーム検出:Linux")
    #クロームのバージョンを検出
    res = subprocess.check_output("google-chrome --version|grep -o [0-9].*",shell=True)
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
        return
    else:
        seleniumVer = seleniumVer.group()
    
    #seleniumのzipをダウンロード
    print("seleniumをダウンロードしています…")
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

    print("seleniumのダウンロード完了")
    time.sleep(1)

def pipInstall():
    print("必要なライブラリをインストール中…\n")
    install_list = ["selenium","bs4","lxml","requests"]
    for lib_name in install_list:
        try:
            importlib.import_module(lib_name)
        except ImportError:
            pipcom(["install",lib_name])
    print("\nライブラリのインストール完了")
    time.sleep(1)



main()
