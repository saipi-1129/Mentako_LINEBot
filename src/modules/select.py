from mysql.connector import Error
from .connect import connect_to_sql

def select_from_sql(userid):
    connection = None  # connection を初期化
    try:
        # MySQLに接続
        connection = connect_to_sql()
        if connection is None:
            print("Failed to connect to MySQL")
            return None

        if connection.is_connected():
            cursor = connection.cursor()

            select_query = """SELECT live_id FROM test WHERE userid = %s ORDER BY live_id ASC LIMIT 1;"""
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