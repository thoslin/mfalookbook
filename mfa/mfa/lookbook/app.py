from flask import Flask, render_template
from ..models import Session, Comment


app = Flask(__name__)


@app.route("/")
def index():
    session = Session()
    comments = session.query(Comment).all()[:15]
    session.close()
    return render_template("index.html", comments=comments)


@app.route("/archive")
def archive():
    return render_template("archive.html")