import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

host = os.environ['host']
dbname = os.environ['dbname']
password = os.environ['password']
user = os.environ['user']

SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}:5432/{}".format(user, password, host, dbname)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine)

Base = declarative_base()