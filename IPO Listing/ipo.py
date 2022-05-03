import os
from datetime import date
import requests
import bs4
import pandas as pd
from IPython.display import display
from tabulate import tabulate


# HTML request
res = requests.get('https://investorzone.in/ipo/')
soup = bs4.BeautifulSoup(res.text,"lxml")

# Creating soup object for both IPO instances
items_mainline = soup.find(id='table-fill-1')
items_sme = soup.find(id='hot-stocks')

# Getting headers, same for both tables
headers = items_mainline.find_all('th')
headers_sme = items_sme.find_all('th')



# Creating empty map object for storing text values of the response
def create_ipo_map(headers):
    ipo_map = {}
    for x in headers:
        ipo_map[x.text] = []
    return ipo_map

ipo_map = create_ipo_map(headers)
ipo_map_sme = create_ipo_map(headers_sme)


# Getting text Rows
rows = items_mainline.find_all('tr')
rows_sme = items_sme.find_all('tr')
# rows.extend(items_sme.find_all('tr'))

# Creating row list object, filtering empty rows out
def create_row_list(rows):
    row_list = []
    for row in rows:
        row_list.append(row.findAll('td'))
    return row_list

row_list = create_row_list(rows)
row_list_sme = create_row_list(rows_sme)

row_list = list(filter(lambda x: x != [], row_list))
row_list_sme = list(filter(lambda x: x != [], row_list_sme))

# Appending rows to the map object
def row_append(row_list, headers, ipo_map):
    for i in range(len(row_list)):
        for j,x in enumerate(headers):
            temp = ipo_map[x.text]
            temp.append(row_list[i][j].text)
            ipo_map[x.text] = temp
    
    return ipo_map

ipo_map = row_append(row_list, headers, ipo_map)
ipo_map_sme = row_append(row_list_sme, headers_sme, ipo_map_sme)

# Creating dataframe object
df = pd.DataFrame(ipo_map)
df_sme = pd.DataFrame(ipo_map_sme)

# Getting today's date for comparison
today = date.today()
today = today.strftime("%Y-%m-%d")

# Convert date for df comparison
curr_date = pd.to_datetime(today) 

# Dataframe list
df_list = [df, df_sme]

# Changing data types of the date columns from text to datetime
for x in df_list:
    x["Open Date"] = pd.to_datetime(x["Open Date"])
    x["Close Date"] = pd.to_datetime(x["Close Date"])

# Filter condition for open IPOs
upcoming_ipos = df[curr_date <= df["Close Date"]]
upcoming_ipos_sme = df_sme[curr_date <= df_sme["Close Date"]]


# Output
# display(upcoming_ipos.head())

# df.to_csv('dataframe.csv')
# upcoming_ipos.to_csv('upcoming_ipos.csv')
# upcoming_ipos_sme.to_csv('upcoming_ipos_sme.csv')

with pd.ExcelWriter('.\\IPO Listing\\upcoming_ipos.xlsx') as writer:
    upcoming_ipos.to_excel(writer, sheet_name='MainLine', index=False)
    upcoming_ipos_sme.to_excel(writer, sheet_name='SME', index=False)

# print(tabulate(df, headers = 'keys', tablefmt = 'psql'))