from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/index/<title>")
def index(title):
    return render_template('index.html', title=title)


@app.route("/list_prof")
def list_prof():
    prof_list = [
        "Врач",
        "Инженер",
        "Механик",
        "Капитан Корабля"
    ]
    return render_template('list_prof.html', list=prof_list)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
