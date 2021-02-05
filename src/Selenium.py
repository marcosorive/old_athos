from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROMEDRIVER_PATH = "C:/Users/Marcos/webdriver/chromedriver.exe"
GOOGLE_CHROME_BIN = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"

class Selenium:

    def __init__(self):
        self.ua = UserAgent()

    def setup(self):
        options = Options()
        options.binary_location = GOOGLE_CHROME_BIN
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument("--log-level=3")
        options.add_argument("user-agent=" + self.ua.random)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.headless = True
        self.driver = webdriver.Chrome(executable_path = CHROMEDRIVER_PATH , chrome_options = options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return self.driver

    def dispose(self):
        self.driver.quit()

# def test_selenium():
#     options = Options()
#     ua = UserAgent()
#     options.binary_location = GOOGLE_CHROME_BIN
#     options.add_argument('--disable-gpu')
#     options.add_argument('--no-sandbox')
#     options.add_argument("user-agent=" + ua.random)
#     options.headless = True

#     driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH , chrome_options=options)

#     # url = 'https://www.amazon.es/dp/B01HD5KCKC'
#     url = "https://www.game.es/buscar/mario"
#     driver.get(url)

#     # el = driver.find_element_by_id('priceblock_saleprice')
#     el = driver.find_element_by_class_name('buy--price')

#     print(el.text)