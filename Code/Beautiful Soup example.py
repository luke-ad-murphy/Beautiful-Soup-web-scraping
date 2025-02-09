########################## SCRIPT OVERVIEW #################################
"""

Purpose: Assignment 1, Data Science MSc Scripting module
Question 2

Author: Luke Murphy
Created: 21st February 2020
Last edited: 29th March 2020
Last edited by: Luke Murphy

"""

############################################################################

import requests
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import bs4
import pandas as pd

# Function to extract all elements from each page in turn
def soup(nextpage):
    url ="https://www.autotrader.co.uk/car-search?advertClassification=standard&postcode=SL71LQ&onesearchad=Used&onesearchad=Nearly%20New&onesearchad=New&advertising-location=at_cars&is-quick-search=TRUE&page={}".format(nextpage)
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, "html.parser")
    cars = soup.find_all('li', {'class':'search-page__result'})
    sales_title = [ads.find('h2', {'class':'listing-title'}).find('a',{'class':'js-click-handler listing-fpa-link tracking-standard-link'}).text for ads in cars]
    attention = [ads.find('p', {'class':'listing-attention-grabber'}).text for ads in cars]
    price = [ads.find('div', {'class':'vehicle-price'}).text.strip() for ads in cars]
    reg_yr = [ads.find('li').text.strip() for ads in cars]
    temp_li = [ads.find_all('li') for ads in cars]
    mileage = [e[2].text.rsplit(' miles', 1)[0].strip() if len(e) >= 3 else '' for e in temp_li]
    engine_size = [e[3].text.rsplit('L', 1)[0].strip() if len(e) >= 2 else '' for e in temp_li]
    transmission = [e[5].text.strip() if len(e) >= 4 else '' for e in temp_li]  
    fuel = [e[6].text.strip() if len(e) >= 4 else '' for e in temp_li]
    body_type = [e[1].text.strip() if len(e) >= 1 else '' for e in temp_li]
    owners = [e[7].text.rsplit(' own', 1)[0].strip() if len(e) >= 1 else '' for e in temp_li]
    locs = [ads.find_all('span', {'class':'seller-town'}) for ads in cars]
    location = [e[0].text.strip().title() if len(e) >= 1 else '' for e in locs]
    linkz = [ads.find('a',{'class':'tracking-motoring-products-link action-anchor'})['href'] for ads in cars]
    df = pd.DataFrame({'href':linkz})
    df['blurb'] = df['href'].str.split('numSeats=').str[1]
    df['seats'] = df['blurb'].str[:1]
    numseats = df['seats'].tolist()
    return sales_title, attention, price, reg_yr, mileage, engine_size, transmission, fuel, body_type, owners, location, numseats;

# Run the function to extract the elements for selected pages
soup(1)
soup(2)
soup(3)
soup(4)
soup(5)

# Create a tuple for the elements extracted from each page
p1 = soup(1)
p2 = soup(2)
p3 = soup(3)
p4 = soup(4)
p5 = soup(5)

# create dataframes from tuples
df_auto_p1 = pd.DataFrame(list(p1)).transpose()
df_auto_p1.columns = ['sales_title', 'attention', 'price', 'reg_yr', 'mileage',
                      'engine_size','transmission', 'fuel', 'body_type', 
                      'owners', 'location', 'numseats']

df_auto_p2 = pd.DataFrame(list(p2)).transpose()
df_auto_p2.columns = ['sales_title', 'attention', 'price', 'reg_yr', 'mileage',
                      'engine_size','transmission', 'fuel', 'body_type', 
                      'owners', 'location', 'numseats']

df_auto_p3 = pd.DataFrame(list(p3)).transpose()
df_auto_p3.columns = ['sales_title', 'attention', 'price', 'reg_yr', 'mileage',
                      'engine_size','transmission', 'fuel', 'body_type', 
                      'owners', 'location', 'numseats']

