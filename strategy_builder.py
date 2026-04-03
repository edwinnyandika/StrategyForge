#!/usr/bin/env python3
"""
StrategyForge — AI Strategy Builder
Uses Claude API to generate complete trading strategies.
Usage: python tools/strategy_builder.py
"""

import os
import json
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime

try:
    import anthropic
except ImportError:
    print("Install required: pip install anthropic")
    sys.exit(1)

# ── System prompt that turns Claude into a strategy engine ──────────────────
SYSTEM_PROMPT = """You are StrategyForge's trading strategy engine — an expert in technical analysis, 
algorithmic trading, and strategy development across all financial markets.

When given a strategy request, you generate:
1. A complete, ready-to-use implementation in the requested platform language
2. A filled-out strategy.json metadata file
3. A clear README with setup and usage instructions

Rules:
- Code must be complete, runnable, and well-commented
- Parameters must include sensible defaults AND optimization ranges
- Always include entry, exit, stop-loss, and take-profit logic
- Adapt parameters to the trader archetype (scalper = tighter stops/faster signals, 
  swing = wider stops/slower signals, algo = no manual elements)
- Adapt to the market (crypto needs wider stops than forex, equities need session filters)
- Output ONLY valid JSON for strategy.json — no markdown fences
- For Pine Script: use v5 syntax
- For MQL5: generate a complete Expert Advisor with OnInit, OnTick, OnDeinit
- For Python: use vectorbt for backtesting with a clean backtest() function

Always end with a section called OPTIMIZATION_NOTES explaining the 3 most impactful 
parameters to tune and suggested ranges for the chosen market/archetype combo.
"""

def build_user_prompt(strategy_name, archetype, market, platform, description, extras):
    timeframe_map = {
        "scalper":         "1m, 3m, or 5m",
        "day-trader":      "15m or 1h",
        "swing-trader":    "4h or Daily",
        "position-trader": "Weekly",
        "algo-trader":     "15m or 1h (automated)"
    }
    risk_map = {
        "scalper":         "0.25–0.5% per trade, ATR-based tight stops",
        "day-trader":      "0.5–1% per trade, no overnight holds",
        "swing-trader":    "1–2% per trade, swing high/low stops",
        "position-trader": "2–5% per trade, macro-aware",
        "algo-trader":     "1% per trade, fully rule-based, no discretion"
    }
    session_map = {
        "forex":      "London + NY overlap (07:00–12:00 EST)",
        "crypto":     "08:00–22:00 UTC (peak liquidity)",
        "equities":   "Market open (09:30–11:00 EST) + power hour (15:00–16:00 EST)",
        "commodities":"Commodity-specific sessions",
        "futures":    "Regular trading hours only",
        "options":    "Market hours, avoid expiration days"
    }

    return f"""Generate a complete StrategyForge strategy package for the following:

STRATEGY: {strategy_name}
DESCRIPTION: {description}
ARCHETYPE: {archetype}
MARKET: {market}
PLATFORM: {platform}
PREFERRED TIMEFRAME: {timeframe_map.get(archetype, "4h")}
RISK PROFILE: {risk_map.get(archetype, "1% per trade")}
SESSION FILTER: {session_map.get(market, "Standard market hours")}
EXTRA REQUIREMENTS: {extras if extras else "None"}

Please generate:

---SECTION: STRATEGY_JSON---
(A complete strategy.json object — plain JSON only, no fences)

---SECTION: CODE---
(Complete {platform} implementation with full comments)

---SECTION: README---
(Setup, parameters, usage, and how to deploy on {platform})

---SECTION: OPTIMIZATION_NOTES---
(Top 3 parameters to optimize with suggested ranges for {market}/{archetype})
"""

def parse_sections(raw_text):
    """Extract named sections from the AI response."""
    sections = {}
    pattern = r"---SECTION:\s*(\w+)---(.*?)(?=---SECTION:|$)"
    matches = re.findall(pattern, raw_text, re.DOTALL)
    for name, content in matches:
        sections[name.strip()] = content.strip()
    return sections

