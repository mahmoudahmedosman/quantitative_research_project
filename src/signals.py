import pandas as pd

def cross_section_zscore(df: pd.DataFrame) -> pd.DataFrame:
    return df.sub(df.mean(axis=1), axis=0).div(df.std(axis=1), axis=0)

def momentum(returns: pd.DataFrame, lookback: int = 252, skip: int = 21) -> pd.DataFrame:
    return cross_section_zscore(returns.shift(skip).rolling(lookback).sum())

def short_term_reversal(returns: pd.DataFrame, lookback: int = 5) -> pd.DataFrame:
    return cross_section_zscore(-returns.rolling(lookback).sum())

def volatility_signal(returns: pd.DataFrame, lookback: int = 21) -> pd.DataFrame:
    return cross_section_zscore(-returns.rolling(lookback).std())
