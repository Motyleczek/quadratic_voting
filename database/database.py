from typing import List, Dict

from dotenv import load_dotenv
from sqlalchemy import create_engine, insert
from sqlalchemy.schema import MetaData
from sqlalchemy.sql import text
import os


def insert_to_table(db_conn, metadata: MetaData, tablename: str, insert_data_lst: List[Dict[str, str]]):
    for data in insert_data_lst:
        db_conn.execute(metadata.tables[tablename].insert(data))


def get_password(db_conn, username: str) -> str:
    query = "Select password from User where username = '" + username + "'"
    res = db_conn.execute(query)
    for r in res:
        return r[0]


load_dotenv()

db_link = f'mysql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}'
eng = create_engine(db_link)
db_con = eng.connect()

meta = MetaData()
meta.reflect(bind=eng)





