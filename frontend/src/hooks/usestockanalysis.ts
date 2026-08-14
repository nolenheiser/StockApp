import { getStockAnalysis } from "../api/stockanalysis";
import { useQueries } from "@tanstack/react-query";

export function useStockAnalysis(tickers: string[]) {
  return useQueries({
    queries: tickers.map((t) => ({
      queryKey: ['stockAnalysis', t],
      queryFn: () => getStockAnalysis(t),
    }))
  })
}
