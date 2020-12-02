import os
import platform
import subprocess
import zipfile
import time

def main():
    print("e-Learning自動回答プログラム <e-auto> セットアップシステムです。")
    print("Google Chromeが必要です。予めご準備ください。\n")
    time.sleep(3)
    #プラットホーム取得
    print("プラットホーム検出中…")
    time.sleep(2)
    pf = platform.system()

    if  pf == "Windows":
        WinSetup()
    elif pf == "Darwin":
        MacSetup()
    elif pf =="Linux":
        LiSetup()






def WinSetup():
    path = ""
    print("プラットホーム検出:Windows")
    print("Google Chrome の存在するファイルのパスを入力してください。")
    path = input("")
    print("セットアップ中…")
    res=subprocess.check_output('dir /B/O-N "'+path+ '"|findstr "^[0-9].*¥>',shell=True)
    print(res)


def MacSetup():
    print("プラットホーム検出:macOS")
    res=subprocess.check_output("/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version")
    pass

def LiSetup():
    print("プラットホーム検出:Linux")
    res=subprocess.check_output("google-chrome --version|grep -o [0-9].*")
    pass

main()
