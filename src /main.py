import time
import requests
import mysql.connector
from mysql.connector import Error
from linebot.v3.messaging import MessagingApi, TextMessage, BroadcastRequest
from linebot.v3.messaging.api_client import ApiClient, Configuration
import datetime


LINE_CHANNEL_ACCESS_TOKEN = ''  # 自分のアクセストークンに置き換えてください
configuration = Configuration()
configuration.access_token = LINE_CHANNEL_ACCESS_TOKEN

# 現在時刻を取得
current_time = datetime.datetime.now()


# 配信状況のチェック
def check_stream(userid):
    url = f"https://www.mirrativ.com/api/user/profile?user_id={userid}"
    res = requests.get(url)

    if res.status_code == 200:
        try:
            data = res.json()
            if data and "onlive" in data and data["onlive"] and "live_id" in data["onlive"]:
                live_id = data["onlive"]["live_id"]
                name = data["name"]
                print(f"配信ID: {live_id}, ユーザー名: {name}")
                message = f"{name}さんが配信を始めました！配信URL: https://www.mirrativ.com/live/{live_id}"
                return live_id, name, message
            else:
                return None, None, None  # 配信中でなければNoneを返す
        except KeyError:
            return None, None, None  # データに問題があればNoneを返す
    else:
        return None, None, "配信状況の確認に失敗しました。"  # APIリクエストが失敗した場合のエラーメッセージ

# MySQLに接続してデータを保存
def insert_to_sql(userid,name, live_id):
    connection = None  # connection を初期化
    try:
        # MySQLに接続
        connection = mysql.connector.connect(
            host='',  # MySQLサーバーのIP
            database='',  # 使用するデータベース名
            user='',  # MySQLのユーザー名
            password=''  # MySQLのパスワード
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # データを挿入するSQLクエリ
            insert_query = """INSERT INTO test (userid,name, live_id, time) VALUES (%s,%s, %s, %s)"""
            cursor.execute(insert_query, (userid,name, live_id, current_time))
            connection.commit()
            print(f"Record inserted: Name = {name}, Live ID = {live_id}")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    finally:
        if connection is not None and connection.is_connected():  # connectionが初期化されているか確認
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def select_from_sql(userid):
    connection = None  # connection を初期化
    try:
        # MySQLに接続
        connection = mysql.connector.connect(
            host='',  # MySQLサーバーのIP
            database='',  # 使用するデータベース名
            user='',  # MySQLのユーザー名
            password=''  # MySQLのパスワード
        )

        if connection.is_connected():
            cursor = connection.cursor()

            select_query = """SELECT live_id FROM test WHERE userid = %s ORDER BY live_id DESC LIMIT 1;"""
            # パラメータをタプルで渡す (userid, )の形式
            cursor.execute(select_query, (userid,))
            result = cursor.fetchone()
            if result:
                latest_live_id = result[0]
                print(f"latest Live ID = {latest_live_id}")
                return latest_live_id
            else:
                print(f"No live_id found for userid = {userid}")
                return None

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    finally:
        if connection is not None and connection.is_connected():  # connectionが初期化されているか確認
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# 配信のモニタリング
def monitor_stream(userids):
    last_live_ids = {}  # ユーザーごとの最後のlive_idを記録
    while True:
        for userid in userids:
            live_id, name, message = check_stream(userid)  # 各ユーザーの配信状況を確認
            if live_id:
                latest = select_from_sql(userid) #あらかじめSQLにuseridを追加しておかないとエラーが出る
                if live_id != latest:  # 新しい配信IDなら処理
                    push_message(message)  # LINEにメッセージを送信
                    insert_to_sql(userid,name, live_id)  # データベースに挿入
                    print(message)  # メッセージを表示
                else:
                    print(f"{userid}の配信は新しくありません。再確認します。")
            else:
                print(f"{userid}の配信は行われていません。再確認します。")
            print("////////////////////////////////////////////////////")
        time.sleep(60)  # 1分待機


def push_message(message):
    try:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.broadcast(
                BroadcastRequest(
                    messages=[TextMessage(text=message)]  # メッセージをリスト形式で渡す
                )
            )
        print("メッセージがブロードキャストされました")
    except Exception as e:
        print(f"エラーが発生しました: {e}")


# ユーザーIDリスト
userids = [""]  # 実際のユーザーIDをリストに追加してください

# 実行  
monitor_stream(userids)
