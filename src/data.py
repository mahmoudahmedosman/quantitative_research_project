import pandas as pd
import yfinance as yf
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

def download_prices(tickers: list, start: str = "2010-01-01", end: str = None, cache: bool = True) -> pd.DataFrame:
    tag = end or "today"
    cache_path = DATA_DIR / f"prices_{start}_{tag}.csv"
    if cache and cache_path.exists():
        print(f"Loading from cache: {cache_path.name}")
        return pd.read_csv(cache_path, index_col=0, parse_dates=True)
    print(f"Downloading {len(tickers)} tickers...")
    raw = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=True)
    prices = raw["Close"]
    prices = prices.loc[:, prices.isnull().mean() < 0.2].ffill().dropna(how="all")
    if cache:
        prices.to_csv(cache_path)
    return prices

def compute_returns(prices: pd.DataFrame, periods: int = 1) -> pd.DataFrame:
    import numpy as np
    return np.log(prices / prices.shift(periods)).dropna()
