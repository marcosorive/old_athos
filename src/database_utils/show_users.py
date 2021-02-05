import sys
import os
from pathlib import Path
path = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path.parent.__str__())
import database
from User import User

try:
    database.Base.metadata.create_all(database.engine)
    session = database.Session()

    users = session.query(User).all()
    for i in users:
        print(i)
        print("-----------------")
except Exception as e:
    session.rollback()
    print("An error ocurred: " + e.__str__ )
finally:
    session.close()