df_auto_p4 = pd.DataFrame(list(p4)).transpose()
df_auto_p4.columns = ['sales_title', 'attention', 'price', 'reg_yr', 'mileage',
                      'engine_size','transmission', 'fuel', 'body_type', 
                      'owners', 'location', 'numseats']

df_auto_p5 = pd.DataFrame(list(p5)).transpose()
df_auto_p5.columns = ['sales_title', 'attention', 'price', 'reg_yr', 'mileage',
                      'engine_size','transmission', 'fuel', 'body_type', 
                      'owners', 'location', 'numseats']


#######################################################
#######################################################
#######################################################


### APPEND DATAFRAMES
df_cars_all = pd.concat([df_auto_p1, df_auto_p2, df_auto_p3, df_auto_p4, df_auto_p5])


#######################################################
#######################################################
#######################################################


### CLEAN OVEARLL DATAFRAME

# run frequencies to understand any data issues

# Examine and clean up:
    
# Price
df_cars_all.groupby(['price']).size().reset_index(name='counts')
df_cars_all['price'] = (df_cars_all['price'].
          replace(',','', regex=True).
          replace('£','', regex=True)).astype('int64')


# Reg yr
df_cars_all.groupby(['reg_yr']).size().reset_index(name='counts')
# take first four chars from reg_yr as reg_yr
df_cars_all['reg_yr'] = (df_cars_all['reg_yr'].str.slice(0, 4).astype('int64'))
df_cars_all.groupby(['reg_yr']).size().reset_index(name='counts')


# Mileage
df_cars_all.groupby(['mileage']).size().reset_index(name='counts')
df_cars_all['mileage'] = (df_cars_all['mileage'].replace(',','', regex=True)).astype('int64')


# Engine size
df_cars_all.groupby(['engine_size']).size().reset_index(name='counts')
df_cars_all['engine_size'] = (df_cars_all['engine_size'].astype(float))


# Transmission
df_cars_all.groupby(['transmission']).size().reset_index(name='counts')
# need to replace 'Diesel'
df_cars_all.transmission.replace({"Diesel": "Unknown"}, inplace=True)
df_cars_all.groupby(['transmission']).size().reset_index(name='counts')


# Fueltype
df_cars_all.groupby(['fuel']).size().reset_index(name='counts')
# need to replace '4 owners'
df_cars_all.fuel.replace({"4 owners": "Unknown"}, inplace=True)
df_cars_all.groupby(['fuel']).size().reset_index(name='counts')


# Body type
df_cars_all.groupby(['body_type']).size().reset_index(name='counts')
                        
                        
# Owners                        
df_cars_all.groupby(['owners']).size().reset_index(name='counts')
# need to replace 'Full service history','Part service history','Petrol'
df_cars_all.owners.replace({"": "Unknown",
                            "Full service history": "Unknown",
                            "Part service history": "Unknown",
                            "ULEZ": "Unknown"}, inplace=True)
df_cars_all.groupby(['owners']).size().reset_index(name='counts')


# Number of seats                      
df_cars_all.groupby(['numseats']).size().reset_index(name='counts')



#############################################################################
#############################################################################
#############################################################################

### Output to CSV
df_cars_all.to_csv('C:/Users/LMurphy/Desktop/Autotrader_db.csv', index=False)


#############################################################################
#############################################################################
#############################################################################


### ANALYSIS OF COLLECTED DATA

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# set font sizes and style for visulations
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 8}
plt.rc('font', **font)


## Read in CSV file
autotrader = pd.read_csv("C:/Users/LMurphy/Desktop/Autotrader_db.csv", encoding='cp1252')

# create a summy field to easily facilitate totals
autotrader['count'] = 1

#c. Calculate the total car sales based on the “Numbers of owners” features
autotrader.groupby(['owners']).size().reset_index(name='counts')
order = ["Unknown", "2", "3", "4", "5", "6", "7","11"]
autotrader.groupby('owners').agg({'count' : 'sum'}).loc[order].plot(title='Adverts by number of owners',kind='bar',
               figsize=(10, 5),legend=False)


