#IMPORTS
import asyncio
import httpx
import os
from dotenv import load_dotenv
import utils

#CONFIG
load_dotenv()

API_KEY=os.getenv("FREDS_API_KEY")
URL='https://api.stlouisfed.org/fred/series/observations'

#Functions

#Pulls standard return of US treasury bond over 10 years
async def get_treasury():

    params ={
        'series_id':'DGS10',
        'api_key':API_KEY,
        'file_type':'json',
        'sort_order':'desc',
        'limit':20
    }
    receipt = (await utils.fetch(URL,params))['observations']
    for i in receipt:
        if i['value'] != '.':
            return float(i['value'])
    else:
        raise ValueError("No valid treasury rates could be found")
