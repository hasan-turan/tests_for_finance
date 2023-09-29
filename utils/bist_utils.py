import os.path

from utils import file_utils


def get_bist_stocks():
    path = "../resources/bist100.txt"
    stocks = []
    if not os.path.exists(path):
        return stocks

    # lines = file_utils.read_lines(path)
    #
    # for line in lines:
    #     if len(line.strip()) > 0:
    #         stocks.append(line.replace("\r", "").replace("\n", "") + ".IS")

    with open(path, 'r') as file:
        stocks = file.read().splitlines()

    stocks = [stock.replace("\r", "").replace("\n", "") + ".IS" for stock in stocks]

    return stocks
