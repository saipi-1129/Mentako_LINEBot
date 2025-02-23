from mysql.connector import Error
from .connect import connect_to_sql
import datetime
import pytz

# 現在時刻を取得
timezone = pytz.timezone("Asia/Tokyo")
current_time = datetime.datetime.now(timezone)

# MySQLに接続してデータを保存
def insert_to_sql(userid, name, live_id):
    connection = None  # connection を初期化
    try:
        # MySQLに接続
        connection = connect_to_sql()
        if connection is None:
            print("Failed to connect to MySQL")
            return

        if connection.is_connected():
            cursor = connection.cursor()

            # データを挿入するSQLクエリ
            insert_query = """INSERT INTO test (userid, name, live_id, time) VALUES (%s, %s, %s, %s)"""
            cursor.execute(insert_query, (userid, name, live_id, current_time))
            connection.commit()
            print(f"Record inserted: Name = {name}, Live ID = {live_id}")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    finally:
        if connection is not None and connection.is_connected():  # connectionが初期化されているか確認
            cursor.close()
            connection.close()
            print("MySQL connection is closed")