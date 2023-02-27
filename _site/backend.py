# %%
import feedparser
import pandas as pd
from datetime import datetime
import plotting


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
        colName: [] for colName in ['title', 'price', 'brand', 'latitude', 'longitude']
    }
    for station in dataFromRSS:
        res['title'].append(station['title'])
        res['price'].append(station['price'])
        res['brand'].append(station['brand'])
        res['latitude'].append(station['latitude'])
        res['longitude'].append(station['longitude'])
    return pd.DataFrame(res)


def formatData(df: pd.DataFrame):
    '''
    Takes input data and formats it, should work for any ULP data by default
    '''
    df.loc[:, 'title'] = df['title'].str.split(': ').str[-1]
    df = df.sort_values(by='price', ascending=True)
    df.price = df.price.astype(float)
    df.latitude = df.latitude.astype(float)
    df.longitude = df.longitude.astype(float)
    return df


def tagLoc(df: pd.DataFrame, locationTag: str):
    '''
    Takes a df and adds a location tag column
    '''
    df.loc[:, 'location'] = locationTag
    return df


def retrieveData():
    '''
    Function to retrieve data, format it, and save output to csv.
    Currently hardcoded for perth...
    '''
    ulpNORToday = get_fuel(1, 25)
    ulpSORToday = get_fuel(1, 26)
    pricesNOR = getFuelReturnDf(ulpNORToday)
    pricesSOR = getFuelReturnDf(ulpSORToday)
    # add location tags
    pricesNOR = tagLoc(pricesNOR, 'NOR')
    pricesSOR = tagLoc(pricesSOR, 'SOR')
    # concatenate rowwise as we have the same columns in both SOR and NOR
    pricesPerth = pd.concat([pricesNOR, pricesSOR])
    # modify dataframe using formatData()
    pricesPerth = formatData(pricesPerth)
    # save output to a file for posterity
    pricesPerth.to_csv(f'data/{TODAYS_DATE}-pricesPerth.csv', index=False)
    return pricesPerth


# useful constants
TODAYS_DATE = datetime.today().strftime("%d-%m-%Y")

# check if pricesPerth already exists
if 'pricesPerth' in globals():
    print('pricesPerth already exists')
else:
    # create it
    pricesPerth = retrieveData()
# %%
makePlots = plotting.plotCoordinator()
makePlots.allPlots()
# %%


def injectIntoHTML():
    '''
    Function to inject data into html
    '''
    pricesPerthHTML = pricesPerth.to_html(index=False)

    with open('header.html', 'r') as f:
        headerHTML = f.read()
    headerHTML = headerHTML.replace('<!-- insert_date -->', TODAYS_DATE)

    headerHTML = headerHTML.replace(
        '<!-- insert table here -->', pricesPerthHTML)
    # write img link
    # headerHTML = headerHTML.replace('<!-- insert table here -->', pricesPerthHTML)
    # write to index.html
    with open('index.html', 'w') as outputfile:
        outputfile.write(headerHTML)


injectIntoHTML()
# %%
