from database.database_definitions import Session, User, UserVote, UserRole, UserVoteDetail, Vote, VoteDetail, Role, db_con, meta
from typing import List, Dict

from sqlalchemy.schema import MetaData


def insert_to_table(tablename: str, insert_data_lst: List[Dict[str, str]]):
    for data in insert_data_lst:
        db_con.execute(meta.tables[tablename].insert(data))


def get_user_login(session, username) -> User:
    return session.query(User).filter(User.username == username).first()
