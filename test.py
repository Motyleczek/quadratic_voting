import database.database_definitions as db
import database.db_functions as dbf

if __name__ == '__main__':

    # data = [{'username': 'system', 'password': 'xd', 'email': 'hehelol@xd.pl'}]
    # db.insert_to_table(db.db_con, db.meta, 'User', data)

    session = db.Session()
    users = dbf.get_user_login(session, 'System')
    print(users.password)

    pass