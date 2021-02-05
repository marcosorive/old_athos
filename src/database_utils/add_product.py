import sys
import os
from pathlib import Path
path = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path.parent.__str__())
import database
from Product import Product

if len(sys.argv) < 5:
    print("Missing parameters. Order of parameters:  amazon_id, current price, name, warning, delta")
    exit(1)

database.Base.metadata.create_all(database.engine)
session = database.Session()

p = Product(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

session.add(p)
session.commit()
print("Product added successfully!")

session.close()
'''
Example: python add_product.py B07PHPXHQS 100 echo_dot 50 50
'''