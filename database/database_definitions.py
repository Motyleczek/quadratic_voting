from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
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

User = Base.classes.User
Role = Base.classes.Role
UserRole = Base.classes.UserRole
UserVote = Base.classes.UserVote
UserVoteDetail = Base.classes.UserVoteDetail
Vote = Base.classes.Vote
VoteDetail = Base.classes.VoteDetail









