from pymongo import MongoClient

try:
    client = MongoClient('localhost', 27017)
    db = client["amazonpricetracker"]
    user = db.collection["user"]

    users = user.find()
    for i in users:
        print(i)
    client.close()
except Exception as e:
    print("An error ocurred: " + e )