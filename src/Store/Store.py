from abc import ABC, abstractmethod

class Store(ABC):

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    @abstractmethod
    def get_price_from_url(self, url):
        raise NotImplementedError("You are calling the base class method.")