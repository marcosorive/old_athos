from Store.Store import Store
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import traceback

class Elcorteingles(Store):

    def __init__(self, driver, logger):
        super(Elcorteingles, self).__init__(driver, logger)

    def get_price_from_url(self, url):
        try:
            self.logger.info(f'Retrieving from elcorteingles url {url}.')
            self.driver.get(url)
        except Exception as e:
            self.logger.error(str(e))
            return False, float(9999999)
        try:
            with open("./corteingles.html","w") as file:
                file.write(self.driver.page_source)
            price = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "price_big")))
            # wait = WebDriverWait(self.driver, 10)
            # price = wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "price_big_sale")))
            # price = self.driver. text_to_be_present_in_element find_element_by_class_name('price_big_sale').text
            price = price.replace("€","").replace(",",".").replace(" ","")
        except Exception as e:
            self.logger.error(str(e))
            traceback.print_exc()
            return False, float(999999)
        self.logger.info(f'Price obtained is {str(price)}')
        return True, float(price)
