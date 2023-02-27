# %%
'''
A seperate script for generating relevant plots
'''
# imports
import pandas as pd
from plotnine import ggplot, geom_point, aes, scale_x_continuous, theme_bw, ggtitle, geom_col, theme, element_text
from datetime import datetime
import os

# constants
TODAYS_DATE = datetime.today().strftime("%d-%m-%Y")

# plot data


class plotCoordinator():
    '''
    A class to handle the plotting of data
    '''

    def __init__(self):
        self.pricesPerth = pd.read_csv(f'data/{TODAYS_DATE}-pricesPerth.csv')

    def checkPlotExists(self, plotName, forceTrue=False):
        '''
        Checks if a plot exists already
        '''
        if forceTrue:
            return True
        elif os.path.exists(f'images/{TODAYS_DATE}-{plotName}.png'):
            print(f'{plotName} already exists')
            return True
        else:
            return False

    # create a plot of prices vs lattitude
    def pricesByLatitude(self):
        '''
        Plot of longitude vs latitude coloured by price
        '''
        plotName = 'pricesByLatitude'
        # check if pricesByLatitude exists already for today
        if not self.checkPlotExists(plotName):
            pricesByLatitude = (ggplot(self.pricesPerth, aes(x='latitude', y='price', color='brand'))
                                + geom_point()
                                + ggtitle("Prices vs latitude coloured by brand")
                                )
            pricesByLatitude.save(
                f'images/{TODAYS_DATE}-pricesByLatitude.png', height=10, width=15)

    def brandsBarPlot(self):
        plotName = 'brandsBarPlot'
        if not self.checkPlotExists(plotName):
            brandsBarPlot = (
                ggplot(self.pricesPerth, aes(x="brand", y="price")) +
                geom_col() +
                theme(axis_text_x=element_text(rotation=90, hjust=1))
            )
            brandsBarPlot.save(
                f'images/{TODAYS_DATE}-brandsBarPlot.png', height=10, width=15)

    def pricesMap(self):
        plotName = 'pricesMap'
        if not self.checkPlotExists(plotName):
            pricesMap = (
                ggplot(self.pricesPerth, aes(y="latitude", x="longitude", colour="price")) +
                geom_point() +
                scale_x_continuous(breaks=[1, 100]) +
                theme_bw() +
                ggtitle("Prices by location around Perth")
            )
            pricesMap.save(
                f'images/{TODAYS_DATE}-pricesMap.png', height=10, width=15)

    def allPlots(self):
        '''
        Fires off all plots
        '''
        self.pricesByLatitude()
        self.brandsBarPlot()
        self.pricesMap()
        print('All plots generated')

# init function


def init():
    '''
    Initialise the plotting script
    '''
    # create an instance of the class
    plotter = plotCoordinator()
    plotter.allPlots()


if __name__ == '__main__':
    init()

# %%
