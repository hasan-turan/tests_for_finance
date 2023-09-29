import requests
from bs4 import BeautifulSoup as bs
import csv

from utils import file_utils


def get_bist_100():
    html = requests.get('http://www.kap.org.tr/tr/Endeksler', verify=False).text
    soup = bs(html, "html.parser")
    bist_100_tables = soup.find("div", string="BIST 100", attrs={'class': 'vcell'}).parent.find_next_siblings("div", attrs={"class": "column-type7 wmargin"})
    if len(bist_100_tables) == 0:
        return

    bist_100 = bist_100_tables[0]

    # bist100 = soup.find('div', {'class': 'column-type7 wmargin'})
    stocks = bist_100.findAll("div", {'class': 'comp-cell _02 vtable'})

    f = open("../resources/bist100.txt", "w")
    for stock in stocks:
        stock_name = stock.find('a').text
        f.write(stock_name + "\n")
    f.close()


def get_bist_all():
    html = requests.get('http://www.kap.org.tr/tr/Endeksler', verify=False).text
    soup = bs(html, "html.parser")
    bist_all_tables = soup.find("div", string="BIST TÜM", attrs={'class': 'vcell'}).parent.find_next_siblings("div", attrs={"class": "column-type7 wmargin"})
    if len(bist_all_tables) == 0:
        return

    bist_all = bist_all_tables[0]
    stocks = bist_all.findAll("div", {'class': 'comp-cell _02 vtable'})

    for stock in stocks:
        stock_name = stock.find('a').text
        file_utils.append(stock_name + "\n")
