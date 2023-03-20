'''
Interfaces with osrm docker image for fuel directions
eg: curl "http://127.0.0.1:5000/route/v1/driving/115.8264304,-31.9552672;116.070139,-32.182278?steps=true"
'''
#%%
import requests
import json
import pandas as pd

def getDirections(startLat, startLon, endLat, endLon):
    '''
    Takes start and end coordinates and returns a json object with directions
    '''
    commandURL = (
        f'http://127.0.0.1:5000/route/v1/driving/'
        f'{startLon},{startLat};{endLon},{endLat}?steps=true'
    )
    response = requests.get(commandURL)
    return response.json()

coords = {
    "startLon": 115.8264304,
    "startLat": -31.9552672,
    "endLon": 116.070139,
    "endLat": -32.182278
}

drivingDirections = getDirections(**coords)
# %%

# to get total distance covered...
drivingDirections['routes'][0]['distance']

# %%
