import database.database_definitions as db
import database.db_functions as dbf
import voting.voting as v

if __name__ == '__main__':

    # data = [{'username': 'system', 'password': 'xd', 'email': 'hehelol@xd.pl'}]
    # dbf.insert_to_table('User', data)

    session = db.Session()
    # users = dbf.get_user_login(session, 'System')
    # print(users.password)
    v.vote(session, 38, 6, 'test', {4: 2, 5: 2, 6: 2}, 6)

    pass