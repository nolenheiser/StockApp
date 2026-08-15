# StockApp

Full stack stock app. Provides risk analysis (sharpe,beta,volatility,drawdown) as well as a chart to directly compare stock pricing over past 5 years.

## Live demo links
* note startup may take some time based on render free tier
Backend: https://stockapp-f4dh.onrender.com
Frontend: https://stock-app-git-main-nolenheiser1.vercel.app/

## Features
Single-stock analysis
Backend calculates sharpe, beta, volatilty and drawdown. for any alloqws tickers


Multi-Stock
Supports up to 5 tickers at once each paired with own single-stock analysis card.
Each stock appears on a shared chart with its own color and a legend


Input Validation
Tickers are validated before they are passed to backend to make sure data can be pulled
If a stock is no longer available an error is thrown.
Duplicate tickers are not allowed

Error codes
distinct messages for bad input (400), rate limiting (429), and upstream data provider failures (502)


## Tech-stack
### Backend
Python, FastAPI
FMP — historical price data
Finnhub — real-time price data
FRED — 10-year Treasury rate (used for Sharpe calculation)
slowapi — rate limiting
In-memory cache
Deployed on Render

### Frontend
React, TypeScript, Vite
TanStack Query
Recharts
Deployed on Vercel

## Methodology (for risk analysis)
Returns: daily percent changes are calculated logarithmically
Volatility: standard deviation of daily log returns over a 90-day window.
Sharpe ratio: mean daily excess return (daily risk free rate is pulled from FRED) divided by the standard deviation of excess returns.
              Uses 252 day window (standard number of market days in a year)
Beta: covariance of a stocks returns compared to SPY(market that follows the S&P 500), stock must have at least 90 data points to qualify for beta calculation
Drawdown: maximum peak-to-trough decline over the full 5-year window.
Data window: Maximum length of data return is 5 years (per FMP)
Tickers allowed: FMP only allows certain tickers to be request due to the free tier being used for this project


## Prerequisites 

Python 3.10+
Node.js 18.0+ 
npm


## License

Distributed under the MIT License. See `LICENSE` for details.







