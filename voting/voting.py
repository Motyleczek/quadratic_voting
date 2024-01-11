from database.database_definitions import Session, User, UserVote, UserRole, UserVoteDetail, Vote, VoteDetail, Role, db_con, meta
from database.db_functions import add_vote_results_to_db, get_voting_parameters, get_voter_votings, check_user_did_vote

from datetime import date, datetime

from typing import List, Dict, Tuple
from math import sqrt


#TODO: podsumowanie głosowania po jego zakończeniu i uzupełnienie VoteDetail -> ?
#TODO: sprawdzenie czasu otwarcia głosowania -> ?

def get_user_votings(session, userid: int) -> Dict[Tuple[int, str], Tuple[List[Tuple[int, str]], int]]:
    """
    returns dict where key is Tuple [vote id, vote name] and value is Tuple [List[voting options (id and optionname)], credits]
    """
    votings = get_voter_votings(session, userid)
    dict = {}
    for v in votings:
        parameters = get_voting_parameters(session, v[0])
        dict[v] = parameters
    return dict


def vote(session, userid: int, voteid: int, username: str, results: Dict[int, int], credit: int):
    if check_user_did_vote(session, userid, voteid):
        raise ValueError('You have already voted!')
    if sum(results.values()) < credit:
        raise ValueError('You do not use all of your credits')
    if sum(results.values()) > credit:
        raise ValueError('You use too much credits')
    sqrt_results = {key: round(sqrt(results[key]), 4) for key in results.keys()}
    add_vote_results_to_db(session, userid, voteid, username, sqrt_results)



