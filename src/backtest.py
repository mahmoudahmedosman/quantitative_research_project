import pandas as pd
from typing import Callable

def run_backtest(
    returns: pd.DataFrame,
    signal_fn: Callable,
    signal_kwargs: dict = {},
    top_n: int = 10,
    rebal_freq: int = 21,
    warmup: int = 300,
) -> tuple:
    dates = returns.index[warmup:]
    rebal_dates = dates[::rebal_freq]
    positions = pd.DataFrame(0.0, index=returns.index, columns=returns.columns)

    for i, date in enumerate(rebal_dates):
        signal = signal_fn(returns.loc[:date], **signal_kwargs)
        if signal.empty or signal.iloc[-1].isnull().all():
            continue
        latest = signal.iloc[-1].dropna()
        pos = pd.Series(0.0, index=returns.columns)
        n = min(top_n, len(latest) // 2)
        pos[latest.nlargest(n).index]  =  1.0 / n
        pos[latest.nsmallest(n).index] = -1.0 / n
        next_date = rebal_dates[i + 1] if i + 1 < len(rebal_dates) else returns.index[-1]
        positions.loc[date:next_date] = pos.values

    port_returns = (positions.shift(1) * returns).sum(axis=1).loc[dates]
    return port_returns, positions.loc[dates]
