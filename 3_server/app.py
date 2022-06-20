from flask import Flask, render_template
import psycopg2

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


@app.route("/get_session_id")
def get_session_id():
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(id) FROM tables.session')

    session_id = cursor.fetchall()[0][0] + 1
    cursor.execute(f'INSERT INTO tables.session(id) VALUES ({session_id})')
    conn.commit()
    cursor.close()
    return str(session_id)


@app.route('/tauth/<int:session_id>')
def telegram_auth(session_id: int):
    return render_template("telegram_auth.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25565)
