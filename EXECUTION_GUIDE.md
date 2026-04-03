# StrategyForge — Execution Guide

How to set up the repo and use AI to generate, backtest, and manage strategies.

---

## Quick Start (3 Steps)

### Step 1 — Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/strategyforge.git
cd strategyforge
pip install anthropic vectorbt pandas numpy
```

### Step 2 — Set your Anthropic API key

```bash
# Mac/Linux
export ANTHROPIC_API_KEY="sk-ant-..."

# Windows
set ANTHROPIC_API_KEY=sk-ant-...
```

Get an API key at: https://console.anthropic.com

### Step 3 — Run the AI builder

```bash
python tools/strategy_builder.py
```

Follow the prompts. Your strategy gets saved directly into `strategies/` with the correct folder structure.

---

## Two Ways to Use the AI Builder

### Option A: Interactive CLI (recommended for single strategies)

```bash
python tools/strategy_builder.py
```

The wizard asks you:
- What strategy? (plain English description)
- Archetype? (scalper / day-trader / swing-trader / position-trader / algo-trader)
- Market? (forex / crypto / equities / commodities / futures / options)
- Platform? (pinescript / mql5 / python / mql4 / thinkscript)
- Extra requirements? (optional)

It calls Claude, streams the output, and saves everything into the right folder.

### Option B: Batch generation (for building your full library)

Create a `batch.json` file:

```json
[
  {
    "name": "EMA Crossover with RSI Filter",
    "archetype": "scalper",
    "market": "forex",
    "platform": "pinescript",
    "extras": "London/NY session only. ATR stop loss."
  },
  {
    "name": "Bollinger Band Squeeze",
    "archetype": "swing-trader",
    "market": "crypto",
    "platform": "python",
    "extras": "Volume confirmation on breakout."
  }
]
```

Then run:

```bash
python tools/strategy_builder.py --batch batch.json --output .
```

This generates all strategies in one run — great for seeding your entire library.

### Option C: Browser UI

Open `tools/strategyforge_ui.html` in your browser. Enter your API key, describe the strategy, pick your settings. Generated code appears in tabs — copy or download. No installation required.

---

## What Gets Generated

For every strategy, the AI creates:

| File | Description |
|------|-------------|
| `strategy.json` | Machine-readable metadata: tags, parameters, markets, archetypes |
| `{platform}/{archetype}.{ext}` | Complete, commented, runnable code |
| `README.md` | Setup guide, parameter docs, deployment instructions |
| Optimization notes | Top 3 parameters to tune, suggested ranges |

### Example output structure

```
strategies/
└── trend-following/
    └── ema-crossover-rsi-filter/
        ├── strategy.json
        ├── README.md
        ├── pinescript/
        │   └── scalper.pine        ← paste into TradingView Pine Editor
        ├── mql5/
        │   └── scalper.mq5         ← copy to MT5 Experts folder
        ├── python/
        │   └── scalper.py          ← run directly
        └── results/
            └── (backtest results go here)
```

---

## Deploying Generated Code

### Pine Script (TradingView)
1. Open TradingView → Open a chart
2. Click "Pine Editor" at the bottom
3. Paste the contents of `{archetype}.pine`
4. Click "Add to chart"
5. For live alerts: set up alerts using the strategy signals

### MQL5 (MetaTrader 5)
1. Copy `{archetype}.mq5` to: `MT5 Data Folder > MQL5 > Experts`
2. Open MetaEditor → Press F7 to compile
3. Drag the EA onto a chart
4. In the Strategy Tester: set the input parameters from `strategy.json`

### Python (backtesting)
```bash
cd strategies/trend-following/ema-crossover-rsi-filter/python
pip install vectorbt pandas
python scalper.py
```

---

## Customising AI-generated strategies

After generation, open the code and look for the `inputs` or `Parameters` section at the top. All tunable values are collected there — the AI always puts them in one place with comments.

**To re-generate with different parameters**, just run the builder again with more specific extras:

```
Extra requirements: Use 9/21 EMA, RSI period 14, only enter on close above EMA,
stop loss at 1.2x ATR, take profit at 2.4x ATR (2:1 RR)
```

---

## Running Backtests (Python strategies)

Every Python strategy includes a `backtest()` function powered by vectorbt.

```bash
python strategies/.../python/swing-trader.py
```

This outputs:
- Total return
- Win rate
- Max drawdown
- Sharpe ratio
- Number of trades
- A simple equity curve plot

To batch-backtest all Python strategies:

```bash
python tools/backtest_runner.py --market forex --timeframe 1h
```

---

## Finding Strategies with the CLI

```bash
# All scalper strategies for forex
python tools/strategy_finder.py --archetype scalper --market forex

# All strategies that work on both forex and crypto
python tools/strategy_finder.py --market forex --market crypto

# All Pine Script strategies in the trend-following category
python tools/strategy_finder.py --platform pinescript --category trend-following

# Strategies tagged with 'ema' or 'rsi'
python tools/strategy_finder.py --tags ema rsi
```

---

## Composing Strategies

StrategyForge strategies are designed to stack. The `overlays/` folder has drop-in additions:

```
overlays/
├── filters/
│   ├── london_ny_session.pine    ← Only trade during high-liquidity hours
│   ├── news_filter.pine          ← Pause before major news events
│   └── spread_filter.pine        ← Skip when spread is too wide
├── confirmations/
│   ├── volume_confirmation.pine  ← Require above-average volume
│   └── mtf_trend.pine            ← Confirm trend on higher timeframe
└── risk_controls/
    ├── daily_loss_limit.pine     ← Stop trading after X% daily loss
    └── max_trades_per_day.pine   ← Cap the number of trades
```

To combine: ask the AI directly:

```
Extra requirements: Add the London/NY session filter and volume confirmation overlay.
Cap at 3 trades per day. Use the daily loss limit of 2%.
```

---

## Repo Maintenance

### Indexing all strategies
```bash
python tools/strategy_finder.py --rebuild-index
```

This re-scans all `strategy.json` files and regenerates `docs/strategy-index.md`.

### Updating an existing strategy
Re-run the builder with `--update` and the strategy slug:
```bash
python tools/strategy_builder.py --update ema-crossover-rsi-filter
```

---

## Cost Estimate

Each strategy generation uses approximately:
- ~800 tokens input
- ~2,000–4,000 tokens output
- At Claude Sonnet pricing: roughly $0.01–0.02 per strategy

A full library of 100 strategies costs approximately $1–2 in API credits.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `anthropic` not found | `pip install anthropic` |
| API key error | Check `ANTHROPIC_API_KEY` is set correctly |
| Empty sections in output | Re-run — occasional model variability |
| Pine Script syntax error | Ask AI: "Fix this Pine Script v5 error: [paste error]" |
| MQL5 won't compile | Ask AI: "Fix this MQL5 compilation error: [paste error]" |

---

*StrategyForge — Build smarter, trade better.*
