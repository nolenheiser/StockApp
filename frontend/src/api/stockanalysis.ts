
import type { StockAnalysis } from '../types/analysis'

export async function getStockAnalysis(ticker:string): Promise<StockAnalysis> {
const VITE_API_URL = import.meta.env.VITE_API_URL;

const url = `${VITE_API_URL}/stock/analysis/${ticker}`

const response = await fetch(url)

if (response.ok){
    return response.json()
}
else{
    throw new Error(`Bad response: ${response.status}`)
}
}