def save_strategy(sections, strategy_slug, archetype, market, platform, output_dir):
    """Save all generated files to the correct repo structure."""
    # Determine category from strategy name (basic heuristic; can be extended)
    category_keywords = {
        "ema": "trend-following", "sma": "trend-following", "macd": "trend-following",
        "rsi": "mean-reversion", "bollinger": "mean-reversion", "stochastic": "mean-reversion",
        "breakout": "breakout", "donchian": "breakout", "opening-range": "breakout",
        "vwap": "volume-based", "volume": "volume-based",
        "pin-bar": "price-action", "engulfing": "price-action", "order-block": "smart-money-concepts",
        "smc": "smart-money-concepts", "fair-value": "smart-money-concepts",
        "momentum": "momentum", "roc": "momentum"
    }
    category = "trend-following"
    for kw, cat in category_keywords.items():
        if kw in strategy_slug:
            category = cat
            break

    # Build folder path
    base = Path(output_dir) / "strategies" / category / strategy_slug
    platform_dir = base / platform.lower().replace(" ", "-").replace("/", "-")
    platform_dir.mkdir(parents=True, exist_ok=True)
    (base / "results").mkdir(exist_ok=True)

    saved = []

    # Save strategy.json
    if "STRATEGY_JSON" in sections:
        json_path = base / "strategy.json"
        try:
            parsed = json.loads(sections["STRATEGY_JSON"])
            json_path.write_text(json.dumps(parsed, indent=2))
        except json.JSONDecodeError:
            json_path.write_text(sections["STRATEGY_JSON"])
        saved.append(str(json_path))

    # Save code with correct extension
    ext_map = {
        "pinescript": "pine",
        "mql5": "mq5",
        "mql4": "mq4",
        "python": "py",
        "thinkscript": "ts"
    }
    ext = ext_map.get(platform.lower(), "txt")
    code_filename = f"{archetype}.{ext}"

    if "CODE" in sections:
        code_path = platform_dir / code_filename
        code_path.write_text(sections["CODE"])
        saved.append(str(code_path))

    # Save README
    if "README" in sections:
        readme_path = base / "README.md"
        full_readme = f"# {strategy_slug.replace('-', ' ').title()}\n\n"
        full_readme += f"**Archetype:** {archetype} | **Market:** {market} | **Platform:** {platform}\n\n"
        full_readme += f"*Generated by StrategyForge AI on {datetime.now().strftime('%Y-%m-%d')}*\n\n"
        full_readme += "---\n\n"
        full_readme += sections["README"]
        if "OPTIMIZATION_NOTES" in sections:
            full_readme += "\n\n---\n\n## Optimization Notes\n\n"
            full_readme += sections["OPTIMIZATION_NOTES"]
        readme_path.write_text(full_readme)
        saved.append(str(readme_path))

    return saved, category

