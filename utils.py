#Imports
import math
import asyncio
import httpx
from fastapi import HTTPException
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
#CONSTANTS

NY_TIMEZONE = "America/New_York"
#FUNCTIONS


#HTTPX wrapper that sends params to server and returns json from server
async def fetch(url:str, params:dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
        except Exception as e:
            raise HTTPException(status_code=502, detail="Upstream data provider error")
    return response.json()


#Returns daily percent change of stock, takes data as arg
async def day_to_day_percent_change(data):

    daily_changes=[]
    for i,day in enumerate(data[1:], start =1):
        percent_change=(math.log(day.close)-math.log(data[i-1].close))
        daily_changes.append(percent_change)
    return(daily_changes)


# Returns n previous days as list of strings: format 'year-month-day'
def prev_days(amount:int):

    ny = ZoneInfo(NY_TIMEZONE)
    ny_now = datetime.now(ny)

    recent_dates = []
    for i in range(amount):
        recent_day = (ny_now - timedelta(days=i)).date()
        recent_dates.append(recent_day.isoformat())

    return recent_dates
