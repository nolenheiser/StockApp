#IMPORTS
import os
import analysis
import finnhub, fmp, fred
from fastapi import FastAPI, HTTPException, Request 
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

#Setup
#App and rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

#Cors middleware (Allows front end to access backend)
allowed_origins_raw = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
origins = allowed_origins_raw.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,"https://stock-app-steel-pi.vercel.app",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Endpoints
@app.get('/')
async def root():
    return{"Home page"}


# Current price
@app.get('/stock/{ticker}')
@limiter.limit("60/minute")
async def price(request: Request, ticker:str):
    return await finnhub.get_stock_price(ticker)

# Market Status
@app.get('/market/{exchange}')
@limiter.limit("60/minute")
async def status(request:Request, exchange:str):
    return await finnhub.get_status(exchange)

#Historical data
@app.get('/stock/historical-data/{ticker}')
@limiter.limit("10/minute")
async def historical(request: Request, ticker:str):
    return await fmp.get_price_data(ticker)



#Risk Analysis

@app.get('/stock/analysis/{ticker}')
@limiter.limit("10/minute")
async def stock_analysis(request: Request, ticker:str):
    json_data = await fmp.get_price_data(ticker)
    factors = {
        'drawdown': await analysis.drawdown(json_data),
        'volatility': await analysis.volatility(json_data),
        'beta': await analysis.beta(json_data),
        'sharpe': await analysis.sharpe(json_data)
    }
    return factors