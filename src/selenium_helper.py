from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROMEDRIVER_PATH = "C:/Users/Marcos/webdriver/chromedriver.exe"
GOOGLE_CHROME_BIN = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"

def get_driver():
    options = Options()
    ua = UserAgent()
    options.binary_location = GOOGLE_CHROME_BIN
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=3")
    options.add_argument("user-agent=" + ua.random)
    options.headless = True

    return webdriver.Chrome(executable_path=CHROMEDRIVER_PATH , chrome_options=options)

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