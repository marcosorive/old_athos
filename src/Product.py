from sqlalchemy import Column, Integer, String, ForeignKey, Float
import database
from logger import logger

'''
Class that represents a Product. Used by SqlAchemy ORM.
'''
class Product(database.Base):

    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    store = Column(String)
    current = Column(Float)
    warning = Column(Float)
    delta = Column(Float)
    lowest = Column(Float)

    '''
    '''
    def __init__(self, name, store, url, current_price, warning, delta):
        self.name = name
        self.store = store
        self.url = url
        self.current = current_price
        self.warning = warning
        self.delta = delta
        self.lowest = current_price

    def __str__(self):
        result = f'- Name: {self.name} \n'
        result = result +  f'- Internal ID: {self.id}\n'
        result = result + f'- Store: {self.store}\n'
        result = result + f'- Current price: {self.current}\n'
        result = result + f'- Lowest price: {self.lowest}\n'
        result = result + f'- Warning: {self.warning}\n'
        result = result + f'- Delta: {self.delta}'
        return result

'''
    Adds a product to the DB.
'''
def add_product(name, store, url, current_price, warning, delta):
    session = database.Session()
    try:
        p = Product(name, store, url, current_price, warning, delta)
        session.add(p)
        session.commit()
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise Exception(e.__str__)
    finally:
        session.close()

'''
    Returns all products from DB.
'''
def get_all_products():
    session = database.Session()
    try:
        return session.query(Product).all()
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise Exception(e.__str__)
    finally:
        session.close()

'''
    Deletes a product from DB.
'''
def delete_product(id):
    session = database.Session()
    try:
        product = session.query(Product).filter(Product.id == id).first()
        session.delete(product)
        session.commit()
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise Exception(e.__str__)
    finally:
        session.close()

'''
    Updates the lowest price in DB.
'''
def update_lowest_price(id, lowest_price):
    session = database.Session()
    try:
        p = session.query(Product).filter(Product.id == id).first()
        p.lowest = lowest_price
        session.commit()
    except Exception as e:
        logger.error(e)
        session.rollback()
    finally:
        session.close()
'''
    Updates the current price in the DB.
'''
def update_current_price(id, current_price):
    session = database.Session()
    try:
        p = session.query(Product).filter(Product.id == id).first()
        p.current = current_price
        session.commit()
    except Exception as e:
        logger.error(e)
        session.rollback()
    finally:
        session.close()