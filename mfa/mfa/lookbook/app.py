from flask import Flask, render_template, request, jsonify
from jinja2 import Environment, PackageLoader
from sqlalchemy import extract
from ..models import Comment, Post, db_session

import calendar
import math
import urlparse

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


def album(url):
    url, fragment = urlparse.urldefrag(url)
    if url.endswith("/"):
        url = url[:-1]
    return url + "/embed"
env.filters["album"] = album


def number_to_month(i, abbr=False):
    if abbr:
        return calendar.month_abbr[i]
    return calendar.month_name[i]
env.filters["number_to_month"] = number_to_month


def paginate(query, page, per_page=15):
    total_pages = int(math.ceil(query.count()/float(per_page)))
    if page > total_pages or page < 1:
        return [], 0
    return query[(page-1)*per_page:page*per_page], page + 1


@app.route("/posts/<int:post_id>/", methods=["GET"])
@app.route("/", methods=["GET"])
def index(post_id=None):
    if post_id:
        query = Comment.query.filter(Comment.post_id == post_id).order_by("-point")
    else:
        query = Comment.query.order_by("-point")
    comments, next_page = paginate(query, request.args.get("page", 1, type=int))
    if "ajax" in request.args:
        return jsonify(
            comments=render_template(env.get_template('tiles.html'), comments=comments),
            next_page=next_page
        )
    return render_template(env.get_template("index.html"),
                           comments=comments)


@app.route("/archive/")
def archive():
    archive = (db_session.query(extract("year", Post.timestamp).label("year"),
                                extract("month", Post.timestamp).label("month"))
                         .group_by("year", "month")
                         .order_by("-year", "-month"))

    return render_template(env.get_template("archive.html"),
                           archive=archive)


@app.route("/archive/<int:year>/<int:month>/")
def month_archive(year, month):
    posts = Post.query.filter(extract("year", Post.timestamp) == year,
                                       extract("month", Post.timestamp) == month)

    return render_template(env.get_template("month_archive.html"),
                           posts=posts, year=year, month=month)


@app.teardown_appcontext
def shutdown_session():
    db_session.remove()
