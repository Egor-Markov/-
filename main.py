from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Подключение SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///articles.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Создание db
db = SQLAlchemy(app)


# Создание таблицы
class Article(db.Model):
    # id
    id = db.Column(db.Integer, primary_key=True)
    # Заголовок
    title = db.Column(db.String(100), nullable=False)
    # Содержание статьи
    text = db.Column(db.Text, nullable=False)

    # Вывод объекта и id
    def __repr__(self):
        return f"<Article {self.id}>"


@app.route("/")
def content():
    return render_template("index.html")


@app.route("/card")
def card():
    return render_template("new_article.html")


@app.route("/all_cards")
def all_cards():
    # Отображение всех статей
    cards = Article.query.order_by(Article.id).all()
    return render_template("viewing.html", cards=cards)


# Запуск страницы c картой
@app.route("/all_cards/<int:id>")
def article(id):
    card = Article.query.get(id)

    return render_template("article.html", card=card)


@app.route("/parse", methods=["GET", "POST"])
def parse():
    if request.method == "POST":
        url = request.form["url"]
        response = requests.get(url)
        bs = BeautifulSoup(response.text, "lxml")
        elements = bs.find_all("p")
        text = ""
        for el in elements:
            text += el.text.strip() + "\n"
        title = "Парсинг: " + url[:50]
        new_article = Article(title=title, text=text)
        db.session.add(new_article)
        db.session.commit()
        return redirect("/")
    return render_template("parsing.html")


@app.route("/writing", methods=["GET", "POST"])
def writing():
    if request.method == "POST":
        title = request.form["title"]
        text = request.form["text"]

        # Создание объкта для передачи в дб

        card = Article(title=title, text=text)

        db.session.add(card)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("writing.html")


if __name__ == "__main__":
    app.run(debug=True)
