import json
from linebot.v3.messaging import MessagingApi, TextMessage, BroadcastRequest
from linebot.v3.messaging.api_client import ApiClient, Configuration

# config.json の読み込み
with open('config.json', 'r') as f:
    config = json.load(f)

LINE_CHANNEL_ACCESS_TOKEN = config['LINE_CHANNEL_ACCESS_TOKEN']

configuration = Configuration()
configuration.access_token = LINE_CHANNEL_ACCESS_TOKEN



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