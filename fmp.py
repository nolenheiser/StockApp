#IMPORTS
import cache
import constants
import asyncio
import httpx
import os
import utils
from fastapi import HTTPException
from dotenv import load_dotenv
from schema import PriceNormalized

#CONFIG
load_dotenv()

#CONSTANT

PREV_DAYS = 7
API_KEY = os.getenv("FMP_API_KEY")
BASE_URL = 'https://financialmodelingprep.com'

#FUNCTIONS
#Returns list of pydantic objects listing close price and date
async def get_price_data(symbol:str):
    if symbol not in constants.FMP_ALLOWED_TICKERS:
        raise HTTPException(status_code=400, detail="unavailable stock")
    prev_days = utils.prev_days(PREV_DAYS)


    if symbol in cache._cache and cache._cache[symbol]['cached_at'] == prev_days[0]:

        return cache._cache[symbol]['data']

    url = f"{BASE_URL}/stable/historical-price-eod/dividend-adjusted"
    params={
        "symbol":symbol,
        "apikey": API_KEY
    }

    response = await utils.fetch(url,params)
    
    if response[0]['date'] not in prev_days:
        raise HTTPException(status_code=400, detail="Stock not currently traded.")
    else:
        data = [PriceNormalized(date = i['date'], close = i['adjClose']) for i in response]
        cache._cache[symbol] = {'data':(data), 'cached_at':prev_days[0]}
        return data
