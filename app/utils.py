"""
General utilities
"""
import sys
sys.path.append("../")

from app.server.database import local_session
from sqlalchemy.orm import Session

def get_db()->Session:
    """
    Connect to database 
    :return : local session of database
    """
    db_session = local_session()
    try:
        yield db_session
    finally:
        db_session.close()