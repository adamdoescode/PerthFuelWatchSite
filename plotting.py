#%%
'''
A seperate script for generating relevant plots
'''
#imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plotnine import ggplot, geom_point, aes, stat_smooth, facet_wrap, scale_x_continuous, theme_bw, ggtitle, geom_col, scale_x_discrete, theme, element_text
from datetime import datetime
import os

#constants
TODAYS_DATE = datetime.today().strftime("%d-%m-%Y")

#plot data
class plotCoordinator():
    '''
    A class to handle the plotting of data
    '''
    def __init__(self):
        self.pricesPerth = pd.read_csv(f'data/{TODAYS_DATE}-pricesPerth.csv')
    
    def checkPlotExists(self, plotName):
        '''
        Checks if a plot exists already
        '''
        if os.path.exists(f'images/{TODAYS_DATE}-{plotName}.png'):
            print(f'{plotName} already exists')
            return True
        else:
            return False

    # create a plot of prices vs lattitude
    def plotNOR_SOR(self):
        '''
        Plot of longitude vs latitude coloured by price
        '''
        plotName = 'plotNOR_SOR'
        #check if plotNOR_SOR exists already for today
        if not self.checkPlotExists(plotName):
            plotNOR_SOR = (ggplot(self.pricesPerth, aes(x='latitude', y='price', color='brand'))
                + geom_point()
                + ggtitle("Prices vs latitude coloured by brand")
                )
            plotNOR_SOR.save(f'images/{TODAYS_DATE}-plotNOR_SOR.png', height=10, width=15)

    def brandsBarPlot(self):
        plotName = 'brandsBarPlot'
        if not self.checkPlotExists(plotName):
            brandsBarPlot = (
                ggplot(self.pricesPerth, aes(x="brand", y="price")) +
                geom_col() +
                theme(axis_text_x=element_text(rotation=90, hjust=1))
            )
            brandsBarPlot.save('images/{TODAYS_DATE}-brandsBarPlot.png', height=10, width=15)

    def pricesHeatMap(self):
        plotName = 'pricesHeatMap'
        if not self.checkPlotExists(plotName):
            pricesHeatMap = (
                ggplot(self.pricesPerth, aes(y="latitude",x="longitude", colour = "price")) +
                geom_point() + 
                scale_x_continuous(breaks = [1,100]) +
                theme_bw() +
                ggtitle("Prices by location around Perth")
            )
            pricesHeatMap.save('images/{TODAYS_DATE}-pricesHeatMap.png', height=10, width=15)
    
    def allPlots(self):
        '''
        Fires off all plots
        '''
        self.plotNOR_SOR()
        self.brandsBarPlot()
        self.pricesHeatMap()
        print('All plots generated')

#init function
def init():
    '''
    Initialise the plotting script
    '''
    #create an instance of the class
    plotter = plotCoordinator()
    plotter.allPlots()

if __name__ == '__main__':
    init()

# %%
