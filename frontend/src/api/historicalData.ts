import type { HistoricalData } from "../types/historical";

const BASE_URL = 'http://localhost:8000'

export async function getHistoricalData(ticker:string): Promise<HistoricalData[]> {

const url = `${BASE_URL}/stock/historical-data/${ticker}`
const response = await fetch(url)

if(response.ok){
    return response.json()
}
else{
    throw new Error(`Problem obtaining historical data:${response.status}`)
}
}
