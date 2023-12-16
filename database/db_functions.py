from database.database_definitions import Session, User, UserVote, UserRole, UserVoteDetail, Vote, VoteDetail, Role, db_con, meta
from datetime import date, datetime
from typing import List, Dict

from sqlalchemy.schema import MetaData
import sqlalchemy


def insert_to_table(tablename: str, insert_data_lst: List[Dict[str, str]]):
    for data in insert_data_lst:
        db_con.execute(meta.tables[tablename].insert(data))


def get_user_login(session, username: str) -> User:
    return session.query(User).filter(User.username == username and User.is_active == 1).first()


def insert_new_user(session, username: str, password: str, email: str, user_role: str = None, createdby: str = None):
    createdby = createdby if createdby else 'System'
    createdon = datetime.now()
    active = True
    user = User(username = username, password = password, email = email, createdby = createdby, createdon = createdon, lastupdatedby = createdby, lastupdatedon = createdon, is_active = active)
    # try:
    session.add(user)
    session.commit()
    # except sqlalchemy.exc.IntegrityError:
    #     raise ValueError('Username or e-mail already exist')  # To można zmienić tak, żeby sie wyświetlał komunikat do użytkownika
    if user_role:
        roleid = session.query(Role.id).filter(Role.name == user_role and Role.active == 1).first()[0]
        userid = session.query(User.id).filter(User.username == username).first()[0]
        user_role_ins = UserRole(userid = userid, roleid = roleid, createdby=createdby) if createdby else (
            UserRole(userid = userid, roleid = roleid))
        session.add(user_role_ins)
        session.commit()


def get_user_role(session, username: str) -> List[str]:
    roles = session.query(Role.name).join(UserRole).join(User).filter(User.username == username and User.is_active == 1 and UserRole.active == 1 and Role.active == 1).all()
    return [r[0] for r in roles]


def create_voting(session, name: str, type_: str, start_date: date, end_date: date, author: str, credits: int) -> int:
    voteid = session.query(Vote.id).filter(Vote.name == name and Vote.active == 1).first()
    if voteid:
        raise ValueError('Vote already exists. Please use different name')
    if end_date < start_date:
        raise ValueError
    vote = Vote(name = name, type = type_, startdate = start_date, enddate = end_date, author = author, optionnumber = 0, credits = credits, createdby = author, lastupdatedby = author)
    session.add(vote)
    session.commit()
    voteid = session.query(Vote.id).filter(Vote.name == name and Vote.active == 1).first()
    return voteid

