from utils import file_utils
from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs


def get_list(self):
    browser = webdriver.Chrome()
    browser.get(self.url)
    time.sleep(1)
    elem = browser.find_element(by=By.TAG_NAME, value="body")
    no_of_pagedowns = 20
    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        no_of_pagedowns -= 1

    soup = bs(browser.page_source, "html.parser")
    browser.close()
    divs = soup.find_all("div", attrs={"class": "cmc-table__table-wrapper-outer"})

    symbol_tds = divs[2].find("table").find("tbody").find_all("td", attrs={"class": "cmc-table__cell--sort-by__symbol"})
    print(symbol_tds)
    file_utils.delete("resources/crypto.txt")
    for symbol_td in symbol_tds:
        print(symbol_td)
        symbol = symbol_td.find("div").text
        file_utils.append("resources/crypto.txt", symbol)

# # import requests
#
# from bs4 import BeautifulSoup as bs
# import requests as requests
# import urllib3 as urllib3
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from utils import file_utils
# import time
# from requests import Session
# import json
# from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
#
#
# class Coinmarketcap:
#
#     def __init__(self):
#         urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#         self.url: str = "https://coinmarketcap.com/all/views/all/"
#
#     # def get_crypto_list():
#     #     url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
#     #
#     #     headers = {
#     #         'Accepts': 'application/json',
#     #         'X-CMC_PRO_API_KEY': '4605c4b2-3c4a-4d5e-b0a9-dff288508de0',
#     #     }
#     #     session = Session()
#     #     session.headers.update(headers)
#     #     try:
#     #         response = session.get(url)
#     #         jsonData = json.loads(response.text)
#     #
#     #         for item in jsonData["data"]:
#     #             print(item['symbol'])
#     #
#     #     except (ConnectionError, Timeout, TooManyRedirects) as e:
#     #         print(e)
#
#
