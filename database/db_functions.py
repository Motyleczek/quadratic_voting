from database.database_definitions import Session, User, UserVote, UserRole, UserVoteDetail, Vote, VoteDetail, Role, db_con, meta
from datetime import date, datetime
from typing import List, Dict, Tuple

from sqlalchemy.schema import MetaData
import sqlalchemy

# Users

def insert_to_table(tablename: str, insert_data_lst: List[Dict[str, str]]):
    for data in insert_data_lst:
        db_con.execute(meta.tables[tablename].insert(data))


def get_user_login(session, username: str) -> User:
    return session.query(User).filter(User.username == username, User.is_active == 1).first()


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
        roleid = session.query(Role.id).filter(Role.name == user_role, Role.active == 1).first()[0]
        userid = session.query(User.id).filter(User.username == username).first()[0]
        user_role_ins = UserRole(userid = userid, roleid = roleid, createdby = createdby, lastupdatedby = createdby) if createdby else (
            UserRole(userid = userid, roleid = roleid))
        session.add(user_role_ins)
        session.commit()


def get_user_role(session, username: str) -> List[str]:
    userid1 = session.query(User.id).filter(User.username == username, User.is_acive == 1).first()[0]
    roles_id = session.query(UserRole.roleid).filter(UserRole.userid == userid1, UserRole.active == 1).all()
    roles = []
    for rid in roles_id:
        roles.append(session.query(Role.name).filter(Role.id == rid[0], Role.active == 1).first())
    return [r[0] for r in roles]

def get_voters_createdby_user(session, username: str) -> List[str]:
    role_voter = session.query(Role.id).filter(Role.name == 'Voter', Role.active == 1).first()[0]
    voters_id = session.query(UserRole.userid).filter(UserRole.roleid == role_voter, UserRole.active == 1).all()
    users_lst = []
    for voter in voters_id:
        u = session.query(User.username).filter(User.createdby == username, User.id == voter[0], User.is_active == 1).first()
        if u:
            users_lst.append(u[0])
    return users_lst

# Voting
def create_voting(session, name: str, start_date: date, end_date: date, author: str, credits: int, type_: str = 'Rankingowe') -> int:
    voteid = session.query(Vote.id).filter(Vote.name == name, Vote.active == 1).first()
    if voteid:
        raise ValueError('Vote already exists. Please use different name')
    if end_date < start_date:
        raise ValueError('End date cannot be earlier than start date!')
    vote = Vote(name = name, type = type_, startdate = start_date, enddate = end_date, author = author, optionnumber = 0, credits = credits, createdby = author, lastupdatedby = author)
    session.add(vote)
    session.commit()
    voteid = session.query(Vote.id).filter(Vote.name == name, Vote.active == 1).first()[0]
    userid = session.query(User.id).filter(User.username == author, User.is_active == 1).first()[0]
    uservote = UserVote(userid = userid, voteid = voteid, role = 'Author', createdby = author, lastupdatedby = author)
    session.add(uservote)
    session.commit()
    return voteid


def add_options_to_voting(session, voteid: int, option_list: List[str], createdby: str):
    for optionname in option_list:
        votedetail = VoteDetail(voteid = voteid, optionname = optionname, createdby = createdby, lastupdatedby = createdby)
        session.add(votedetail)
        session.commit()
    vote = session.query(Vote).filter(Vote.id == voteid)
    vote_record = vote.one()
    vote_record.optionnumber = len(option_list)
    vote_record.lastupdatedby = createdby
    vote_record.lastupdatedon = datetime.now()
    session.commit()
    

def add_users_to_voting(session, voteid: int, users_list: List[str], createdby: str, role: str = 'Voter'):
    for username in users_list:
        userid = session.query(User.id).filter(User.username == username, User.is_active == 1).first()[0]
        voteuser = UserVote(userid = userid, voteid = voteid, role = role, createdby = createdby, lastupdatedby = createdby)
        session.add(voteuser)
        session.commit()


def get_voting_parameters(session, voteid: int) -> Tuple[List[str], int]:
    option_lst = session.query(VoteDetail.optionname).filter(VoteDetail.voteid == voteid, VoteDetail.active == 1).all()
    option_lst =  [o[0] for o in option_lst]
    credit = session.query(Vote.credits).filter(Vote.id == voteid, Vote.active == 1).first()[0]
    return option_lst, credit

def add_vote_results_to_db(session, userid: int, voteid: int, username:str, result_dict: Dict[int, int]):
    """
    result_dict - dict where key is option id from VoteDetail table and value is result for the option
    """
    uservoteid = session.query(UserVote.id).filter(UserVote.userid == userid, UserVote.voteid == voteid, UserVote.active == 1).first()[0]
    for option in result_dict.keys():
        uservotedetail = UserVoteDetail(uservoteid = uservoteid, votedetailid = option, result = result_dict[option], createdby = username, lastupdatedby = username)
        session.add(uservotedetail)
        session.commit()
    uservote = session.query(UserVote).filter(UserVote.userid == userid, UserVote.voteid == voteid, UserVote.active == 1)
    uservote_record = uservote.one()
    uservote_record.didvote = 1
    uservote_record.lastupdatedby = username
    uservote_record.lastupdatedon = datetime.now()
    session.commit()


def add_vote_summary(session, username: str, voteid: int):
    optionid_lst = session.query(VoteDetail.id).filter(VoteDetail.voteid == voteid, VoteDetail.active == 1).all()
    optionid_lst = [o[0] for o in optionid_lst]
    for o in optionid_lst:
        results = session.query(UserVoteDetail.result).filter(UserVoteDetail.votedetailid == o, UserVoteDetail.active == 1).all()
        sm = sum([r[0] for r in results])
        vote_detail = session.query(VoteDetail).filter(VoteDetail.id == o, VoteDetail.active == 1)
        vote_detail_record = vote_detail.one()
        vote_detail_record.lastupdatedon = datetime.now()
        vote_detail_record.lastupdatedby = username
        vote_detail_record.result = sm
        session.commit()

def get_vote_summary(session, voteid: int) -> Tuple[Dict[str, int], float]:
    results = session.query(VoteDetail.optionname, VoteDetail.result).filter(VoteDetail.voteid == voteid, VoteDetail.active == 1).all()
    # users_lst = session.query(UserVote.userid).filter(UserVote.voteid == voteid and UserVote.active == 1).all()
    # all_voters = len(users_lst)
    # voters = 0
    # for u in users_lst:



