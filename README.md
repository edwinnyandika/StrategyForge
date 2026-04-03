# 📈 StrategyForge — The Universal Trading Strategy Repository

> **One repo. Every strategy. Every market. Every platform. Every trader.**

StrategyForge is an open, structured library of battle-tested trading strategies spanning every known methodology — from classical textbook approaches to modern YouTube-popularized systems. Each strategy is implemented across multiple coding platforms (Pine Script, MQL5, Python), optimized for distinct trader archetypes (scalper, swing trader, position trader, algo trader), and calibrated for specific financial markets (forex, equities, crypto, commodities, futures, options).

---

## 🧭 What Is This Repo?

Most strategy repos give you code. StrategyForge gives you a **complete trading intelligence system**:

- A strategy is not just a script — it is a **modular, documented, composable unit** with clearly defined entry/exit logic, risk parameters, optimization ranges, and archetype-specific variants.
- Every strategy includes **cross-platform implementations** — the same logic expressed in Pine Script (TradingView), MQL5 (MetaTrader 4/5), and Python (backtesting/live).
- Every strategy is tagged with **market context metadata** — which asset classes it works on, which timeframes it thrives in, and how it behaves in trending vs ranging vs volatile conditions.
- Strategies can be **stacked and composed** — the repo is organized so you can combine a base strategy with complementary overlays, filters, and confirmations.

---

## 🏗️ Repository Structure

```
strategyforge/
│
├── strategies/
│   ├── trend-following/
│   │   ├── ema-crossover/
│   │   ├── supertrend/
│   │   ├── ichimoku-cloud/
│   │   ├── adx-trend-strength/
│   │   └── ...
│   ├── mean-reversion/
│   │   ├── rsi-reversal/
│   │   ├── bollinger-band-squeeze/
│   │   ├── keltner-channel-reversion/
│   │   └── ...
│   ├── momentum/
│   │   ├── macd-momentum/
│   │   ├── stochastic-momentum/
│   │   ├── rate-of-change/
│   │   └── ...
│   ├── breakout/
│   │   ├── donchian-channel-breakout/
│   │   ├── opening-range-breakout/
│   │   ├── volume-breakout/
│   │   └── ...
│   ├── price-action/
│   │   ├── pin-bar/
│   │   ├── inside-bar/
│   │   ├── engulfing-pattern/
│   │   ├── order-blocks/
│   │   ├── fair-value-gaps/
│   │   └── ...
│   ├── smart-money-concepts/
│   │   ├── change-of-character/
│   │   ├── break-of-structure/
│   │   ├── liquidity-zones/
│   │   ├── premium-discount-zones/
│   │   └── ...
│   ├── volume-based/
│   │   ├── vwap-strategy/
│   │   ├── volume-profile/
│   │   ├── on-balance-volume/
│   │   └── ...
│   ├── volatility-based/
│   │   ├── atr-based-entries/
│   │   ├── vix-regime-filter/
│   │   └── ...
│   ├── market-structure/
│   │   ├── support-resistance/
│   │   ├── supply-demand-zones/
│   │   ├── trendline-bounce/
│   │   └── ...
│   ├── multi-timeframe/
│   │   ├── htf-ltf-confluence/
│   │   └── ...
│   └── composite/                 ← Combined strategies
│       ├── smc-rsi-confluence/
│       ├── ema-vwap-scalp/
│       └── ...
│
├── platforms/
│   ├── pinescript/                ← TradingView (v5)
│   ├── mql5/                      ← MetaTrader 5
│   ├── mql4/                      ← MetaTrader 4
│   ├── python/
│   │   ├── backtesting/           ← backtrader, vectorbt, bt
│   │   └── live/                  ← ccxt, alpaca, interactive-brokers
│   └── thinkscript/               ← TD Ameritrade/thinkorswim
│
├── archetypes/
│   ├── scalper/                   ← 1m–15m, high frequency
│   ├── day-trader/                ← 5m–1h, intraday only
│   ├── swing-trader/              ← 4h–Daily, multi-day
│   ├── position-trader/           ← Weekly–Monthly, macro
│   └── algo-trader/               ← Fully automated, no manual discretion
│
├── markets/
│   ├── forex/
│   ├── equities/
│   ├── crypto/
│   ├── commodities/
│   ├── futures/
│   └── options/
│
├── optimizers/
│   ├── parameter-optimizer/       ← Walk-forward optimization
│   ├── regime-detector/           ← Identifies trending/ranging/volatile market
│   ├── risk-manager/              ← Position sizing, stop loss calculators
│   └── portfolio-combiner/        ← Correlation analysis across strategies
│
├── overlays/
│   ├── filters/                   ← Session filter, news filter, spread filter
│   ├── confirmations/             ← Volume confirmation, multi-TF confirmation
│   └── risk-controls/             ← Max drawdown guard, daily loss limit
│
├── templates/
│   ├── strategy-template.md       ← How to contribute a new strategy
│   ├── pinescript-base.pine
│   ├── mql5-base.mq5
│   └── python-base.py
│
├── docs/
│   ├── getting-started.md
│   ├── strategy-index.md          ← Full searchable index
│   ├── archetype-guide.md
│   ├── market-guide.md
│   └── composition-guide.md
│
└── tools/
    ├── strategy-finder.py         ← CLI: find strategies by tags
    ├── backtest-runner.py         ← Batch backtest across params
    └── report-generator.py        ← HTML/PDF performance reports
```

