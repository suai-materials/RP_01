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

app = Flask(__name__)


def get_user_id_by_token(token):
    """Получение id пользователя по его токену"""
    cursor = conn.cursor()
    cursor.execute(f"""SELECT id FROM tables.users WHERE token = '{token}'""")
    user_id = cursor.fetchall()[0][0]
    cursor.close()
    return user_id


@app.route('/', methods=['GET'])
def dont_be_here():
    """Заглушка на обычный экран, чтобы никто не заходил :)"""
    return 'Вас не должно быть здесь'


@app.route("/check_auth", methods=['POST'])
def check_auth():
    """Проверяет, вошёл ли пользователь, если вошёл, то выдаём токен"""
    data = request.get_json()
    cursor = conn.cursor()
    cursor.execute(f"""SELECT user_id FROM tables.session 
    WHERE ip = '{request.remote_addr}' AND id = {data['session_id']} AND 
    secret_key = '{data['secret_key']}' """)
    user_id = cursor.fetchall()
    if len(user_id) != 0:
        user_id = user_id[0][0]
        # Если id пользователя не указан,
        # значит пользователь не зашёл и просим программу продолжать ждать
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
    """Получение теста по id"""
    user_id: int
    try:
        token = request.headers['Authorization']
        user_id = get_user_id_by_token(token)
    except Exception:
        return "token not found", 401
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM tables.test WHERE id = {test_id}""")
    test = cursor.fetchall()[0]
    # test[2] - вопросы, test[5] - их количество
    test_data = sample(test[2], test[5])
    test_data[0]["test_id"] = test_id
    cursor.execute(f"""UPDATE tables.user_stats SET test_now = %s WHERE user_id = {user_id}""",
                   [json.dumps(test_data)])
    conn.commit()
    cursor.close()
    return render_template("test.html", name=test[1], test_data=test_data, user_id=user_id)


@app.route("/tests")
def tests():
    """Получение списка тестов в отформатированном виде"""
    # result = response
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
    cursor.execute("""SELECT id, topic_name, tests  FROM tables.topic ORDER BY id""")
    for topic_info in cursor.fetchall():
        # Если прикреплённых тестов больше 0
        if len(topic_info[2]) != 0:
            result.append({
                "type": "topic",
                "topic_id": topic_info[0],
                "name": topic_info[1]
            })
            size_now = len(result)
            grade_topic = 0
            for test_id in topic_info[2]:
                cursor.execute(
                    f"""SELECT test_name, attempts FROM tables.test WHERE id = {test_id}""")
                test_data = cursor.fetchall()[0]
                grade = [grade_data for grade_data in grades if grade_data["test_id"] == test_id]
                result.append({
                    "type": "topicTest",
                    "test_id": test_id,
                    "name": test_data[0],
                    "grade": 0 if len(grade) == 0 else grade[0]["grade"],
                    "attempts": test_data[1] if len(grade) == 0 else grade[0]["attempts"]
                })
                grade_topic += result[-1]["grade"]
            result[size_now - 1]["grade"] = grade_topic / (len(result) - size_now)
    cursor.close()
    return json.dumps(result)


@app.route("/topics")
def topics():
    """Список тем в отформатированном виде"""
    result = []
    cursor = conn.cursor()
    cursor.execute("""SELECT id, topic_name, icon  FROM tables.topic ORDER BY id""")
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
    """Получение темы по id"""
    topic_id = int(topic_id)
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT topic_name, filename f FROM tables.topic WHERE id = {topic_id} ORDER BY id")
    topic_data = cursor.fetchall()[0]
    with open(fr"C:\Users\pankSU\Documents\RP_01\3_server\data\topics\_html\{topic_data[1]}", "r",
              encoding="utf-8") as content:
        return render_template("topic.html", content=content.read(), name=topic_data[0])


@app.route("/session_id")
def session_id():
    """Получение номера сессии"""
    cursor = conn.cursor()
    # Получение сессии по ip
    cursor.execute(f"SELECT id FROM tables.session WHERE ip = '{request.remote_addr}'")
    session_id = cursor.fetchall()
    secret_key = str(
        hashlib.sha256((str(datetime.datetime.now()) + str(session_id)).encode()).hexdigest())
    # Если сессия была найдена, то отправляем новый секретный код и сбрасываем id пользователя
    if len(session_id) != 0:
        session_id = session_id[0][0]
        cursor.execute(
            f'''UPDATE tables.session SET secret_key = '{secret_key}', 
            user_id = null WHERE id = {session_id}''')
        conn.commit()
        cursor.close()
        return {"session_id": session_id, "secret_key": secret_key}
    # Если была найдена, то создаём session и возвращаем её данные
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
    """Проверка данных, которые прислал телеграм, то есть авторизация пользователя"""
    auth_data_dict = request.args.to_dict()
    if auth_data_dict["session_id"] == "null":
        return "Please log in with app"
    auth_data = "\n".join(
        sorted([f"{key}={data}" for key, data in auth_data_dict.items() if
                key != "hash" and key != "session_id"]))
    SECRET_KEY = hashlib.sha256(BOT_TOKEN.encode('utf-8'))
    if (hmac.new(SECRET_KEY.digest(), msg=bytearray(auth_data, 'utf-8'),
                 digestmod=hashlib.sha256).hexdigest() == auth_data_dict["hash"]):
        auth_data_dict.pop("hash")
        cursor = conn.cursor()
        cursor.execute(f"SELECT id FROM tables.session WHERE id = {auth_data_dict['session_id']}")
        if len(cursor.fetchall()) == 0:
            cursor.close()
            return "Попробуйте снова перейти по ссылке в приложении"
        cursor.execute(f"SELECT id FROM tables.users WHERE id = {auth_data_dict['id']}")
        # Если пользователь не зарегистрирован, то идёт добавление всех его данных
        if len(cursor.fetchall()) == 0:
            cursor.execute(
                f'''INSERT INTO tables.users({", ".join(auth_data_dict.keys())}) VALUES ({", ".join([repr(value) for key, value in auth_data_dict.items()])})''')
            cursor.execute(
                f'UPDATE tables.session SET user_id = {auth_data_dict["id"]} WHERE id = {auth_data_dict["session_id"]}')
            cursor.execute(
                f'''INSERT INTO tables.user_stats(user_id) VALUES ({auth_data_dict["id"]})''')
            conn.commit()
            cursor.close()
            return f"Вы успешно зарегистрированы"
        else:
            cursor.execute(
                f'''UPDATE tables.users SET 
                {", ".join([f"{key}={repr(data)}" for key, data in auth_data_dict.items()
                            if key != "id"])} 
                WHERE id = {auth_data_dict["id"]}''')
            cursor.execute(f'''UPDATE tables.session SET user_id = {auth_data_dict["id"]}
             WHERE id = {auth_data_dict["session_id"]}''')
            conn.commit()
            cursor.close()
            return f"Вы успешно вошли"
    else:
        return "Telegram передал нам плохие данные, попробуйте снова " \
               "пройти операцию, авторизации через приложение"


def get_grade(percent):
    """Получение оценки по проценту"""
    if percent > 0.87:
        return 5
    elif percent > 0.72:
        return 4
    elif percent > 0.57:
        return 3
    else:
        return 2


@app.route("/test_data/<int:user_id>", methods=["POST"])
def check_test_data(user_id):
    """Проверка теста"""
    cursor = conn.cursor()
    cursor.execute(f"""SELECT test_now FROM tables.user_stats WHERE user_id = {user_id}""")
    test_data = cursor.fetchall()[0][0]
    result = test_data.copy()
    points = 0
    for i, question in enumerate(test_data):
        result[i]["user_answer"] = request.form[(str(i + 1))]
        # Проверка ответов в отличчи от типов вопроса
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
    # Выставление оценки
    for i in range(len(grades)):
        if test_now[0]["test_id"] == grades[i]["test_id"]:
            if grades[i]["attempts"] > 0:
                grades[i]["attempts"] -= 1
                if grades[i]["grade"] > grade:
                    grades[i]["grade"] = grade
            is_found = True
        average_grade += grades[i]["grade"]
    # Если оценки не найдены
    if not is_found:
        cursor.execute(f"SELECT attempts FROM tables.test WHERE id = {test_now[0]['test_id']}")
        grades.append(
            {"attempts": cursor.fetchall()[0][0] - 1, "test_id": test_now[0]["test_id"],
             "grade": grade})
        average_grade += grade
    average_grade /= len(grades)
    cursor.execute(f"UPDATE tables.user_stats SET grades = %s, average_grade = {average_grade},"
                   f" test_now = '[]'", [json.dumps(grades)])
    conn.commit()
    cursor.close()
    return render_template("test_result.html", test_data=result, grade=grade)


@app.route("/close_test/", methods=["POST"])
def close_test():
    """Закрытие теста"""
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
    # Код схож, с заполнением результата по выполнению теста, но без выставления оценки
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


def generate_one_integral() -> Integral:
    """Генерирование одного интеграла"""
    x = symbols("x")
    a = randrange(0, 12)
    b = randrange(0, 5)
    c = randrange(-10, 10)
    d = randrange(c, 20)
    integrals_array = [Integral(a * x, (x, c, d)), Integral(x, (x, c, d)),
                       Integral(a * x ** b, (x, c, d)),
                       Integral(x ** b, (x, c, d)), Integral(a * b, (x, c, d)),
                       Integral(a + b, (x, c, d))]
    return choice(integrals_array)


@app.route("/generate_integral/")
def generate_integral():
    """Генерирование выражение с интегралом"""
    user_id: int
    try:
        token = request.headers['Authorization']
        user_id = get_user_id_by_token(token)
    except Exception:
        return "token not found", 401
    answer = 0
    while answer == 0:
        i1 = generate_one_integral()
        i2 = generate_one_integral()
        # Действия с интегралами
        funcs = [lambda i1, i2: i1 + i2, lambda i1, i2: i1 - i2, lambda i1, i2: i1,
                 lambda i1, i2: i2]
        f = choice(funcs)(i1, i2)
        cursor = conn.cursor()
        answer = f.doit()
    cursor.execute(
        f"""UPDATE tables.user_stats SET generated_answer = {round(float(answer), 2)} WHERE user_id = {user_id}""")
    conn.commit()
    cursor.close()
    return render_template("generator.html", latex_formul=latex(f))


@app.route("/check_generate_integral/", methods=["POST"])
def check_generate_data():
    """Проверка ответа на интеграл"""
    user_id: int
    try:
        token = request.headers['Authorization']
        user_id = get_user_id_by_token(token)
    except Exception:
        return "token not found", 401
    cursor = conn.cursor()
    cursor.execute(f"""SELECT generated_answer FROM tables.user_stats WHERE user_id = {user_id}""")
    if cursor.fetchall()[0][0] == request.json["answer"]:
        cursor.execute(f"""UPDATE tables.user_stats SET generator_correct =  generator_correct + 1, 
        generator_count =  generator_count + 1 WHERE user_id = {user_id}""")
        conn.commit()
        cursor.close()
        return {"is_correct": True}
    else:
        cursor.execute(f"""UPDATE tables.user_stats SET
                generator_count =  generator_count + 1 WHERE user_id = {user_id}""")
        conn.commit()
        cursor.close()
        return {"is_correct": False}


@app.route("/user_data/")
def user_data():
    """Получение информации о пользователе"""
    user_id: int
    try:
        token = request.headers['Authorization']
        user_id = get_user_id_by_token(token)
    except Exception:
        return "token not found", 401
    cursor = conn.cursor()
    cursor.execute(
        f"""SELECT first_name, last_name, photo_url FROM tables.users WHERE id = {user_id}""")
    # переменная для результатов запросов
    res = cursor.fetchall()[0]
    # result = response
    result = {
        "first_name": res[0],
        "last_name": res[1],
        "photo_url": res[2]
    }
    cursor.execute(f"""SELECT grades, average_grade, generator_correct, generator_count 
        FROM tables.user_stats WHERE user_id = {user_id}""")
    res = cursor.fetchall()[0]
    result["grades"] = res[0]
    result["average_grade"] = res[1]
    result["generator_correct"] = res[2]
    result["generator_count"] = res[3]
    cursor.close()
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25565)
