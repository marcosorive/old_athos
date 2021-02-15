import sys
import os
from pathlib import Path
path = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path.parent.__str__())
import database
from Product import Product
import utils

if len(sys.argv) < 5:
    print("Missing parameters. Order of parameters: name, url, current price, warning, delta")
    exit(1)

store = utils.get_domain_from_url(sys.argv[2])

database.Base.metadata.create_all(database.engine)
session = database.Session()

p = Product(sys.argv[1], store, sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

session.add(p)
session.commit()
print("Product added successfully!")

session.close()
'''
Example: python add_product.py standMixer https://www.elcorteingles.es/electrodomesticos/A26340496-robot-de-cocina-kitchenaid-5k45sseob-con-bol-de-43-litros/ 339.15 300 20
'''