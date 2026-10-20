# Systematic Equity Signals in Sharia-Compliant vs Unconstrained Universes

**Author:** Mahmoud Osman  
**Background:** PhD in Physical Cosmology, Sorbonne Université / LPNHE / CNRS (2026)  
**Status:** Work in progress — Part 1 complete, Parts 2–4 in development

---

## Motivation

There is almost no publicly available, rigorous quantitative research on Sharia-compliant equity universes. This project applies the same statistical methodology used in observational cosmology — rigorous out-of-sample validation, honest uncertainty quantification, and transparent reporting of null results — to the question of whether systematic investing is viable within Islamic finance constraints.

The project is also a personal bridge between my PhD work in Bayesian field-level inference and the quantitative finance industry. The methodology transfers directly: characterise the data before modelling it, validate out-of-sample, and be intellectually honest when results do not match expectations.

---

## Project Structure

```
quant-research/
├── data/                          # Cached market data (not tracked by Git)
├── notebooks/
│   ├── 01_universe_comparison.ipynb   # Universe characterisation
│   ├── 02_volatility.ipynb            # GARCH volatility modelling
│   ├── 03_signals_IC.ipynb            # Signal IC analysis ← current
│   ├── 04_strategies.ipynb            # Backtested strategies (in progress)
│   ├── 05_market_modelling.ipynb      # PCA / surface fitting (planned)
│   └── 06_simulation_inference.ipynb  # SBI market simulation (long-term)
├── src/
│   ├── universe.py    # Universe definitions and Sharia screening
│   ├── data.py        # Data loading and caching
│   ├── signals.py     # Momentum, reversal, volatility signals
│   ├── backtest.py    # Walk-forward backtesting engine
│   ├── metrics.py     # Sharpe, drawdown, turnover, net Sharpe
│   └── volatility.py  # Rolling, EWMA, GARCH(1,1) estimators
├── requirements.txt
└── README.md
```

---

## Universes

| Universe | Description | N stocks |
|---|---|---|
| SP500 | Full S&P 500 (Wikipedia, live fetch) | ~470 |
| SPUS | Sharia-screened: Stage 1 business activity exclusions | ~392 |
| Diff | Excluded companies (SP500 − SPUS) | ~78 |

**Sharia screening (Stage 1)** excludes companies with material revenue from: conventional banking and insurance, alcohol, tobacco, gambling, weapons manufacturing, pork, and adult entertainment. Stage 2 financial ratio screens (debt/market cap < 33%) are not yet applied — this is noted as a limitation and planned for Part 1b.

---

## Results

### Part 1a — Universe Characterisation and Signal Analysis (2015–2026)

**Return and risk metrics**

Mean annualised returns are 5.81% ± 8.97% for SP500, 6.09% ± 9.31% for SPUS, and 2.12% ± 3.38% for the excluded companies. While SPUS shows a marginally higher mean return, this difference is not statistically significant (p=0.65). Both SP500 and SPUS significantly outperform the excluded universe (p=0.0002 and p=0.0004 respectively), whose lower returns reflect the underperformance of conventional financials, REITs, and defence stocks over this period.

Mean Sharpe ratios are similar across all three groups (SP500: 0.35 ± 0.23, SPUS: 0.36 ± 0.24, Diff: 0.31 ± 0.20), with all values within one standard deviation of each other. Maximum drawdown is near-identical across universes (approximately −59%), indicating that Sharia screening provides no protection against market-wide tail risk.

**Signal analysis**

We evaluate momentum, short-term reversal, and volatility signals using Spearman rank correlation and Pearson correlation between signal scores and 21-day forward returns.

*Momentum* shows no significant rank-predictive power under Spearman (p=0.36/0.29), but significant magnitude predictability under Pearson (p=0.002/0.0003). This divergence indicates a non-linear relationship concentrated in the tails — extreme momentum stocks outperform meaningfully while the bulk of the ranking carries little signal. SPUS shows marginally stronger momentum IC under Pearson (0.018 vs 0.015).

