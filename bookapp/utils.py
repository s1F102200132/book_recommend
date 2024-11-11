# utils.pyに記述するコード
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ASIN取得関数
def get_asin_from_amazon_2(url):
    asin = ""
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome("chromedriver.exeのパス", options=options)
    driver.get(url)
    driver.implicitly_wait(10)
    
    elem_base = driver.find_element_by_id('ASIN')
    if elem_base:
        asin = elem_base.get_attribute("value")
    driver.quit()
    return asin

# Amazonページ取得関数
def get_page_from_amazon(url):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome("chromedriver.exeのパス", options=options)
    driver.get(url)
    driver.implicitly_wait(10)
    
    text = driver.page_source
    driver.quit()
    return text
