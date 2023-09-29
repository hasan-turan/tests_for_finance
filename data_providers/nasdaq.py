from bs4 import BeautifulSoup
import requests
import certifi


def get_list():
    url =   'https://www.nasdaq.com/market-activity/quotes/nasdaq-ndx-index'
    session = requests.Session()
    session.verify = certifi.where()
    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", attrs={"class": "nasdaq-ndx-index__table"})

        if table:
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                first_column_data = columns[0].get_text()
                print(first_column_data)
        else:
            print('Table not found on the page.')
    else:
        print('Failed to retrieve the web page.')
