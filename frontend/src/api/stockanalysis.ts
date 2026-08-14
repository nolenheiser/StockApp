
import type { StockAnalysis } from '../types/analysis'

const BASE_URL = 'http://localhost:8000'

export async function getStockAnalysis(ticker:string): Promise<StockAnalysis> {

const url = `${BASE_URL}/stock/analysis/${ticker}`

const response = await fetch(url)

if (response.ok){
    return response.json()
}
else{
    throw new Error(`Bad response: ${response.status}`)
}
}