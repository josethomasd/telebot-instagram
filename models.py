from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///mydatabase.db', echo=True)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    insta_id = Column(String, primary_key=True)
    username = Column(String)
    userid = Column(String)

    def __init__(self, insta_id, username, userid):
        self.insta_id = insta_id
        self.username = username
        self.userid = userid

    def __repr__(self):
       return "<User('%s','%s', '%s')>" % (self.insta_id, self.username, self.userid)


users_table = User.__table__
metadata = Base.metadata


if __name__ == "__main__":
    metadata.create_all(engine)

