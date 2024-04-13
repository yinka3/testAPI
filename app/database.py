from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings as envset

SQLALCHMY_DATABASE_URL = f'postgresql://{envset.db_username}:{envset.db_password}@{envset.db_hostname}/{envset.db_name}'


engine = create_engine(SQLALCHMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# In case I need to run raw SQL instead of sqlachemy
# while True:
#   try:
#     conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='Freeword3', 
#                           row_factory=dict_row)
#     cursor = conn.cursor()
#     print("Successfully connected to Database")
#     break
#   except Exception as error:
#     print("Failed to connect")
#     print("Error: ", error)
#     time.sleep(3)