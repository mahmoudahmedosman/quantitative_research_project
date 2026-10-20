import numpy as np
import pandas as pd

def sharpe_ratio(returns: pd.Series, periods_per_year: int = 252) -> float:
    if returns.std() == 0: return 0.0
    return (returns.mean() / returns.std()) * np.sqrt(periods_per_year)

def max_drawdown(returns: pd.Series) -> float:
    cumulative = (1 + returns).cumprod()
    drawdown = (cumulative - cumulative.cummax()) / cumulative.cummax()
    return drawdown.min()

def annualised_return(returns: pd.Series, periods_per_year: int = 252) -> float:
    total = (1 + returns).prod()
    n_years = len(returns) / periods_per_year
    return total ** (1 / n_years) - 1

def turnover(positions: pd.DataFrame) -> pd.Series:
    return positions.diff().abs().sum(axis=1)

def net_sharpe(returns: pd.Series, positions: pd.DataFrame, cost_bps: float = 5.0, periods_per_year: int = 252) -> float:
    cost = turnover(positions) * (cost_bps / 10_000)
    return sharpe_ratio(returns - cost.reindex(returns.index).fillna(0), periods_per_year)

def summary(returns: pd.Series, positions: pd.DataFrame = None, cost_bps: float = 5.0, label: str = "") -> dict:
    tag = f"[{label}] " if label else ""
    stats = {
        f"{tag}Annualised Return":    f"{annualised_return(returns):.2%}",
        f"{tag}Sharpe (gross)":       f"{sharpe_ratio(returns):.2f}",
        f"{tag}Max Drawdown":         f"{max_drawdown(returns):.2%}",
    }
    if positions is not None:
        stats[f"{tag}Sharpe (net)"]       = f"{net_sharpe(returns, positions, cost_bps):.2f}"
        stats[f"{tag}Mean Daily Turnover"] = f"{turnover(positions).mean():.2%}"
    for k, v in stats.items():
        print(f"  {k:45s}: {v}")
    return stats
