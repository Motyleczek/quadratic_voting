from dotenv import load_dotenv
from sqlalchemy import create_engine, insert
from sqlalchemy.schema import MetaData
import os


load_dotenv()

db_link = f'mysql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}'
eng = create_engine(db_link)
db_con = eng.connect()

meta = MetaData()
meta.reflect(bind=eng)

for table_name, table in meta.tables.items():
    print(table_name)

# print(stmt.compile(eng))