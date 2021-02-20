import bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey, Float
import database
from logger import logger

'''
Class that represents a User. Uses by SqlAchemy ORM.
'''
class User(database.Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    chat_id = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

'''
Helper function that checks the password of a user.
'''
def login(logger, username, password):
    session = database.Session()
    try:
        user = session.query(User).filter_by(username = username).first()
        return bcrypt.checkpw(password.encode('utf-8') , bytes.decode(user.password).encode('utf-8'))
    except Exception as e:
        logger.error(e)
        session.rollback()
    finally:
        session.close()
    return False

'''
Helper function adds a chat id to a user. Adding the chat id to the DB means that the user has been authenticated.
'''
def add_chat_id_to_user(logger, username, chat_id):
    session = database.Session()
    try:
        user = session.query(User).filter_by(username = username).first()
        user.chat_id = chat_id
        session.commit()
    except Exception as e:
        logger.error(e)
        session.rollback()
    finally:
        session.close()

'''
Checks if the user id is in the DB, and thus, the user has been authenticated.
'''
def check_chat_id(chat_id):
    session = database.Session()
    try:
        return session.query(User).filter_by(chat_id = chat_id).count() == 1
    except Exception as e:
        logger.error(e)
        session.rollback()
    finally:
        session.close()

def get_all_chat_ids():
    session = database.Session()
    try:
        users = session.query(User).all()
    except Exception as e:
        logger.error(e)
        session.rollback()
    finally:
        session.close()
    return [u.chat_id for u in users]