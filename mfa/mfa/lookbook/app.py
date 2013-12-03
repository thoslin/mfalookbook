from flask import Flask, render_template
from jinja2 import Environment, PackageLoader
from sqlalchemy import extract
from ..models import Session, Comment, Post

import calendar

app = Flask(__name__)
env = Environment(loader=PackageLoader('mfa.lookbook', 'templates'))
month_abbr = dict((k, v) for k, v in enumerate(calendar.month_abbr))


def thumbnail(url, size="m"):
    """ Get thumbnail for imgur.com image """
    parts = url.rsplit(".", 1)
    if len(parts) == 2:
        _size = "%s." % size
        if "com" in parts[1]:
            return url + "%sjpg" % _size
        return _size.join(parts)
    return url
env.filters["thumbnail"] = thumbnail


def number_to_month(i):
    return month_abbr.get(i)
env.filters["number_to_month"] = number_to_month


@app.route("/")
def index():
    session = Session()
    comments = session.query(Comment).order_by("-point")[:15]
    session.close()
    return render_template(env.get_template("index.html"),
                           comments=comments)


@app.route("/archive/")
def archive():
    session = Session()
    archive = (session.query(extract("year", Post.timestamp).label("year"),
                             extract("month", Post.timestamp).label("month"))
                      .group_by("year", "month")
                      .order_by("-year", "-month"))
    session.close()

    return render_template(env.get_template("archive.html"),
                           archive=archive)
