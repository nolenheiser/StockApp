#IMPORTS
import asyncio
import httpx
import os
from dotenv import load_dotenv
import utils

#CONFIG
load_dotenv()

#CONSTANTS
API_KEY = os.getenv("FINNHUB_API_KEY")
BASE_URL = "https://finnhub.io/api/v1"

#FUNCTIONS

#Pulls stock price, currently does more than js that : NEEDS SPECIFICATION STILL
async def get_stock_price(symbol:str):
    url = f"{BASE_URL}/quote"
    params = {
        "symbol": symbol,
        "token": API_KEY
    }
    return await utils.fetch(url,params)

#Gets all holidays for given exchange : NEEDS SPECIFICATION STILL
async def get_holidays(exchange:str):
    url = f"{BASE_URL}/stock/market-holiday"
    params = {
        "exchange":exchange,
        "token": API_KEY
        }
    return await utils.fetch(url,params)
    
#Gets market status as well as other market details: NEEDS SPECIFICATION STILL
async def get_status(exchange:str):
    url = f"{BASE_URL}/stock/market-status"
    params = {
        "exchange":exchange,
        "token": API_KEY
        }
    return await utils.fetch(url,params)
