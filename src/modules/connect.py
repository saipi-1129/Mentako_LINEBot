import json
import mysql.connector
from mysql.connector import Error

# config.json の読み込み
with open('config.json', 'r') as f:
    config = json.load(f)

# 設定の利用
DB_HOST = config['DB']['HOST']
DB_NAME = config['DB']['NAME']
DB_USER = config['DB']['USER']
DB_PASSWORD = config['DB']['PASSWORD']

def connect_to_sql():
    try:
        connection = mysql.connector.connect(
            host= DB_HOST,  # MySQLサーバーのIP
            database= DB_NAME,  # 使用するデータベース名
            user= DB_USER,  # MySQLのユーザー名
            password= DB_PASSWORD  # MySQLのパスワード
        )
        if connection.is_connected():
            print("Successfully connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None