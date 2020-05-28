from pymongo import MongoClient
from bson.objectid import ObjectId
import sys

if len(sys.argv) < 2:
	print("User ID missing")
	exit(1)
try:
	user_id=sys.argv[1]

	client = MongoClient('localhost', 27017)
	db = client["amazonpricetracker"]
	user = db.collection["user"]

	deleted = user.delete_one({
		"_id" :  ObjectId(user_id),
	})
	client.close()
	print("User deleted")
except Exception as e:
	print("An error ocurred: " + e )