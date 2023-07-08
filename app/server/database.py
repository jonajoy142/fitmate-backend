"""
Database connectivity file
"""
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os

# get enviornment variables
load_dotenv(find_dotenv())

host = os.getenv("DATABASE_HOST")
username = os.getenv('DATABASE_USER_NAME')
password = os.getenv('DATABASE_PASSWORD')
database = os.getenv('DATABASE')

# database url
DATABASE_URL = f"postgresql://{username}:{password}@{host}/{database}"

# get database connect via engine
engine = create_engine(DATABASE_URL)

# local session creator for database
local_session = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine,
)

# base to create models to database
base = declarative_base()
