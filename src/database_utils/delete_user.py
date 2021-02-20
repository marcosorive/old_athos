import sys
import os
from pathlib import Path
path = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path.parent.__str__())
import database
from User import User


if len(sys.argv) < 2:
	print("User ID missing")
	exit(1)
try:
    database.Base.metadata.create_all(database.engine)
    session = database.Session()
    
	u = session.query(User).filter(User.id == id).first()
	session.delete(u)
    session.commit()
    print("User deleted correctly.")
except Exception as e:
    session.rollback()
    print("An error ocurred: " + e )
finally:
    session.close()