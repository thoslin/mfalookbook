from flask import Flask, render_template, request
from jinja2 import Environment, PackageLoader
from sqlalchemy import extract
from ..models import Session, Comment, Post

import calendar
import math

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


def paginate(query, page, per_page=15):
    total_pages = int(math.ceil(query.count()/float(per_page)))
    if not page:
        page = 1
    page = int(page)
    if page > total_pages or page < 1:
        return []
    return query[(page-1)*per_page:page*per_page]


@app.route("/posts/<int:post_id>/")
@app.route("/")
def index(post_id=None):
    session = Session()
    if post_id:
        comments = (session.query(Comment).filter(Post.id == post_id)
                           .order_by("-point"))
    else:
        comments = session.query(Comment).order_by("-point")
    session.close()
    return render_template(env.get_template("index.html"),
                           comments=paginate(comments, request.args.get("page")))


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