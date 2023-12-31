from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    intro = db.Column(db.String(300), nullable = False)
    title = db.Column(db.String(100), nullable = False)
    text = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return "<Article %r>" % self.id


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/create-article", methods = ["POST","GET"])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(text = text, title = title, intro = intro)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect("/results")
        except:
            return "error while adding article into data base"
        
    else:
        return render_template("create-article.html")


@app.route("/results")
def results():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("results.html", articles = articles)


@app.route("/results/<int:id>")
def detail(id):
    article = Article.query.get(id)
    return render_template("details.html", article = article)


@app.route("/results/<int:id>/delete")
def article_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/results")
    except:
        return "Error while remove from data base"


if __name__ == "__main__":
    app.run(debug = True)