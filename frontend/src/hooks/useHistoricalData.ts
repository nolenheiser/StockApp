import { getHistoricalData } from "../api/historicalData";
import { useQueries } from "@tanstack/react-query";

export function useHistoricalData(tickers: string[]) {
  return useQueries({
    queries: tickers.map((t) => ({
      queryKey: ['historicalData', t],
      queryFn: () => getHistoricalData(t),
    }))
  })
}