---

## 🎯 Strategy Anatomy

Every strategy in this repo follows a **unified, machine-readable structure**:

```
strategies/trend-following/ema-crossover/
├── README.md              ← Human-readable full breakdown
├── strategy.json          ← Machine-readable metadata & tags
├── pinescript/
│   ├── scalper.pine       ← Optimized for 1m–5m
│   ├── day-trader.pine    ← Optimized for 15m–1h
│   └── swing-trader.pine  ← Optimized for 4h–Daily
├── mql5/
│   ├── EA_EMA_Scalper.mq5
│   └── EA_EMA_Swing.mq5
├── python/
│   ├── backtest.py
│   └── live_bot.py
├── results/
│   ├── forex_backtest.md
│   ├── crypto_backtest.md
│   └── equity_backtest.md
└── overlays/
    └── with-rsi-filter.md ← How to combine with RSI
```

### strategy.json Schema

```json
{
  "name": "EMA Crossover",
  "slug": "ema-crossover",
  "category": "trend-following",
  "description": "...",
  "logic": {
    "entry_long": "Fast EMA crosses above Slow EMA",
    "entry_short": "Fast EMA crosses below Slow EMA",
    "exit": "Opposite crossover or fixed ATR stop"
  },
  "parameters": {
    "fast_ema": { "default": 9, "range": [5, 21], "step": 1 },
    "slow_ema": { "default": 21, "range": [15, 55], "step": 1 },
    "atr_multiplier": { "default": 1.5, "range": [1.0, 3.0], "step": 0.25 }
  },
  "archetypes": ["scalper", "day-trader", "swing-trader"],
  "markets": ["forex", "equities", "crypto"],
  "timeframes": ["5m", "15m", "1h", "4h"],
  "market_conditions": ["trending"],
  "avoid_conditions": ["ranging", "low-volatility"],
  "platforms": ["pinescript", "mql5", "python"],
  "youtube_sources": ["Trading Fraternity", "The Moving Average"],
  "tags": ["ema", "crossover", "trend", "beginner-friendly"],
  "difficulty": "beginner",
  "win_rate_range": "45-60%",
  "risk_reward": "1:2+"
}
```

---

## 👤 Trader Archetypes

Each strategy variant is tuned for a specific type of trader. The same underlying logic behaves differently across archetypes — parameters, timeframes, and risk rules are adjusted accordingly.

| Archetype | Timeframes | Trades/Day | Hold Duration | Risk/Trade | Notes |
|---|---|---|---|---|---|
| **Scalper** | 1m, 3m, 5m | 10–50+ | Seconds to minutes | 0.25–0.5% | Tight stops, fast exits, session-specific |
| **Day Trader** | 5m, 15m, 30m, 1h | 2–10 | Minutes to hours | 0.5–1% | No overnight holds, session-based |
| **Swing Trader** | 4h, Daily | 2–10/week | Days to weeks | 1–2% | Overnight holds, fundamentals awareness |
| **Position Trader** | Weekly, Monthly | 1–4/month | Weeks to months | 2–5% | Macro-aware, low frequency |
| **Algo Trader** | Any | Bot-defined | Bot-defined | Fully automated | Focus on execution, slippage, latency |

