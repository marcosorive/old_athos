from pymongo import MongoClient
import bcrypt
import logging

class Auth:
	
	def __init__(self, logger):
		self.logger = logger
		self.client = MongoClient('localhost', 27017)
		self.db = self.client["amazonpricetracker"]
		self.user = self.db.collection["user"]

	def login(self,username,password):
		if ( self.user.find({"username": username}).count() == 0 ):
			return False
		else:
			cursor=self.user.find_one({"username":username})
			return bcrypt.checkpw(password.encode('utf-8'),bytes.decode(cursor["password"]).encode('utf-8'),)

	def add_chat_id_to_user(self,username,chat_id):
		if (self.user.find({"username": username}).count() == 0 ):
			return False
		else:
			return self.user.update_one({"username": username},{"$set":{"chat_id":chat_id}})

	def check_chat_id(self,chat_id):
		return self.user.find({"chat_id": chat_id}).count() == 1

	def get_chat_id_from_user(self,username):
		return self.user.find_one({"username": username})["chat_id"]

	def get_all_chat_id(self):
		users = self.user.find()
		return [ user["chat_id"] for user in users ]

	def print_all_users(self):
		for i in self.user.find({}):
			print(i)