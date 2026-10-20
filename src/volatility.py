"""
Volatility modelling module.

Three estimators in increasing sophistication:
  1. Rolling std      — simple, high noise
  2. EWMA             — more responsive
  3. GARCH(1,1)       — models clustering and persistence explicitly

GARCH(1,1) variance equation:
  σ²(t) = ω + α·r²(t−1) + β·σ²(t−1)

  ω > 0, α ≥ 0, β ≥ 0, α + β < 1 (stationarity)

  Long-run variance:  σ̄² = ω / (1 − α − β)
  Persistence:        α + β
  Half-life:          log(0.5) / log(α + β)  [days]
"""

import numpy as np
import pandas as pd
from arch import arch_model
from typing import Optional
import warnings
warnings.filterwarnings('ignore')


def rolling_vol(returns: pd.DataFrame, window: int = 21) -> pd.DataFrame:
    """Rolling std annualised. σ̂(t) = std[r(t-W..t)] × √252"""
    return returns.rolling(window).std() * np.sqrt(252)


def ewma_vol(returns: pd.DataFrame, lam: float = 0.94) -> pd.DataFrame:
    """
    RiskMetrics EWMA volatility.
    σ²(t) = λ·σ²(t−1) + (1−λ)·r²(t),  λ=0.94
    Annualised by ×√252.
    """
    var = returns.pow(2).ewm(alpha=1 - lam, adjust=False).mean()
    return np.sqrt(var) * np.sqrt(252)


def fit_garch(returns: pd.Series, ticker: str = "") -> Optional[dict]:
    """
    Fit GARCH(1,1) to a single return series.
    Returns dict of parameters and derived quantities, or None if fit fails.
    """
    try:
        r = returns.dropna() * 100  # scale for numerical stability
        result = arch_model(r, vol='Garch', p=1, q=1, dist='normal').fit(
            disp='off', show_warning=False)

        omega = result.params['omega']
        alpha = result.params['alpha[1]']
        beta  = result.params['beta[1]']
        pers  = alpha + beta

        half_life    = np.log(0.5) / np.log(pers) if 0 < pers < 1 else np.nan
        long_run_vol = np.sqrt(omega / (1 - pers)) * np.sqrt(252) / 100 \
                       if pers < 1 else np.nan

        return dict(ticker=ticker, omega=omega, alpha=alpha, beta=beta,
                    persistence=pers, half_life=half_life,
                    long_run_vol=long_run_vol, aic=result.aic)
    except Exception as e:
        print(f"  GARCH failed for {ticker}: {e}")
        return None


def fit_garch_universe(returns: pd.DataFrame, label: str = "") -> pd.DataFrame:
    """
    Fit GARCH(1,1) to every stock in the universe.
    Returns DataFrame: one row per stock, columns = GARCH parameters.
    """
    print(f"Fitting GARCH(1,1) [{label}] — {returns.shape[1]} stocks...")
    rows = [fit_garch(returns[t], ticker=t) for t in returns.columns]
    rows = [r for r in rows if r is not None]
    df = pd.DataFrame(rows).set_index('ticker')
    print(f"  Converged: {len(df)}/{returns.shape[1]}")
    return df


def garch_conditional_vol(returns: pd.Series) -> Optional[pd.Series]:
    """
    In-sample GARCH(1,1) conditional volatility path for one stock.
    Returns annualised σ(t) series.
    """
    try:
        r = returns.dropna() * 100
        result = arch_model(r, vol='Garch', p=1, q=1, dist='normal').fit(
            disp='off', show_warning=False)
        cv = result.conditional_volatility / 100 * np.sqrt(252)
        cv.index = r.index
        return cv
    except Exception:
        return None


def compare_universes(g_sp500: pd.DataFrame, g_spus: pd.DataFrame) -> pd.DataFrame:
    """
    Compare GARCH parameter distributions between SP500 and SPUS.
    Key table for the paper: does screening select for different vol dynamics?
    """
    params = ['alpha', 'beta', 'persistence', 'half_life', 'long_run_vol']
    rows = []
    for p in params:
        a, b = g_sp500[p].dropna(), g_spus[p].dropna()
        rows.append({
            'parameter':     p,
            'SP500 mean':    a.mean(),
            'SP500 std':     a.std(),
            'SPUS mean':     b.mean(),
            'SPUS std':      b.std(),
            'difference':    b.mean() - a.mean(),
            'rel. diff (%)': (b.mean() - a.mean()) / a.mean() * 100,
        })
    return pd.DataFrame(rows).set_index('parameter').round(4)
