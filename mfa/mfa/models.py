from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker


engine = create_engine('sqlite:////tmp/mfa.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    permalink = Column(String)
    title = Column(String)
    timestamp = Column(DateTime)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    permalink = Column(String)
    point = Column(Integer)
    images = Column(PickleType)

    post = relationship("Post", backref=backref("comments", lazy="dynamic"))


def init_db():
    Base.metadata.create_all(bind=engine)