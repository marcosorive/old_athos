import sys
import os
from pathlib import Path
path = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path.parent.__str__())
import database
from User import User
import bcrypt

if len(sys.argv) < 3:
    print("User or password missing.")
    exit(1)
try:
    database.Base.metadata.create_all(database.engine)
    session = database.Session()
    
    username=sys.argv[1]
    passw=sys.argv[2]


    hashed_pass = bcrypt.hashpw(passw.encode('utf8'), bcrypt.gensalt())
    user = User(username, hashed_pass)
    session.add(user)
    session.commit()
    print("User added correctly.")
except Exception as e:
    session.rollback()
    print("An error ocurred: " + e )
finally:
    session.close()