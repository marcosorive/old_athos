class Amazon:

    def __init__(self, logger):
        self.logger = logger
        self.url_header = "https://www.amazon.es/dp/"

    def get_price_with_id(self, id, driver):
        try:
            url = self.url_header+id
            self.logger.info(f'Retrieving from amazon url {url}.')
            driver.get(self.url_header+id)
            with open("test.test.html","w", encoding="utf8") as file:
                file.write(driver.page_source)
        except Exception as e:
            self.logger.error(str(e))
            return float(9999999)
        tries = 0
        while True:
            try:
                if tries == 0:
                    price = driver.find_element_by_id('priceblock_saleprice').text
                elif tries == 1:
                    price = driver.find_element_by_id('priceblock_ourprice').text
                elif tries == 2:
                    price = driver.find_element_by_id('priceblock_dealprice').text
                elif tries == 3:
                    price = driver.find_element_by_id('olp-sl-new-used').find_element_by_class_name("a-color-price").text
                else:
                    price = "9999999"
                break
            except Exception as e:
                self.logger.error(str(e))
                tries += 1
        price = price.replace("€","").replace(",",".").replace(" ","")
        return float(price)