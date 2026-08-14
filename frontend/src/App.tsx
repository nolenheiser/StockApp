import { useState } from 'react'
import './App.css'
import type { HistoricalData } from './types/historical'
import { useStockAnalysis } from './hooks/usestockanalysis'
import { useHistoricalData } from './hooks/useHistoricalData'
import { LineChart, XAxis,YAxis,Line,CartesianGrid, Tooltip,Legend} from 'recharts'
import { useMemo } from 'react'
import { allowedTickers } from './constants'
import express from 'express';
import cors from 'cors';


//Cors
const app = express();

app.use(cors({
  origin: 'https://stock-app-steel-pi.vercel.app'
}));

function App() {
  const [inputValue, setInputValue] = useState("SPY")
  const [tickers, setTickers] = useState<string[]>(["SPY"])
  const analysisResults = useStockAnalysis(tickers)
  const historicalResults = useHistoricalData(tickers)
  const [errorMessage, setErrorMessage] =useState("")

const allChartData: HistoricalData[][] = useMemo(() => {
  const result: HistoricalData[][] = []
  for (let i = 0; i < historicalResults.length; i++) {
    const item = historicalResults[i]
    if (item.data) {
      result.push([...item.data].reverse())
    } else {
      result.push([])
    }
  }
  return result
}, [historicalResults])



const mergedChartData= useMemo(() =>{
  const lookup: Record<string, any> ={}
  for(let i=0; i<tickers.length;i++){
  const ticker = tickers[i]
  const data = allChartData[i]

  for(let j=0;j<data.length;j++){
  const dateEntry = data[j]
  if(!lookup[dateEntry.date]){
    lookup[dateEntry.date]={date:dateEntry.date}
  }
  lookup[dateEntry.date][ticker] = dateEntry.close
}
}
 return Object.values(lookup)
},[tickers,allChartData])

const smallerData= useMemo(()=>{
  return mergedChartData.filter((_,index) => index%5==0)

},[mergedChartData])


const colors = ["#e81a9c", "#1a9ce8", "#9ce81a", "#e89c1a"]

const chart = (
  <div className='chartSection'>
  <LineChart data={smallerData} width={1000} height={400}>
    <Tooltip />
    <Legend />
    <CartesianGrid strokeDasharray="3 3" />
    <XAxis dataKey="date" tick={{ fontSize: 12 }} />
    <YAxis />
    {tickers.map((ticker, index) => (
      <Line key={ticker} dataKey={ticker} stroke={colors[index % colors.length]} strokeWidth={2} dot={false} />
    ))}
  </LineChart>
  </div>
)



 const analysisReturn = analysisResults.map((result, index) => {
  const ticker = tickers[index]
  
    if(result.isLoading){
       return <p className='loadingPage' key={ticker}>Loading... </p>
    }
    else if(result.error){
      if(result.error.message.includes("400")){
         return <p className='error400' key={ticker}>Error code: 400, Bad Request</p>
      }
      else if(result.error.message.includes("429")){
        return <p className='error429' key={ticker}>Error code: 429, Request limit reached</p>
      }
      else if(result.error.message.includes("502")){
        return <p className='error502' key={ticker}>Error code: 502, Data provider error</p>
      }
      else{
        return <p className='genericError' key={ticker}>Something went wrong</p>
      }
    }
    else if(result.data){
      return  (<div className='analysisStats' 
                key={ticker}>
                <h3>{ticker}</h3>
                <p>drawdown:{result.data.drawdown.toFixed(2)}%</p>
                <p>volatility:{result.data.volatility.toFixed(2)}%</p>
                <p>sharpe:{result.data.sharpe.toFixed(2)}</p>
                <p>beta:{result.data.beta.toFixed(2)}</p>
              </div>)
    }
})



  return(
      <div className='app'>
        <div className='buttonsInputs'>
        <input value={inputValue} onChange={(e) => setInputValue(e.target.value)}maxLength={10}/>
        <button onClick={() => 
          {if(tickers.includes(inputValue))
            {
            setErrorMessage(`${inputValue} already included`)
            setTimeout(()=>setErrorMessage(""), 3000)
            }
          else if(!allowedTickers.includes(inputValue))
            {
            setErrorMessage(`${inputValue} is not an accepted input`)
            setTimeout(()=>setErrorMessage(""), 3000)
          }
          else if (tickers.length >= 5) {
            setErrorMessage("Maximum of 5 tickers, reset to add more")
            setTimeout(() => setErrorMessage(""), 3000)
          }
        else{setTickers([...tickers, inputValue])}}
        }>Search</button>
        <button onClick={() => setTickers(["SPY"])}>Reset</button>
        {errorMessage && <p className='tickerError'>{errorMessage}</p>}
        </div>
        {analysisReturn}
        {chart}
      </div>
  )
  
}
export default App