import type { HistoricalData } from "../types/historical";

const API_URL = import.meta.env.VITE_API_URL;

export async function getHistoricalData(ticker:string): Promise<HistoricalData[]> {

const url = `${API_URL}/stock/historical-data/${ticker}`
const response = await fetch(url)

if(response.ok){
    return response.json()
}
else{
    throw new Error(`Problem obtaining historical data:${response.status}`)
}
}
