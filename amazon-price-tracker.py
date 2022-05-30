from playwright.sync_api import sync_playwright
from requests import head
from bs4 import BeautifulSoup
import csv

import sqlite3
import datetime
from read_database import read_db

#create the database/connect to databse
conn = sqlite3.connect('amztracker.db')
#create a cursor
c = conn.cursor()

#create a table to store the results
#c.execute('''
#CREATE TABLE prices(date DATE, asin TEXT, price FLOAT, title TEXT)
#''')

def scrape():
    #open the file containing the asins and read them into a list
    asins = []
    with open('asins.csv','r') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            asins.append(row[0])
    #scrape data
    with sync_playwright() as p:
         browser = p.webkit.launch(headless = False,slow_mo=50)
         page = browser.new_page()

         for asin in asins:
            try:
                 page.goto(f'https://www.amazon.com/dp/{asin}')
                 html = page.inner_html('#ppd')
                 parser(html,asin)

            except Exception as e:
                 print(e)
                 #append the asin to be retried later
                 asins.append(asin)
                 continue
         conn.commit()
         print("committed new entries to database!")
        

def parser(html,asin):
    #return price
    soup = BeautifulSoup(html,'html.parser')
    price = soup.find('span','a-offscreen')

    title = soup.find('span',id='productTitle').get_text().strip()
    if price:
        print('----------------------------------------------------------')
        date = datetime.datetime.today()
        price = price.get_text().strip().replace('$','').replace(',','')

        c.execute('''INSERT INTO prices VALUES(?,?,?,?)''',(date,asin,price,title))
        print(f"added data for {asin},\t{price}")
    else:
        print('missing price info')
    


if __name__=='__main__':
    scrape()#extract info and store in a databse
    read_db()#read from the database
