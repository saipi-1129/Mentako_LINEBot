import requests

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