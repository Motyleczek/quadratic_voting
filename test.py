import database.database as db

if __name__ == '__main__':

    data = [{'name': 'Voter1'}]
    db.insert_to_table(db.db_con, db.meta, 'Role', data)