def run_interactive():
    """Interactive CLI wizard for strategy generation."""
    print("\n" + "="*58)
    print("  StrategyForge — AI Strategy Builder")
    print("  Powered by Claude (Anthropic)")
    print("="*58 + "\n")

    # Get API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        api_key = input("Anthropic API key (or set ANTHROPIC_API_KEY env var): ").strip()
        if not api_key:
            print("Error: API key required.")
            sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Collect inputs
    print("Describe your strategy (e.g. 'EMA crossover with RSI filter'):")
    strategy_name = input("  Strategy name/description: ").strip()
    if not strategy_name:
        strategy_name = "EMA Crossover with RSI Filter"

    slug = re.sub(r"[^a-z0-9]+", "-", strategy_name.lower()).strip("-")

    print("\nTrader archetype:")
    archetypes = ["scalper", "day-trader", "swing-trader", "position-trader", "algo-trader"]
    for i, a in enumerate(archetypes, 1):
        print(f"  {i}. {a}")
    choice = input("  Choose (1-5) [default: 2]: ").strip()
    archetype = archetypes[int(choice)-1] if choice.isdigit() and 1 <= int(choice) <= 5 else "day-trader"

    print("\nMarket:")
    markets = ["forex", "crypto", "equities", "commodities", "futures", "options"]
    for i, m in enumerate(markets, 1):
        print(f"  {i}. {m}")
    choice = input("  Choose (1-6) [default: 1]: ").strip()
    market = markets[int(choice)-1] if choice.isdigit() and 1 <= int(choice) <= 6 else "forex"

    print("\nPlatform:")
    platforms = ["pinescript", "mql5", "python", "mql4", "thinkscript"]
    for i, p in enumerate(platforms, 1):
        print(f"  {i}. {p}")
    choice = input("  Choose (1-5) [default: 1]: ").strip()
    platform = platforms[int(choice)-1] if choice.isdigit() and 1 <= int(choice) <= 5 else "pinescript"

    extras = input("\nExtra requirements (overlays, filters, etc.) [optional]: ").strip()

    output_dir = input("\nOutput directory [default: current repo root '.']: ").strip() or "."

    # Build prompt
    user_prompt = build_user_prompt(strategy_name, archetype, market, platform, strategy_name, extras)

    print(f"\nGenerating '{strategy_name}' for {archetype} on {market} ({platform})...")
    print("This may take 30–60 seconds...\n")

    # Call Claude API with streaming
    full_response = ""
    try:
        with client.messages.stream(
            model="claude-opus-4-5",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}]
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                full_response += text
    except anthropic.APIError as e:
        print(f"\nAPI error: {e}")
        sys.exit(1)

    print("\n\n" + "-"*58)
    print("Generation complete. Saving files...")

    # Parse and save
    sections = parse_sections(full_response)
    if not sections:
        # Fallback: save raw output
        raw_path = Path(output_dir) / f"{slug}_raw_output.md"
        raw_path.write_text(full_response)
        print(f"Saved raw output to: {raw_path}")
    else:
        saved_files, category = save_strategy(sections, slug, archetype, market, platform, output_dir)
        print(f"\nSaved to category: strategies/{category}/{slug}/")
        for f in saved_files:
            print(f"  ✓ {f}")

    print("\nDone. Your strategy is ready in the repo.")
    print("Next step: run a backtest with:")
    if platform == "python":
        print(f"  python strategies/*/{ slug}/python/{archetype}.py")
    elif platform == "pinescript":
        print(f"  Open TradingView → Pine Editor → paste content of {slug}/{platform}/{archetype}.pine")
    elif platform in ("mql5", "mql4"):
        print(f"  Copy {slug}/{platform}/{archetype}.mq5 to your MT5 Experts folder and compile")

def run_batch(batch_file, output_dir):
    """Run multiple strategy generations from a JSON batch file."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: Set ANTHROPIC_API_KEY environment variable for batch mode.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    with open(batch_file) as f:
        batch = json.load(f)

    print(f"Running batch generation: {len(batch)} strategies\n")

    for i, item in enumerate(batch, 1):
        name = item.get("name", f"strategy_{i}")
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        archetype = item.get("archetype", "day-trader")
        market = item.get("market", "forex")
        platform = item.get("platform", "pinescript")
        extras = item.get("extras", "")

        print(f"[{i}/{len(batch)}] {name} ({archetype}/{market}/{platform})...", end=" ", flush=True)

        prompt = build_user_prompt(name, archetype, market, platform, name, extras)
        try:
            response = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )
            raw = response.content[0].text
            sections = parse_sections(raw)
            if sections:
                save_strategy(sections, slug, archetype, market, platform, output_dir)
                print("✓")
            else:
                Path(output_dir).mkdir(exist_ok=True)
                (Path(output_dir) / f"{slug}_raw.md").write_text(raw)
                print("✓ (raw)")
        except Exception as e:
            print(f"✗ Error: {e}")

    print(f"\nBatch complete. All strategies saved to: {output_dir}/strategies/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="StrategyForge AI Strategy Builder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/strategy_builder.py                        # Interactive wizard
  python tools/strategy_builder.py --batch batch.json     # Batch generation
  python tools/strategy_builder.py --batch batch.json --output ./strategies
        """
    )
    parser.add_argument("--batch", help="Path to JSON batch file for bulk generation")
    parser.add_argument("--output", default=".", help="Output directory (repo root)")
    args = parser.parse_args()

    if args.batch:
        run_batch(args.batch, args.output)
    else:
        run_interactive()