---

## 🌍 Market Coverage

Each strategy is calibrated per market type. What works in forex may need adjustment for crypto. Parameters, session filters, volatility norms, and spread tolerances differ.

| Market | Key Characteristics | Default Session Filter |
|---|---|---|
| **Forex** | 24/5, high liquidity, tight spreads | London + NY overlap |
| **Equities** | Session-bound, gap risk, news-driven | Market open hour |
| **Crypto** | 24/7, high volatility, thin books at edges | Liquid hours: 8AM–10PM UTC |
| **Commodities** | Seasonality, supply-demand cycles, global macro | Commodity-specific sessions |
| **Futures** | Leverage, roll risk, strong institutional flow | Regular trading hours |
| **Options** | Greeks-aware, theta decay, IV rank sensitivity | Expiration-aware |

---

## 🧩 Strategy Composition

StrategyForge is built for **composability**. Strategies are designed to be layered:

```
Base Strategy
  + Confirmation Layer    (e.g., volume confirmation, RSI alignment)
  + Trend Filter          (e.g., price above 200 EMA = longs only)
  + Session Filter        (e.g., London/NY session only)
  + Risk Control          (e.g., max 3 trades/day, daily drawdown cap)
  + Market Regime Filter  (e.g., only trade when ADX > 25)
```

The `composite/` folder contains pre-built combinations that have been validated together.

---

## 💻 Platform Guide

### Pine Script (TradingView)
- Version: Pine Script v5
- Usage: Indicators + Strategy scripts (with built-in backtester)
- Deployment: TradingView chart, alerts to webhook/broker

### MQL5 (MetaTrader 5)
- Usage: Expert Advisors (EAs) for fully automated trading
- Includes: Strategy Tester-ready code, custom optimization inputs

### MQL4 (MetaTrader 4)
- For legacy MT4 users; kept in sync with MQL5 versions where possible

### Python
- Backtesting: `vectorbt`, `backtrader`, `bt`
- Live: `ccxt` (crypto), `alpaca-trade-api` (equities), `ib_insync` (Interactive Brokers)
- Each script includes parameter config, logging, and a simple results summary

---

## 🚀 Getting Started

### Find a strategy for your setup

```bash
# Install the CLI tool
pip install -r tools/requirements.txt

# Find strategies for a scalper trading forex on MT5
python tools/strategy-finder.py \
  --archetype scalper \
  --market forex \
  --platform mql5 \
  --condition trending

# List all strategies with 60%+ win rate in backtests
python tools/strategy-finder.py --min-winrate 60
```

### Run a backtest (Python)

```bash
cd strategies/trend-following/ema-crossover/python
pip install -r requirements.txt
python backtest.py --market forex --pair EURUSD --timeframe 15m --archetype day-trader
```

---

## 🤝 Contributing

Want to add a strategy? Follow the contribution template:

1. Copy `templates/strategy-template.md` into the right category folder
2. Fill out the `strategy.json` metadata completely
3. Implement at least one platform (Pine Script preferred for accessibility)
4. Include a backtest result on at least one market/timeframe combo
5. Open a PR — community review before merge

**Strategy sources accepted:** YouTube educators, trading books, academic papers, institutional methodology breakdowns, original research.

---

## 📚 Strategy Index

A full searchable index is maintained in `docs/strategy-index.md`. It includes every strategy with its tags, archetypes, markets, platforms, and difficulty rating.

---

## ⚠️ Disclaimer

All strategies in this repository are for **educational and research purposes only**. Past performance in backtests does not guarantee future results. Trading involves substantial risk of loss. Always test thoroughly in a demo environment before live deployment. The contributors of this repository are not financial advisors.

---

## 📄 License

MIT License — free to use, modify, and distribute. Attribution appreciated.

---

*Built by traders, for traders. Every market. Every style. Every platform.*
