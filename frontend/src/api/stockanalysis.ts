
import type { StockAnalysis } from '../types/analysis'

const API_URL = import.meta.env.VITE_API_URL;

export async function getStockAnalysis(ticker:string): Promise<StockAnalysis> {

const url = `${API_URL}stock/analysis/${ticker}`

const response = await fetch(url)

if (response.ok){
    return response.json()
}
else{
    throw new Error(`Bad response: ${response.status}`)
}
}