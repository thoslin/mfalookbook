from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker, scoped_session

import datetime


engine = create_engine('sqlite:////tmp/mfa.db', echo=True)
Session = sessionmaker(bind=engine)
db_session = scoped_session(Session)

Base = declarative_base()
Base.query = db_session.query_property()


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    permalink = Column(String)
    title = Column(String)
    timestamp = Column(DateTime)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id",
                                         onupdate="CASCADE", ondelete="CASCADE"))
    permalink = Column(String)
    username = Column(String)
    point = Column(Integer)
    images = Column(PickleType)

    post = relationship("Post", backref=backref("comments", lazy="dynamic"))

    def __repr__(self):
        return "<%s>:%s" % (self.username, self.permalink)


def create_comment(session, **kwargs):
    """
    >>> item = {
    ...     'images': [(u'http://i.imgur.com/KZ9431n.jpg', u'Off-white shirt and olive slacks.')],
    ...     'permalink': u'http://www.reddit.com/r/malefashionadvice/comments/1rpung/waywt_nov_29th/cdpnyn0',
    ...     'point': 0,
    ...     'post_timestamp': u'2013-11-29T17:00:16+00:00',
    ...     'post_title': u'WAYWT - Nov. 29th',
    ...     'post_url': 'http://www.reddit.com/r/malefashionadvice/comments/1rpung/waywt_test/',
    ...     'username': u'djhs'
    ... }

    >>> session = Session()
    >>> create_comment(session, **item)
    >>> post = session.query(Post).filter_by(permalink=item["post_url"]).first()
    >>> create_comment(session, **item)
    >>> session.delete(post)
    >>> session.commit()
    >>> session.close()
    """
    post = session.query(Post).filter_by(permalink=kwargs["post_url"]).first()
    if not post:
        timestamp = datetime.datetime.strptime(kwargs["post_timestamp"][:-6], "%Y-%m-%dT%H:%M:%S")
        post = Post(title=kwargs["post_title"], permalink=kwargs["post_url"],
                    timestamp=timestamp)
        session.add(post)

    comment = Comment(post=post, permalink=kwargs["permalink"], username=kwargs["username"],
                      point=kwargs["point"], images=kwargs["images"])
    session.add(comment)
    session.commit()
    session.close()


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import doctest
    doctest.testmod()