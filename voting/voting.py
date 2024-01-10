from database.database_definitions import Session, User, UserVote, UserRole, UserVoteDetail, Vote, VoteDetail, Role, db_con, meta
from database.db_functions import add_vote_results_to_db

from datetime import date, datetime

from typing import List, Dict
from math import sqrt


#TODO: podsumowanie głosowania po jego zakończeniu i uzupełnienie VoteDetail
#TODO: sprawdzenie czasu otwarcia głosowania
#TODO: walidacja czy użytkownik głosował

def vote(session, userid: int, voteid: int, username: str, results: Dict[int, int], credit: int):
    if sum(results.values()) < credit:
        raise ValueError('You do not use all of your credits')
    if sum(results.values()) > credit:
        raise ValueError('You use too much credits')
    sqrt_results = {key: round(sqrt(results[key]), 4) for key in results.keys()}
    add_vote_results_to_db(session, userid, voteid, username, sqrt_results)



