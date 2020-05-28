from pymongo import MongoClient
from bson.objectid import ObjectId

class Product:

    def __init__(self, logger):
        self.logger = logger
        self.client = MongoClient('localhost', 27017)
        self.db = self.client["amazonpricetracker"]
        self.product = self.db.collection["product"]

    def add_product(self,amazon_id,current_price,name="",warning=0,delta=0):
        self.logger.info("Adding product: " + amazon_id + name + warning + delta)
        try:
            return self.product.insert_one({
                "name":name,
                "amazon_id":amazon_id,
                "warning":warning,
                "delta":delta,
                "lowest":current_price,
                "current":current_price,
            })
        except Exception as e:
            self.logger.error("Error adding product: " + str(e))
            return None
    
    def delete_product(self,id):
        self.logger.info("Deleting product with id: " +  str(id))
        try:
            return self.product.delete_one({
                "_id" : ObjectId(id)
            }).deleted_count
        except Exception as e:
            self.logger.error("Error deleting product: " + str(e))
            return None
    
    def get_all_products(self):
        self.logger.info("Getting all products")
        try:
            products = self.product.find({})
            return products
        except Exception as e:
            self.logger.error("Error getting all products: " + str(e))
            return None
 
    def update_current_price(self, id, price):
        self.logger.info("Updating current price of product with id: " +  str(id) + ". New price is " + str(price))
        try:
            return self.product.update_one({"_id": ObjectId(id)},{"$set":{"current":price}}).modified_count
        except Exception as e:
            self.logger.error("Error updating current price: " + str(e))
            return None

    def update_lowest_price(self,id,price):
        self.logger.info("Updating lowest price of product with id:" +  str(id))
        try:
            return self.product.update_one({"_id": ObjectId(id)},{"$set":{"lowest":price}}).modified_count
        except Exception as e:
            self.logger.error("Error updating lowest price: " + str(e))
            return None