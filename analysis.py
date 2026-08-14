#imports
import utils
import numpy as np 
import math
import statistics
import asyncio
import fred
import fmp
from fastapi import HTTPException
#Constants
TRADING_DAYS_PER_YEAR = 252
SHARPE_WINDOW_SESSIONS = 252     #Also min for beta
BETA_MIN =252
VOLATILITY_WINDOW_SESSIONS = 90    

#functions

#REFACTOR DATA
async def drawdown(json_data):
    peak_price = 0
    max_drawdown = 0

    for i in json_data[::-1]:
        price = i.close
        if price>peak_price: peak_price=price
        new_drawdown = ((peak_price-price)/peak_price)*100
        if new_drawdown>max_drawdown: max_drawdown = new_drawdown
    return max_drawdown

async def volatility(json_data):
    selected_dates = json_data[VOLATILITY_WINDOW_SESSIONS-1::-1]
    
    percent_changes = await utils.day_to_day_percent_change(selected_dates)

    std_prices = statistics.stdev(percent_changes)
    return std_prices*math.sqrt(TRADING_DAYS_PER_YEAR)*100
    
async def sharpe(json_data):

    standard_return = (await fred.get_treasury())/100

    daily_standard= standard_return/TRADING_DAYS_PER_YEAR

    selected_dates = json_data[SHARPE_WINDOW_SESSIONS-1::-1]

    percent_changes = await utils.day_to_day_percent_change(selected_dates)
    daily_excess = [i-daily_standard for i in percent_changes]
    sharpe_ratio = statistics.mean(daily_excess)/statistics.stdev(daily_excess)

    return sharpe_ratio*math.sqrt(TRADING_DAYS_PER_YEAR)

async def beta(json_data):
    s_and_p = (await fmp.get_price_data('SPY'))
    
    snp_changes = await utils.day_to_day_percent_change(s_and_p)
    stock_changes = await utils.day_to_day_percent_change(json_data)
    
    stock_days = len(stock_changes)

    if stock_days<BETA_MIN:
        raise HTTPException(status_code=400, detail="Stock not traded for long enough to be analyzed")
    else:
        selected_dates_snp = snp_changes[:stock_days]

        co = np.cov(selected_dates_snp, stock_changes)[0][1]
        va = np.var(selected_dates_snp)

        return co/va

