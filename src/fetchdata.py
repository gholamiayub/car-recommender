import re
import requests
import mysql.connector

from bs4 import BeautifulSoup

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="ayub", # your database username
    passwd="admin", # your database password
    database="bama", # your database name
)

list_items, information, list_years = [], [], []
list_models, list_prices = [], []


def information_regex(item):
    """This function used for
    clear data from more space."""
    regex = re.sub(r'\s+', ' ', item.text) # This replaces more space with one space
    list_items.append(regex)


def get_information(url):
    """ This function used for
    find cars informations from html code."""
    response = requests.get(url) # Send request to target site.
    text = response.text # Extracted html code form target site.
    homes = BeautifulSoup(text, 'html.parser') # Used for clear html code.
    cars_tag = homes.findAll('div', {"class": "card-details"})
    # Extracted html code has class card-details this class include information of cars
    for item in cars_tag:
        """ This loop used for
            clear data from more space
            with information_regex() functio"""
        information_regex(item)

# --- find cars type from follow list ---
models = ['sedan', 'coupe', 'suv', 'wagon', 'convertible', 'van', 'truck']
for model in models:
    """ This loop used for creates liks
        the links has information of cars data"""
    for year in range(2017, 2020):
        UrlName = 'https://www.cars.com/research/{}/{}/?pageNum=0&rpp=110'
        url = UrlName.format(model, year)
        get_information(url)
    for year in range(2015, 2017):
        UrlName = 'https://www.cars.com/research/{}/{}/?pageNum=0&rpp=110'
        url = UrlName.format(model, year)
        get_information(url)
# --- extract data form html code ---
for info in list_items:
    if 'MSRP' in info:
        regex = re.findall(r'\d+ .* STARTING MSRP \$\d+\,\d+', info)
        for item in regex:
            information.append(item.split('STARTING MSRP'))
    if 'CURRENT LISTING PRICE' in info:
        r = r'\d+ .* CURRENT LISTING PRICE \$\d+\,\d+\s\-\s\$\d+\,\d+'
        regex = re.findall(r, info)
        for item in regex:
            information.append(item.split('CURRENT LISTING PRICE'))
# --- Extracting year of production and model of codes ---
for i in information:
    num = i[0].split(maxsplit= 1)
    list_years.append(int(num[0]))
    list_models.append(num[1].strip())
# --- extracting prices from codes ---
for pri in information:
    item = pri[1].replace('$', '')
    item = item.split('-')
    if len(item) == 1:
        item1 = item[0].split(',')
        list_prices.append(int(''.join(item1)))
    if len(item) == 2:
        item2 = item[1].split(',')
        list_prices.append(int(''.join(item2)))

# --- coupling extracted data together ---
zip_item = list(zip(list_models, list_years, list_prices))
mycursor = mydb.cursor()
# --- storing data to database
for item in zip_item:
        car_model, car_year, car_price = item[:3]
         # --- insted tablename insert your tablename ---
        sql = "INSERT IGNORE INTO ML (model, year, price)\
               VALUES (%s, %s, %s)"
        val = [(car_model, car_year, car_price)]
        mycursor.executemany(sql, val)
        mydb.commit()
