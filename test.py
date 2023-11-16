import database.database as db

if __name__ == '__main__':

    # data = [{'username': 'system', 'password': 'xd', 'email': 'hehelol@xd.pl'}]
    # db.insert_to_table(db.db_con, db.meta, 'User', data)

    session = db.Session()
    users = session.query(db.User).filter(db.User.username == 'System').first()
    print(users.id)

    pass