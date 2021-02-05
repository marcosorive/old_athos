import sys
import os
from pathlib import Path
path = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path.parent.__str__())
import database
from Product import Product

try:
    database.Base.metadata.create_all(database.engine)
    session = database.Session()

    products = session.query(Product).all()
    for i in products:
        print(i)
        print("-----------------")
except Exception as e:
    session.rollback()
    print("An error ocurred: " + e.__str__ )
finally:
    session.close()