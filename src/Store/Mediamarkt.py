from Store.Store import Store
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import traceback


class Mediamarkt(Store):

    def __init__(self, driver, logger):
        super(Mediamarkt, self).__init__(driver, logger)

    def get_price_from_url(self, url):
        try:
            self.logger.info(f'Retrieving from mediamarkt url {url}.')
            self.driver.get(url)
        except Exception as e:
            self.logger.error(str(e))
            return False, float(9999999)
        try:
            with open("./mediamark.html","w") as file:
                file.write(self.driver.page_source)
            price = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "price big length-5")))
            price = price.replace("€","").replace(",",".").replace(" ","").replace("-","")
        except Exception as e:
            traceback.print_exc()
            self.logger.error(str(e))
            return False, float(999999)
        self.logger.info(f'Price obtained is {str(price)}')
        return True, float(price)
