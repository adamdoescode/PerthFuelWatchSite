#%%
import feedparser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plotnine import ggplot, geom_point, aes, stat_smooth, facet_wrap, scale_x_continuous, theme_bw, ggtitle, geom_col, scale_x_discrete, theme, element_text
from datetime import datetime
#%%
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
#%%
pricesNOR.loc[:,'title'] = pricesNOR['title'].str.split(': ').str[-1]
pricesSOR.loc[:,'title'] = pricesSOR['title'].str.split(': ').str[-1]
pricesNOR = pricesNOR.sort_values(by='price', ascending=True)
pricesSOR = pricesSOR.sort_values(by='price', ascending=True)
pricesNOR.price = pricesNOR.price.astype(float)
pricesSOR.price = pricesSOR.price.astype(float)
pricesNOR.latitude = pricesNOR.latitude.astype(float)
pricesSOR.latitude = pricesSOR.latitude.astype(float)
pricesNOR.longitude = pricesNOR.longitude.astype(float)
pricesSOR.longitude = pricesSOR.longitude.astype(float)
print('SOR=',np.mean(pricesSOR.price))
print('NOR=',np.mean(pricesNOR.price))

pricesPerth = pd.concat([pricesNOR, pricesSOR])

#save output to a file for posterity
pricesPerth.to_csv(f'data/{datetime.today().strftime("%d-%m-%Y")}-pricesPerth.csv')
# create a plot of prices vs lattitude
plotNOR_SOR = (ggplot(pricesPerth, aes(x='latitude', y='price', color='brand'))
    + geom_point()
    + ggtitle("Prices vs latitude coloured by brand")
    )
plotNOR_SOR.save('images/plotNOR_SOR.png', height=10, width=15)

# %%
brandsBarPlot = (
    ggplot(pricesPerth, aes(x="brand", y="price")) +
    geom_col() +
    theme(axis_text_x=element_text(rotation=90, hjust=1))
)
brandsBarPlot.save('images/brandsBarPlot.png', height=10, width=15)
# %%
pricesHeatMap = (
    ggplot(pricesPerth, aes(y="latitude",x="longitude", colour = "price")) +
    geom_point() + 
    scale_x_continuous(breaks = [1,100]) +
    theme_bw() +
    ggtitle("Prices by location around Perth")
)
pricesHeatMap.save('images/pricesHeatMap.png', height=10, width=15)

#%%
pricesHTML = pricesPerth.to_html()


with open('header.html', 'r') as f:
    headerHTML = f.read()
headerHTML = headerHTML.replace('<!-- insert_date -->' ,datetime.today().strftime('%d/%m/%Y'))

headerHTML = headerHTML.replace('<!-- insert table here -->', pricesHTML)
#write img link
# headerHTML = headerHTML.replace('<!-- insert table here -->', pricesHTML)
# write to index.html
with open('index.html', 'w') as outputfile:
    outputfile.write(headerHTML)

# %%
