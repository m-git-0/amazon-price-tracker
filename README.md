# amazon-price-tracker

This simple project demonstrates how you can strack amazon product prices using python
## steps involves
- Search product uning asins stored in a csv file
- download the html and pass it to the `parse()` function
- extract the data and store them in a database
- access the database and see the stored products(date, asin,price and product title)

## initial setup
- pip install playwright
- playwright install
- pip install bs4
- pip install pandas

##Running the script
`python .\amazon-price-tracker.py`
