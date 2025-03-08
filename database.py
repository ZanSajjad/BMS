
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Database_Url="sqlite:///database.db"

engine =create_engine(Database_Url,connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)