*Volatility* produces a significantly negative IC in both universes (Spearman IC ≈ −0.034, p<0.001; Pearson IC ≈ −0.040, p<0.001). High-volatility stocks outperform low-volatility stocks at the 21-day horizon — a horizon effect: at short horizons in trending markets, high-volatility stocks generate larger moves that are more often positive. The low-volatility premium documented in the literature manifests at longer horizons on a risk-adjusted basis. SP500 and SPUS produce virtually identical results (comparison p=0.999).

*Short-term reversal* is the most robust signal, exhibiting significant rank-predictive power in both universes under Spearman (SP500: IC=0.012, p=0.0004; SPUS: IC=0.011, p=0.001). Under Pearson, reversal magnitude is significant for SP500 (p=0.023) but not for SPUS (p=0.12), suggesting that excluded financial stocks contribute disproportionately to magnitude predictability of the reversal signal.

**Key finding**

Across all three signals and both methods, direct comparison of IC series between SP500 and SPUS yields p-values above 0.6 in every case (Spearman: momentum p=0.93, volatility p=0.999, reversal p=0.79; Pearson: momentum p=0.72, volatility p=0.92, reversal p=0.62). The signal predictive structure is statistically identical between the two universes. **Sharia screening removes a specific underperforming segment of the market while leaving the return-generating structure of the remaining universe entirely intact.**

---

## Roadmap

| Part | Description | Status |
|---|---|---|
| 1a | Universe characterisation and signal IC analysis | ✅ Complete |
| 1b | Stage 2 financial ratio screening | 🔜 Planned |
| 2 | Systematic strategies: long-only momentum, low-vol, combined signal, risk parity on SPUS | 🔜 In progress |
| 3 | Market modelling: PCA and surface fitting in (return, volatility, momentum) space | 🔜 Planned |
| 4 | Simulation-based inference: BORG-inspired market simulator with principled priors | 🔬 Long-term |

---

## Methodological Notes

- **No lookahead bias**: signals computed from past data only at each evaluation date
- **Walk-forward validation**: train on rolling window, test on next period (Parts 2+)
- **Transaction costs modelled**: 5 bps one-way (Parts 2+)
- **Uncertainty reported**: all metrics accompanied by standard deviations and p-values
- **Null results documented**: non-significant findings reported alongside significant ones
- **Reproducible**: all data sourced from public APIs (yfinance, Wikipedia)

---

## Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/quant-research.git
cd quant-research

# Create environment
conda create -n quant python=3.11 -y
conda activate quant

# Install dependencies
pip install -r requirements.txt

# Register kernel and launch Jupyter
python -m ipykernel install --user --name quant --display-name "quant"
jupyter notebook
```

---

## Dependencies

Python 3.11, pandas, numpy, yfinance, matplotlib, seaborn, scipy, statsmodels, arch, scikit-learn, tensorflow, jupyter

---

## Connection to PhD Work

This project explicitly bridges my doctoral research and quantitative finance:

- **Signal validation methodology** mirrors the out-of-sample validation used in the NaCl spectrophotometric pipeline
- **GARCH volatility inference** is analogous to latent parameter estimation in Bayesian forward models
- **Part 3 (PCA / surface fitting)** directly applies the dimensionality reduction and regularised fitting techniques from NaCl to financial data
- **Part 4 (simulation-based inference)** is a BORG-inspired framework: simulate market dynamics from initial conditions, let the system evolve under realistic agent interactions, and infer latent parameters by matching observed price statistics — the financial analogue of reconstructing the 3D matter field from galaxy observations

---

## Citation

If you use this code or results, please cite:

```
Osman, M. (2026). Systematic Equity Signals in Sharia-Compliant vs
Unconstrained Universes. GitHub repository.
https://github.com/<your-username>/quant-research
```

---

## Disclaimer

This project is academic research. Nothing here constitutes financial advice.
All results are based on historical data and do not guarantee future performance.
