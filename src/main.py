import time
import requests
import mysql.connector
from mysql.connector import Error

import json

from modules.connect import connect_to_sql
from modules.check import check_stream
from modules.insert import insert_to_sql
from modules.select import select_from_sql
from modules.push import push_message

# --- Uptime Kuma監視用のWebサーバー機能を追加 ---
import http.server
import socketserver
import threading

PORT = 8000 # Uptime Kumaがアクセスするポート番号

class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

def run_health_check_server():
    with socketserver.TCPServer(("", PORT), HealthCheckHandler) as httpd:
        print(f"Health check server started at port {PORT}")
        httpd.serve_forever()
# --- ここまで追加 ---

# 配信のモニタリング
def monitor_stream(userids):
    last_live_ids = {}
    while True:
        for userid in userids:
            live_id, name, message = check_stream(userid)
            if live_id:
                latest = select_from_sql(userid)
                if live_id != latest:
                    print("送信しました")
                    push_message(message)
                    insert_to_sql(userid, name, live_id)
                    print(message)
                else:
                    print(f"{userid}の配信は新しくありません。再確認します。")
            else:
                print(f"{userid}の配信は行われていません。再確認します。")
            print("////////////////////////////////////////////////////")
        time.sleep(10)

# ユーザーIDリスト
userids = ["126246308"]

# 実行
if __name__ == "__main__":
    # --- ヘルスチェックサーバーを別スレッドで起動 ---
    health_thread = threading.Thread(target=run_health_check_server)
    health_thread.daemon = True
    health_thread.start()
    # --- ここまで追加 ---

    monitor_stream(userids)
