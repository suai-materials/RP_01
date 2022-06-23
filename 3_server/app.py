import datetime
import hashlib
import hmac
import json
from random import sample, choice, randrange

import psycopg2
from flask import Flask, request, render_template
from sympy import *

DOMAIN = "http://api.pank.su:25565/"
BOT_TOKEN = "5472884845:AAGh_XXz2Dlrl2hIcrRF7cWqVqT1C4ZzQB8"
conn = psycopg2.connect(dbname='integrals', user='postgres',
                        password='200tdhj', host='api.pank.su')
# cursor = conn.cursor()
# cursor.execute('SELECT * FROM tables.topic')
# for row in cursor:
#     print(row)
app = Flask(__name__)


def get_user_id_by_token(token):
    cursor = conn.cursor()
    cursor.execute(f"""SELECT id FROM tables.users WHERE token = '{token}'""")
    user_id = cursor.fetchall()[0][0]
    cursor.close()
    return user_id


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
    user_id: int
    try:
        token = request.headers['Authorization']
        user_id = get_user_id_by_token(token)
    except Exception:
        return "token not found", 401
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM tables.test WHERE id = {test_id}""")
    test = cursor.fetchall()[0]
    test_data = sample(test[2], test[5])
    test_data[0]["test_id"] = test_id
    cursor.execute(f"""UPDATE tables.user_stats SET test_now = %s WHERE user_id = {user_id}""",
                   [json.dumps(test_data)])
    conn.commit()
    cursor.close()
    return render_template("test.html", name=test[1], test_data=test_data, user_id=user_id)


@app.route("/tests")
def tests():
    result = []
    user_id: int
    try:
        token = request.headers['Authorization']
        user_id = get_user_id_by_token(token)
    except Exception:
        return "token not found", 401
    cursor = conn.cursor()
    cursor.execute(f"""SELECT grades FROM tables.user_stats WHERE user_id = {user_id}""")
    grades: list = cursor.fetchall()[0][0]
    cursor.execute("""SELECT id, topic_name, tests  FROM tables.topic""")
    for topic_info in cursor:
        result.append({
            "type": "topic",
            "topic_id": topic_info[0],
            "name": topic_info[1]
        })
        for test_id in topic_info[2]:
            cursor.execute(f"""SELECT test_name, attempts FROM tables.test WHERE id = {test_id}""")
            test_data = cursor.fetchall()[0]
            grade = [grade for grade in grades if grade["test_id"] == test_id]
            result.append({
                "type": "topicTest",
                "test_id": test_id,
                "name": test_data[0],
                "grade": 0 if len(grade) == 0 else grade[0]["grade"],
                "attempts": test_data[1] if len(grade) == 0 else grade[0]["attempts"]
            })

    cursor.close()
    return json.dumps(result)


@app.route("/topics")
def topics():
    result = []
    cursor = conn.cursor()
    cursor.execute("""SELECT id, topic_name, icon  FROM tables.topic SORT ORDER BY id""")
    for topic_info in cursor:
        result.append({
            "topic_id": topic_info[0],
            "name": topic_info[1],
            "url": DOMAIN + "topic/" + str(topic_info[0]),
            "topic_icon": topic_info[2]
        })
    return json.dumps(result)


@app.route("/topic/<topic_id>")
def read_topic(topic_id):
    topic_id = int(topic_id)
    cursor = conn.cursor()
    cursor.execute(f"SELECT topic_name, filename f FROM tables.topic WHERE id = {topic_id} ORDER BY id")
    topic_data = cursor.fetchall()[0]
    with open(fr"C:\Users\pankSU\Documents\RP_01\3_server\data\topics\_html\{topic_data[1]}", "r",
              encoding="utf-8") as content:
        return render_template("topic.html", content=content.read(), name=topic_data[0])


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


def get_grade(percent):
    if percent > 0.87:
        return 5
    elif percent > 0.72:
        return 4
    elif percent > 0.57:
        return 3
    elif percent > 0.57:
        return 2


@app.route("/test_data/<int:user_id>", methods=["POST"])
def check_test_data(user_id):
    cursor = conn.cursor()
    cursor.execute(f"""SELECT test_now FROM tables.user_stats WHERE user_id = {user_id}""")
    test_data = cursor.fetchall()[0][0]
    result = test_data.copy()
    points = 0
    for i, question in enumerate(test_data):
        result[i]["user_answer"] = request.form[(str(i + 1))]
        if question["question_type"] == "one_answer":
            result[i]["is_correct"] = question["answers"][int(request.form[(str(i + 1))]) - 1] == \
                                      question["correct"]

        elif question["question_type"] == "entering":
            result[i]["is_correct"] = request.form[(str(i + 1))].lower() == \
                                      question["correct"]
        elif question["question_type"] == "multiple_answers":
            user_answers = [question["answers"][int(el) - 1] for el in
                            request.form.getlist(str(i + 1))]
            result[i]["user_answer"] = [el for el in request.form.getlist(str(i + 1))]
            result[i]["is_correct"] = set(user_answers) == set(question["correct"])
        if result[i]["is_correct"]:
            points += 1
    grade = get_grade(points / len(test_data))
    cursor.execute(f"SELECT grades, test_now FROM tables.user_stats WHERE user_id = {user_id}")
    grades, test_now = cursor.fetchall()[0]
    is_found = False
    average_grade = 0

    for i in range(len(grades)):
        if test_now[0]["test_id"] == grades[i]["test_id"]:
            if grades[i]["attempts"] > 0:
                grades[i]["attempts"] -= 1
                grades[i]["grade"] = grade
            is_found = True
        average_grade += grades[i]["grade"]
    if not is_found:
        cursor.execute(f"SELECT attempts FROM tables.test WHERE id = {test_now[0]['test_id']}")
        grades.append(
            {"attempts": cursor.fetchall()[0][0] - 1, "test_id": test_now[0]["test_id"],
             "grade": grade})
    average_grade /= len(grades)
    cursor.execute(f"UPDATE tables.user_stats SET grades = %s, average_grade = {average_grade},"
                   f" test_now = '[]'", [json.dumps(grades)])
    conn.commit()
    cursor.close()
    print(result)
    return render_template("test_result.html", test_data=result, grade=grade)


@app.route("/close_test/", methods=["POST"])
def close_test():
    user_id: int
    try:
        token = request.headers['Authorization']
        user_id = get_user_id_by_token(token)
    except Exception:
        return "token not found", 401
    cursor = conn.cursor()
    cursor.execute(f"SELECT grades, test_now FROM tables.user_stats WHERE user_id = {user_id}")
    grades, test_now = cursor.fetchall()[0]
    is_found = False
    average_grade = 0
    for i in range(len(grades)):
        average_grade += grades["grade"]
        if test_now[0]["test_id"] == grades[i]["test_id"]:
            if grades[i]["attempts"] > 0:
                grades[i]["attempts"] -= 1
            is_found = True
    if not is_found:
        cursor.execute(f"SELECT attempts FROM tables.test WHERE id = {test_now[0]['test_id']}")
        grades.append(
            {"attempts": cursor.fetchall()[0][0] - 1, "test_id": test_now[0]["test_id"], "grade": 0})
    average_grade /= len(grades)
    cursor.execute(f"UPDATE tables.user_stats SET grades = %s, average_grade = {average_grade},"
                   f" test_now = '[]'", [json.dumps(grades)])
    conn.commit()
    cursor.close()
    return "ok"


@app.route("/generate_integral/")
def generate_integral():
    # user_id: int
    # try:
    #     token = request.headers['Authorization']
    #     user_id = get_user_id_by_token(token)
    # except Exception:
    #     return "token not found", 401
    x = symbols("x")
    a, b, c, d = var("a b c d")
    a = randrange(0, 12)
    b = randrange(0, 12)
    c = randrange(-10, 10)
    d = randrange(c, 20)
    integrals_array = [Integral(a * x, (x, c, d)), Integral(x, (x, c, d)),
                       Integral(a * x ** b, (x, c, d)),
                       Integral(x ** b, (x, c, d)), Integral(E ** x, (x, 0, 1)),
                       Integral(a * E ** x, (x, 0, 1))]
    i1 = choice(integrals_array)
    a = randrange(0, 10)
    b = randrange(0, 10)
    c = randrange(-10, 12)
    d = randrange(c, 22)
    integrals_array = [Integral(a * x, (x, c, d)), Integral(x, (x, c, d)),
                       Integral(a * x ** b, (x, c, d)),
                       Integral(x ** b, (x, c, d)), Integral(E ** x, (x, 0, 1)),
                       Integral(a * E ** x, (x, 0, 1))]
    i2 = choice(integrals_array)
    funcs = [lambda i1, i2: i1 + i2, lambda i1, i2: i1 - i2, lambda i1, i2: i1, lambda i1, i2: i2]
    f = choice(funcs)(i1, i2)
    print(f.doit())
    return render_template("generator.html", latex_formul=latex(f))


# @app.route('/tauth/<int:session_id>')
# def telegram_auth(session_id: int):
#     return render_template("telegram_auth.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25565)
