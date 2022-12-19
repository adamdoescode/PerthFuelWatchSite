#%%
import feedparser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plotnine import ggplot, geom_point, aes, stat_smooth, facet_wrap

def get_fuel(product_id, region_id):
    query: str = 'http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?'
    query = query + 'Product='+str(product_id)+f'&Region={region_id}'
    data = feedparser.parse(query)
    return data['entries']

def getFuelReturnDf(dataFromRSS):
    '''
    Iterate through output to get pandas df
    '''
    res: dict = {
        colName:[] for colName in ['title','price','brand','latitude','longitude']
    }
    for station in dataFromRSS:
        res['title'].append(station['title'])
        res['price'].append(station['price'])
        res['brand'].append(station['brand'])
        res['latitude'].append(station['latitude'])
        res['longitude'].append(station['longitude'])
    return pd.DataFrame(res)

ulpNORToday = get_fuel(1, 25)
ulpSORToday = get_fuel(1, 26)
pricesNOR = getFuelReturnDf(ulpNORToday)
pricesSOR = getFuelReturnDf(ulpSORToday)

pricesNOR.loc[:,'title'] = pricesNOR['title'].str.split(': ').str[-1]
pricesSOR.loc[:,'title'] = pricesSOR['title'].str.split(': ').str[-1]
pricesNOR = pricesNOR.sort_values(by='price', ascending=True)
pricesSOR = pricesSOR.sort_values(by='price', ascending=True)
pricesNOR.price = pricesNOR.price.astype(float)
pricesSOR.price = pricesSOR.price.astype(float)
print('SOR=',np.mean(pricesSOR.price))
print('NOR=',np.mean(pricesNOR.price))

pricesPerth = pd.concat([pricesNOR, pricesSOR])

pricesHTML = pricesPerth.to_html()

with open('header.html', 'r') as f:
    headerHTML = f.read()

headerHTML = headerHTML.replace('<!-- insert table here -->', pricesHTML)
# write to index.html
with open('index.html', 'w') as outputfile:
    outputfile.write(headerHTML)
