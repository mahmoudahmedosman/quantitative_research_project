# Systematic Equity Signals in Sharia-Compliant vs Unconstrained Universes

**Author:** Mahmoud Osman  
**Background:** PhD in Physics (Cosmology), Sorbonne Université / LPNHE / CNRS (2026)  
**Status:** Work in progress — Part 1 complete, Parts 2–4 in development

\---

## Motivation

There is little publicly available, rigorous quantitative research on Islamically, Sharia-compliant equity universes. This project applies rigorous statistical methodology to the question of whether systematic investing is viable within Islamic finance constraints. The project is also a personal bridge between my PhD work and the quantitative finance industry. The methodology transfers directly: characterise the data before modelling it, validate out-of-sample, and be intellectually honest when results do not match expectations.

\---

## Project Structure

```
quant-research/
├── data/                          # Cached market data (May not be included in the Git)
├── notebooks/
│   ├── 01_traditional_signals.ipynb   # Quick look at traditional signals used
│   ├── 02_systematic_study.ipynb      # Systematic studies of S\&P500 vs SPUS (Phase 1 complete)
│   ├── 03_strategies_models.ipynb     # Backtesting strategies and validating models (planned)
│   └── 04_simulation_inference.ipynb  # Simulation-based inference market simulation (planned for long term)
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

\---

## Universes

|Universe|Description|N stocks|
|-|-|-|
|SP500|Full S\&P 500 (Wikipedia, live fetch)|\~470|
|SPUS|Sharia-screened: Stage 1 business activity exclusions|\~392|
|Diff|Excluded companies (SP500 − SPUS)|\~78|

**Sharia screening (Stage 1)** excludes companies with material revenue from: conventional banking and insurance, alcohol, tobacco, gambling, weapons manufacturing, pork, and adult entertainment. Stage 2 financial ratio screens (debt/market cap < 33%) are not yet applied — this is noted as a limitation and planned for Part 1b.
### Results will summarized as reports and if they are not they the notebook will include a conclusion at the end summarizing the work conducted

\---

## Roadmap

|Part|Description|Status|
|-|-|-|
|1a|Universe characterisation and signal IC analysis|✅ Complete|
|1b|Stage 2 financial ratio screening|🔜 Planned|
|2|Systematic strategies: long-only momentum, low-vol, combined signal, risk parity on SPUS|🔜 In progress|
|3|Market modelling: PCA and surface fitting in (return, volatility, momentum) space|🔜 Planned|
|4|Simulation-based inference: BORG-inspired market simulator with principled priors|🔬 Long-term|

\---

## Methodological Notes

* **No lookahead bias**: signals computed from past data only at each evaluation date
* **Walk-forward validation**: train on rolling window, test on next period (Parts 2+)
* **Transaction costs modelled**: 5 bps one-way (Parts 2+)
* **Uncertainty reported**: all metrics accompanied by standard deviations and p-values
* **Null results documented**: non-significant findings reported alongside significant ones
* **Reproducible**: all data sourced from public APIs (yfinance, Wikipedia)

\---

## Installation

```bash
# Clone the repository
git clone https://github.com/mahmoudahmedosman/quantitative\_research\_project.git
cd quantitative\_research\_project

# Create environment
conda create -n quant python=3.11 -y
conda activate quant

# Install dependencies
pip install -r requirements.txt

# Register kernel and launch Jupyter
python -m ipykernel install --user --name quant --display-name "quant"
jupyter notebook
```

\---

## Dependencies

Python 3.11, pandas, numpy, yfinance, matplotlib, seaborn, scipy, statsmodels, arch, scikit-learn, tensorflow, jupyter

\---

## Connection to PhD Work

This project explicitly bridges my doctoral research and quantitative finance:

* **Signal validation methodology** mirrors the out-of-sample validation used in validating cosmological analyses
* **Part 3 (PCA / surface fitting)** directly applies the dimensionality reduction and regularised fitting techniques from NaCl to financial data
* **Part 4 (simulation-based inference)** is a BORG-inspired framework: simulate market dynamics from initial conditions, let the system evolve under realistic agent interactions, and infer latent parameters by matching observed price statistics — the financial analogue of reconstructing the 3D matter field from galaxy observations

\---

## Citation

If you use this code or results, please cite:

```
Osman, M. (2026). Systematic Equity Signals in Islamically-Compliant vs
Unconstrained Universes. GitHub repository.
https://github.com/mahmoudahmedosman/quantitative\_research\_project.git
```

\---

## Disclaimer

This project is primarily for research purposes. Nothing here constitutes financial advice.
All results are based on historical data and do not guarantee future performance.

