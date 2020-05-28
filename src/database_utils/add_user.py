from pymongo import MongoClient
import bcrypt
import sys

if len(sys.argv) < 3:
	print("Falta nombre de usuario/contraseña")
	exit(1)
try:
	username=sys.argv[1]
	passw=sys.argv[2]

	client = MongoClient('localhost', 27017)
	db = client["amazonpricetracker"]
	user = db.collection["user"]

	hashed_pass = bcrypt.hashpw(passw.encode('utf8'),bcrypt.gensalt())
	inserted = user.insert_one({
		"username":username,
		"password":hashed_pass,
		"chat_id":None
	})
	client.close()
	print("Usuario añadido correctamente")
except Exception as e:
	print("Ha habido un error: " + e )
