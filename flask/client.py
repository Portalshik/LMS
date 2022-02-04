from flask import Flask
from flask import url_for

app = Flask(__name__)


@app.route('/')
def empty():
    return "Миссия Колонизация Марса"


@app.route('/index')
def index():
    return "И на Марсе будут яблони цвести!"


@app.route("/promotion")
def promotion():
    return """Человечество вырастает из детства.<br>

Человечеству мала одна планета.<br>

Мы сделаем обитаемыми безжизненные пока планеты.<br>

И начнем с Марса!<br>

Присоединяйся!<br>"""


@app.route("/image_mars")
def image_mars():
    return f"""<h2>Wait Us, Mars!</h2><img src={url_for('static', filename='img/mars.png')}>
<br><p>That's What It Is, The Red Planet.</p>"""


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
