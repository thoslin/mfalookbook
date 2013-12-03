from flask import Flask, render_template
from jinja2 import Environment, PackageLoader
from sqlalchemy import extract
from ..models import Session, Comment, Post

import calendar

app = Flask(__name__)
env = Environment(loader=PackageLoader('mfa.lookbook', 'templates'))


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


def number_to_month(i, abbr=False):
    if abbr:
        return calendar.month_abbr[i]
    return calendar.month_name[i]
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


@app.route("/archive/<int:year>/<int:month>/")
def month_archive(year, month):
    session = Session()
    posts = session.query(Post).filter(extract("year", Post.timestamp) == year,
                                       extract("month", Post.timestamp) == month)
    session.close()

    return render_template(env.get_template("month_archive.html"),
                           posts=posts, year=year, month=month)