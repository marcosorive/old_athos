from bot_config import configure;
from selenium_helper import get_driver;

class Amazon:

    def __init__(self, logger, driver):
        self.logger = logger
        self.url_header = "https://www.amazon.es/dp/"
        self.driver = driver

    def get_price_with_id(self,id):
        try:
            self.driver.get(self.url_header+id)
        except Exception as e:
            self.logger.error(str(e))
            return float(9999999)
        tries = 0
        while True:
            try:
                if tries == 0:
                    price = self.driver.find_element_by_id('priceblock_saleprice').text
                    price = price.replace("€","").replace(",",".").replace(" ","")
                elif tries == 1:
                    price = self.driver.find_element_by_id('priceblock_ourprice').text
                elif tries == 2:
                    price = self.driver.find_element_by_id('priceblock_dealprice').text
                elif tries == 3:
                    price = self.driver.find_element_by_id('olp-sl-new-used').find_element_by_class_name("a-color-price").text
                else:
                    price = 9999999
                break
            except Exception as e:
                self.logger.error(str(e))
                tries += 1
        price = price.replace("€","").replace(",",".").replace(" ","")
        return float(price)