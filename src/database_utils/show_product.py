from pymongo import MongoClient

try:
    client = MongoClient('localhost', 27017)
    db = client["amazonpricetracker"]
    product = db.collection["product"]

    products = product.find()
    for i in products:
        print(i)
    client.close()
except Exception as e:
    print("An error ocurred: " + e )