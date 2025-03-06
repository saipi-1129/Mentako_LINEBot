from modules.push import push_message

def test_push_message():
    message = "これはテストメッセージです。"
    try:
        print("テストメッセージを送信します")
        push_message(message)
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        assert False    

    assert True