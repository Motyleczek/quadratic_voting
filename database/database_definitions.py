from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
import os


load_dotenv()

db_link = f'mysql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}'
eng = create_engine(db_link)
Session = sessionmaker(eng)
db_con = eng.connect()

meta = MetaData()
meta.reflect(bind=eng)

Base = automap_base()
Base.prepare(eng, reflect=True)

Base1 = declarative_base()

class User(Base1):
    __tablename__ = "User"

    id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    username = Column(String(30), nullable = False)
    password = Column(String(180), nullable = False)
    email = Column(String(30), nullable = False)
    createdon = Column(DateTime, nullable = False)
    createdby = Column(String(15), nullable = False)
    lastupdatedon = Column(DateTime, nullable = False)
    lastupdatedby = Column(String(15), nullable = False)
    is_active = Column(Boolean, nullable = False)

    is_authenticated = False
    is_anonymous = False
    is_author = False
    # is_active = active

    def get_id(self):
        return str(self.id)


# User = Base.classes.User
Role = Base.classes.Role
UserRole = Base.classes.UserRole
UserVote = Base.classes.UserVote
UserVoteDetail = Base.classes.UserVoteDetail
Vote = Base.classes.Vote
VoteDetail = Base.classes.VoteDetail









