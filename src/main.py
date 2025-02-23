import time
import requests
import mysql.connector
from mysql.connector import Error


import json 

from modules.connect import connect_to_sql
from modules.check import check_stream
from modules.insert import insert_to_sql
from modules.select import select_from_sql
from modules.push import push_message  # push_messageを追加




# 配信のモニタリング
def monitor_stream(userids):
    last_live_ids = {}  # ユーザーごとの最後のlive_idを記録
    while True:
        for userid in userids:
            live_id, name, message = check_stream(userid)  # 各ユーザーの配信状況を確認
            if live_id:
                latest = select_from_sql(userid) #あらかじめSQLにuseridを追加しておかないとエラーが出る
                if live_id != latest:  # 新しい配信IDなら処理
                    print("送信しました")
                    # push_message(message)  # LINEにメッセージを送信
                    insert_to_sql(userid, name, live_id)  # データベースに挿入
                    print(message)  # メッセージを表示
                else:
                    print(f"{userid}の配信は新しくありません。再確認します。")
            else:
                print(f"{userid}の配信は行われていません。再確認します。")
            print("////////////////////////////////////////////////////")
        time.sleep(10)  # 1分待機

# ユーザーIDリスト
userids = [""]  # 実際のユーザーIDをリストに追加してください

# 実行  
monitor_stream(userids)