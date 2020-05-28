from pymongo import MongoClient
import sys

if len(sys.argv) < 5:
	print("Missing parameters. Order of parameters: amazon ID, name, warning price, delta price, lowest price, current price.")
	exit(1)
try:
	client = MongoClient('localhost', 27017)
	db = client["amazonpricetracker"]
	product = db.collection["product"]

	inserted = product.insert_one({
                "amazon_id":sys.argv[1],
				"name":sys.argv[2],
                "warning":sys.argv[3],
                "delta":sys.argv[4],
                "lowest":sys.argv[5],
                "current":sys.argv[6],
    })
	client.close()
	print("Product added successfully!")
except Exception as e:
	print("An error ocurred: " + e )

'''
Example: python add_product.py B07PHPXHQS echo_dot 1 5 50 50
'''