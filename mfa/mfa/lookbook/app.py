from flask import Flask, render_template
from jinja2 import Environment, PackageLoader
from ..models import Session, Comment


app = Flask(__name__)
env = Environment(loader=PackageLoader('mfa.lookbook', 'templates'))


def thumbnail(url, size="m"):
    """ Get thumbnail for imgur.com image """
    parts = url.rsplit(".", 1)
    if len(parts) == 2:
        _size = "%s." % size
        return _size.join(parts)
    return url
env.filters["thumbnail"] = thumbnail


@app.route("/")
def index():
    session = Session()
    comments = session.query(Comment).order_by("-point")[:15]
    session.close()
    return render_template(env.get_template("index.html"),
                           comments=comments)


@app.route("/archive")
def archive():
    return render_template(env.get_template("archive.html"))