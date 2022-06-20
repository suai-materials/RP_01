import datetime
import hashlib
import hmac

import psycopg2
from flask import Flask, request

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
        token = str(hashlib.sha256((str(datetime.datetime.now()) + BOT_TOKEN).encode()).hexdigest())
        cursor.execute(
            f'''UPDATE tables.users SET token = '{token}' WHERE id = {user_id}''')
        conn.commit()
        return token
    else:
        return "data invalid", 401



@app.route("/get_session_id")
def get_session_id():
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM tables.session WHERE ip = '{request.remote_addr}'")
    session_id = cursor.fetchall()
    secret_key = str(hashlib.sha256(str(datetime.datetime.now()).encode()).hexdigest())
    if len(session_id) != 0:
        session_id = session_id[0][0]
        cursor.execute(
            f'''UPDATE tables.session SET secret_key = '{secret_key}' WHERE id = {session_id}''')
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
    if (hmac.new(SECRET_KEY.digest(), msg=bytearray(auth_data, 'utf-8'),
                 digestmod=hashlib.sha256).hexdigest() == auth_data_dict["hash"]):
        auth_data_dict.pop("hash")
        cursor = conn.cursor()
        cursor.execute(f"SELECT id FROM tables.session WHERE id = {auth_data_dict['session_id']}")
        if len(cursor.fetchall()) == 0:
            return "Попробуйте снова перейти по ссылке в приложении"
        cursor.execute(f"SELECT id FROM tables.users WHERE id = {auth_data_dict['id']}")
        if len(cursor.fetchall()) == 0:
            print(auth_data_dict)
            cursor.execute(
                f'''INSERT INTO tables.users({", ".join(auth_data_dict.keys())}) VALUES ({", ".join([value if "id" in key or key == "auth_date" else f"""'{value}'""" for key, value in auth_data_dict.items()])})''')
            cursor.execute(
                f'UPDATE tables.session SET is_auth = true, user_id = {auth_data_dict["id"]} WHERE id = {auth_data_dict["session_id"]}')
            conn.commit()
            return f"Вы успешно зарегестрированы"
        else:
            cursor.execute(
                f'UPDATE tables.users SET auth_date = {auth_data_dict["auth_date"]}, session_id = {auth_data_dict["session_id"]} WHERE id = {auth_data_dict["id"]}')
            cursor.execute(
                f'UPDATE tables.session SET is_auth = true, user_id = {auth_data_dict["id"]} WHERE id = {auth_data_dict["session_id"]}')
            conn.commit()
            return f"Вы успешно вошли"
    else:
        return "Telegram передал нам плохие данные, попробуйте снова пройти операцию авторизации через приложение"


# @app.route('/tauth/<int:session_id>')
# def telegram_auth(session_id: int):
#     return render_template("telegram_auth.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25565)