#d. What are the most popular car sales based on the “Type of cars”? 
autotrader.groupby('body_type').agg({'count' : 'sum'}).plot(title='Adverts by car body type',kind='bar',
               figsize=(20, 6),legend=False)


#e. Compare car sales on their transmission features 

####################################################
# Section 1 - Overview of sales by transmission type
####################################################

# split the file between automatic and manual sales
autotrader['car_age'] = 2020 - autotrader['reg_yr'].astype('int64')
trans_stats = autotrader.groupby('transmission').agg({'count' : 'sum', 'mileage' : 'mean', 'price' : 'mean', 'car_age' : 'mean', 'engine_size' : 'mean'}).astype('int32').reset_index()


# pie chart of automatic versus manual sales
trans_stats['count'].plot(kind='pie', figsize=(6,6), labels = trans_stats.transmission, autopct ='%1.2f%%', title = 'Proportion of manual vs. automatic transmission sales')


auto = autotrader.loc[autotrader.transmission == 'Automatic']
manual = autotrader.loc[autotrader.transmission == 'Manual']

# scatter showing price versus mileage
x_auto = auto.mileage
y_auto = auto.price
x_manu = manual.mileage
y_manu = manual.price

plt.scatter(x_auto, y_auto, label='Automatic', marker = 'o', color ='blue', s=30)
plt.scatter(x_manu, y_manu, label='Manual', marker = 'o', color ='orange', s=30)
plt.legend(loc=2) # loc specifies where to put the legend
plt.ylim((0,10000))
plt.xlabel('Mileage')
plt.ylabel('Price')
plt.title('Mileage vs price by transmission type')
plt.show


# Body type
bod_man = manual.groupby('body_type').agg({'count' : 'sum'}).reset_index()
bod_aut = auto.groupby('body_type').agg({'count' : 'sum'}).reset_index()

bods = bod_aut.merge(bod_man[['body_type', 'count']], on=['body_type'], how='outer')
bods['automatic'] = bods.count_x
bods['manual'] = bods.count_y

bars=bods[['automatic','manual']]
bars.plot(bods['body_type'], kind='bar', title = 'Sales by body type and transmission')


# Seats
seat_man = manual.groupby('numseats').agg({'count' : 'sum'}).reset_index()
seat_aut = auto.groupby('numseats').agg({'count' : 'sum'}).reset_index()

seats = seat_aut.merge(seat_man[['numseats', 'count']], on=['numseats'], how='outer')
seats['automatic'] = seats.count_x
seats['manual'] = seats.count_y

bars=seats[['automatic','manual']]
bars.plot(seats['numseats'], kind='bar', title = 'Sales by number of seats and transmission')


# Owners
own_man = manual.groupby('owners').agg({'count' : 'sum'}).reset_index()
own_aut = auto.groupby('owners').agg({'count' : 'sum'}).reset_index()

own = own_man.merge(own_aut[['owners', 'count']], on=['owners'], how='outer')
own['automatic'] = own.count_x
own['manual'] = own.count_y

own_order = ["Unknown", "2", "3", "4", "5", "6", "7", "11"]        

bars=own[['owners','automatic','manual']]
ax = bars.set_index("owners").loc[own_order].plot(kind='bar', title = 'Sales by number of owners and transmission')


# Fuel
fuel_man = manual.groupby('fuel').agg({'count' : 'sum'}).reset_index()
fuel_aut = auto.groupby('fuel').agg({'count' : 'sum'}).reset_index()

fuel = fuel_man.merge(fuel_aut[['fuel', 'count']], on=['fuel'], how='outer')
fuel['automatic'] = fuel.count_x
fuel['manual'] = fuel.count_y

bars=fuel[['automatic','manual']]
bars.plot(fuel['fuel'], kind='bar', title = 'Sales by fuel type and transmission')


