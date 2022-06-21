import datetime
import hashlib
import hmac
import json
from random import sample

import psycopg2
from flask import Flask, request, render_template

BOT_TOKEN = ""
conn = psycopg2.connect(dbname='integrals', user='postgres',
                        password='200tdhj', host='api.pank.su')
# cursor = conn.cursor()
# cursor.execute('SELECT * FROM tables.topic')
# for row in cursor:
#     print(row)
app = Flask(__name__)


@app.route('/', methods=['GET'])
def dont_be_here():
    return 'Вас не должно быть здесь'


@app.route("/check_auth", methods=['POST'])
def check_auth():
    data = request.get_json()
    cursor = conn.cursor()
    cursor.execute(f"""SELECT user_id FROM tables.session 
    WHERE ip = '{request.remote_addr}' AND id = {data['session_id']} AND 
    secret_key = '{data['secret_key']}'""")
    user_id = cursor.fetchall()
    if len(user_id) != 0:
        user_id = user_id[0][0]
        if user_id == None:
            return "wait"
        token = str(hashlib.sha256(
            (str(datetime.datetime.now()) + BOT_TOKEN + str(user_id)).encode()).hexdigest())
        cursor.execute(
            f'''UPDATE tables.users SET token = '{token}' WHERE id = {user_id}''')
        conn.commit()
        cursor.close()
        return token
    else:
        cursor.close()
        return "data invalid", 401


@app.route("/test/<int:test_id>")
def start_test(test_id: int):
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM tables.test WHERE id = {test_id}""")
    test = cursor.fetchall()[0]
    cursor.close()
    return render_template("test.html", name=test[1], test_data=sample(test[2], test[5]),
                           sample=sample, len=len)


@app.route("/tests")
def tests():
    result = []
    cursor = conn.cursor()
    cursor.execute("""SELECT id, topic_name, tests  FROM tables.topic""")
    for topic_info in cursor:
        result.append({
            "type": "topic",
            "topic_id": topic_info[0],
            "name": topic_info[1]
        })
        for test_id in topic_info[2]:
            cursor.execute(f"""SELECT test_name FROM tables.test WHERE id = {test_id}""")
            result.append({
                "type": "topicTest",
                "test_id": test_id,
                "name": cursor.fetchall()[0][0]
            })
    return json.dumps(result)


@app.route("/topics")
def topics():
    result = []
    cursor = conn.cursor()
    cursor.execute("""SELECT id, topic_name, icon  FROM tables.topic""")
    for topic_info in cursor:
        result.append({
            "topic_id": topic_info[0],
            "name": topic_info[1],
            "icon": topic_info[2]
        })
    return json.dumps(result)


@app.route("/session_id")
def session_id():
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM tables.session WHERE ip = '{request.remote_addr}'")
    session_id = cursor.fetchall()
    secret_key = str(
        hashlib.sha256((str(datetime.datetime.now()) + str(session_id)).encode()).hexdigest())
    if len(session_id) != 0:
        session_id = session_id[0][0]
        cursor.execute(
            f'''UPDATE tables.session SET secret_key = '{secret_key}', 
            user_id = null WHERE id = {session_id}''')
        conn.commit()
        cursor.close()
        return {"session_id": session_id, "secret_key": secret_key}

    cursor.execute('SELECT MAX(id) FROM tables.session')
    session_id = cursor.fetchall()
    if len(session_id) != 0:
        session_id = session_id[0][0] + 1
    else:
        session_id = 0
    cursor.execute(
        f'''INSERT INTO tables.session(id, ip, secret_key) VALUES ({session_id}, '{request.remote_addr}', '{secret_key}')''')
    conn.commit()
    cursor.close()
    return {"session_id": session_id, "secret_key": secret_key}


@app.route("/check_data")
def check_auth_data():
    auth_data_dict = request.args.to_dict()
    print(auth_data_dict)
    if auth_data_dict["session_id"] == "null":
        return "Please log in with app"
    auth_data = "\n".join(
        sorted([f"{key}={data}" for key, data in auth_data_dict.items() if
                key != "hash" and key != "session_id"]))
    # print(auth_data, request.args.to_dict()["hash"])
    SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode('utf-8'))
    print(hmac.new(SECRET_KEY.digest(), msg=bytearray(auth_data, 'utf-8'),
                   digestmod=hashlib.sha256).hexdigest())
    if (hmac.new(SECRET_KEY.digest(), msg=bytearray(auth_data, 'utf-8'),
                 digestmod=hashlib.sha256).hexdigest() == auth_data_dict["hash"]):
        auth_data_dict.pop("hash")
        cursor = conn.cursor()
        cursor.execute(f"SELECT id FROM tables.session WHERE id = {auth_data_dict['session_id']}")
        if len(cursor.fetchall()) == 0:
            cursor.close()
            return "Попробуйте снова перейти по ссылке в приложении"
        cursor.execute(f"SELECT id FROM tables.users WHERE id = {auth_data_dict['id']}")
        if len(cursor.fetchall()) == 0:
            print(auth_data_dict)
            cursor.execute(
                f'''INSERT INTO tables.users({", ".join(auth_data_dict.keys())}) VALUES ({", ".join([repr(value) for key, value in auth_data_dict.items()])})''')
            cursor.execute(
                f'UPDATE tables.session SET user_id = {auth_data_dict["id"]} WHERE id = {auth_data_dict["session_id"]}')
            cursor.execute(
                f'''INSERT INTO tables.user_stats(user_id) VALUES ({auth_data_dict["id"]})''')
            conn.commit()
            cursor.close()
            return f"Вы успешно зарегестрированы"
        else:
            cursor.execute(
                f'''UPDATE tables.users SET 
                {", ".join([f"{key}={repr(data)}" for key, data in auth_data_dict.items()
                            if key != "id"])} 
                WHERE id = {auth_data_dict["id"]}''')
            cursor.execute(
                f'UPDATE tables.session SET user_id = {auth_data_dict["id"]} WHERE id = {auth_data_dict["session_id"]}')
            conn.commit()
            cursor.close()
            return f"Вы успешно вошли"
    else:
        return "Telegram передал нам плохие данные, попробуйте снова " \
               "пройти операцию, авторизации через приложение"


# @app.route('/tauth/<int:session_id>')
# def telegram_auth(session_id: int):
#     return render_template("telegram_auth.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25565)
