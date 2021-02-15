from Store.Store import Store

class Pccomponentes(Store):

    def __init__(self, driver, logger):
        super(Pccomponentes, self).__init__(driver, logger)

    def get_price_from_url(self, url):
        try:
            self.logger.info(f'Retrieving from pccomponentes url {url}.')
            self.driver.get(url)
        except Exception as e:
            self.logger.error(str(e))
            return False, float(9999999)
        try:
            price = self.driver.find_element_by_id('precio-main').text
            price = price.replace("€","").replace(",",".").replace(" ","")
        except Exception as e:
            self.logger.error(str(e))
            return False, float(999999)
        self.logger.info(f'Price obtained is {str(price)}')
        return True, float(price)
