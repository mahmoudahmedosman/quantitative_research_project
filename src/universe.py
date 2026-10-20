"""
Universe management: SP500 and SPUS (Sharia-screened) universes.

SPUS excludes:
  - Conventional financials (banks, insurance, interest-bearing instruments)
  - Weapons & defence contractors
  - Alcohol producers & distributors
  - Tobacco
  - Pork-related businesses
  - Entertainment (gambling, adult content)

Key methodological note: universe membership must be known BEFORE the signal
date to avoid lookahead bias.
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
UNIVERSE_DIR = DATA_DIR / "universes"
UNIVERSE_DIR.mkdir(parents=True, exist_ok=True)
SPUS_DIR = UNIVERSE_DIR / "spus_holdings"
SPUS_DIR.mkdir(exist_ok=True)

EXCLUDED_TICKERS = {
    # Conventional banking
    "JPM", "BAC", "WFC", "C", "USB", "PNC", "TFC", "FITB", "KEY", "RF",
    "CFG", "HBAN", "MTB", "ZION", "CMA", "GS", "MS", "SCHW",
    # Asset managers
    "BLK", "BX", "KKR", "APO", "CG", "ARES", "BAM", "BN", "TPG",
    # Insurance
    "BRK-B", "MET", "PRU", "AFL", "ALL", "TRV", "CB", "HIG", "AIG",
    "GL", "UNM", "LNC", "PFG", "EQH", "RE", "WRB", "CINF", "ERIE",
    "ACGL", "RNR", "MKL",
    # Payment networks & consumer finance
    "V", "MA", "AXP", "DFS", "COF", "SYF", "ALLY", "SLM",
    # REITs
    "AMT", "PLD", "EQIX", "CCI", "SPG", "O", "DLR", "PSA", "EXR",
    "AVB", "EQR", "MAA", "UDR", "CPT", "NNN", "WPC", "VICI", "GLPI",
    "SBAC", "IRM", "VTR", "WELL", "ARE", "BXP", "KIM", "REG", "FRT",
    # Alcohol
    "STZ", "TAP", "BUD", "BF-B",
    # Tobacco
    "MO", "PM", "BTI",
    # Gambling
    "MGM", "WYNN", "LVS", "CZR", "PENN", "DKNG", "FLUT",
    # Weapons & defence
    "LMT", "RTX", "NOC", "GD", "BA", "LHX", "HII", "TDG",
    # Media / adult entertainment
    "PARA", "WBD", "FOX", "FOXA",
    # Pork
    "HRL",
}

def get_sp500_universe() -> list:
    return [
        "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
        "UNH",  "LLY",  "JPM",  "V",    "XOM",   "MA",   "AVGO",
        "PG",   "HD",   "COST", "MRK",  "ABBV",  "CVX",  "KO",
        "PEP",  "ADBE", "WMT",  "BAC",  "CRM",   "TMO",  "ORCL",
        "ACN",  "MCD",  "CSCO", "ABT",  "AMD",   "DHR",  "NEE",
        "TXN",  "PM",   "INTC", "WFC",  "AMGN",  "RTX",  "QCOM",
        "HON",  "UPS",  "LOW",  "SPGI", "GS",    "MS",   "BLK",
    ]

def get_spus_universe() -> list:
    """SP500 after applying Sharia exclusions."""
    return [t for t in get_sp500_universe() if t not in EXCLUDED_TICKERS]

def get_universe(name: str) -> list:
    if name == "sp500":  return get_sp500_universe()
    elif name == "spus": return get_spus_universe()
    else: raise ValueError(f"Unknown universe: {name}")

def universe_diff() -> dict:
    sp500 = get_sp500_universe()
    spus  = get_spus_universe()
    excluded = set(sp500) - set(spus)
    return {
        "sp500_count":    len(sp500),
        "spus_count":     len(spus),
        "n_excluded":     len(excluded),
        "excluded":       sorted(excluded),
        "exclusion_pct":  round(len(excluded) / len(sp500) * 100, 1),
    }



def get_full_sp500_universe() -> list:
    try:
        import requests
        import io
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        response = requests.get(url, headers=headers)
        tables = pd.read_html(io.StringIO(response.text))
        tickers = tables[0]["Symbol"].str.replace(".", "-", regex=False).tolist()
        print(f"Fetched {len(tickers)} S&P 500 tickers from Wikipedia")
        return tickers
    except Exception as e:
        print(f"Wikipedia fetch failed ({e}), using fallback list")
        return [
            "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
            "UNH",  "LLY",  "JPM",  "V",    "XOM",   "MA",   "AVGO",
            "PG",   "HD",   "COST", "MRK",  "ABBV",  "CVX",  "KO",
            "PEP",  "ADBE", "WMT",  "BAC",  "CRM",   "TMO",  "ORCL",
            "ACN",  "MCD",  "CSCO", "ABT",  "AMD",   "DHR",  "NEE",
            "TXN",  "PM",   "INTC", "WFC",  "AMGN",  "RTX",  "QCOM",
            "HON",  "UPS",  "LOW",  "SPGI", "GS",    "MS",   "BLK",
        ]

def get_full_spus_universe() -> list:
    sp500 = get_full_sp500_universe()
    screened = [t for t in sp500 if t not in EXCLUDED_TICKERS]
    print(f"SPUS: {len(screened)} stocks (excluded {len(sp500) - len(screened)})")
    return screened

def get_full_universe(name: str) -> list:
    if name == "sp500":  return get_full_sp500_universe()
    elif name == "spus": return get_full_spus_universe()
    else: raise ValueError(f"Unknown universe: {name}")