####################################################
# Section 2 - Deeper dive into price differences
####################################################

#	Average price per body type
price_btype_man = manual.groupby('body_type').agg({'price' : 'mean'}).astype('int64').reset_index()
price_btype_aut = auto.groupby('body_type').agg({'price' : 'mean'}).astype('int64').reset_index()

price_btype = price_btype_man.merge(price_btype_aut[['body_type', 'price']], on=['body_type'], how='outer')
price_btype['automatic'] = price_btype.price_x
price_btype['manual'] = price_btype.price_y

bars=price_btype[['automatic','manual']]
bars.plot(price_btype['body_type'], kind='bar', title = 'Mean sale price by body type')


#	Mean age by body type
age_btype_man = manual.groupby('body_type').agg({'car_age' : 'mean'}).astype('int64').reset_index()
age_btype_aut = auto.groupby('body_type').agg({'car_age' : 'mean'}).astype('int64').reset_index()

age_btype = age_btype_man.merge(age_btype_aut[['body_type', 'car_age']], on=['body_type'], how='outer')
age_btype['automatic'] = age_btype.car_age_x
age_btype['manual'] = age_btype.car_age_y

bars=age_btype[['automatic','manual']]
bars.plot(age_btype['body_type'], kind='bar', title = 'Mean sale age by body type')

auto['price'].corr(auto['mileage'])
manual['price'].corr(manual['mileage'])



# scatter of price per 10k miles versus price per 1L of engine size
# Price per 10k miles
autotrader['price_10k_miles'] = autotrader.price / (autotrader.mileage / 10000).astype('int64')

# Price per 1L of engine size
autotrader['price_1L_engine'] = autotrader.price / autotrader.engine_size.astype('int64')

trans_stats2 = autotrader.groupby('transmission').agg({'count' : 'sum', 'price_10k_miles' : 'mean', 'price_1L_engine' : 'mean', 'car_age' : 'mean'}).astype('int32').reset_index()



# Mean price by transmission per reg year
reg_yr_price = autotrader.groupby(['transmission', 'reg_yr']).agg({'count' : 'sum', 'price' : 'mean'}).astype('int32').reset_index()

reg_yr_price_A = reg_yr_price.loc[reg_yr_price.transmission == 'Automatic']
reg_yr_price_M = reg_yr_price.loc[reg_yr_price.transmission == 'Manual']

# bar chart with sales volumes
yr_price = reg_yr_price_M.merge(reg_yr_price_A[['reg_yr', 'count']], on=['reg_yr'], how='outer')
yr_price['automatic'] = yr_price.count_x
yr_price['manual'] = yr_price.count_y
        
yr_order = [1996, 1999, 2000, 2001, 2002, 2003, 2004,
             2005,2006,2007,2008,2009,2010,2011,2013,
             2016,2017]        

bars=yr_price[['reg_yr','automatic','manual']]
ax = bars.set_index("reg_yr").loc[yr_order].plot(kind='bar', title = 'Sales volumes by reg year')


# line chart with mean price            
fig = plt.figure()
plt.plot(reg_yr_price_A['reg_yr'], reg_yr_price_A['price'], label='Automatic', color='blue', linestyle='-', linewidth=2)
plt.plot(reg_yr_price_M['reg_yr'], reg_yr_price_M['price'], label='Manual', color='orange', linestyle='-', linewidth=2)
plt.legend(loc=2) 
plt.title('Mean price by registration year')
plt.xlabel('Registraion Year')
plt.ylabel('Mean price')
plt.xticks(np.arange(min(reg_yr_price['reg_yr']), max(reg_yr_price['reg_yr'])+1, 1.0), rotation=90)
plt.show()



### Output to CSV
autotrader.to_csv('C:/Users/LMurphy/Desktop/Autotrader_db_v2.csv', index=False)



#############################################################################
#############################################################################
#########################  E-N-D  O-F  P-R-O-G-R-A-M ########################
#############################################################################
#############################################################################
