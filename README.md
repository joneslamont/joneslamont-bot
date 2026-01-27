# JonesLamont Bot Framework

A modular, safety-first algorithmic trading framework designed for research,
backtesting, and controlled execution.

## 🔒 Safety by Default

This repository is intentionally configured to prevent accidental live trading
and secret leakage.

Built-in protections include:
- Execution firewall (LIVE mode blocked unless explicitly enabled)
- `.env` files ignored by default
- Git pre-push hook that blocks secrets and credentials
- Public-safe configuration templates only

Live execution is **disabled by default**.

## 🧱 Project Structure

```text
src/
  core/          # Engine, execution guards, shared logic
  execution/     # Execution adapters (paper / live gated)
  strategies/    # Strategy logic
  risk/          # Risk management modules
  config/        # Public-safe configuration templates

## ⚠️ Important Notes

- This repository **never** contains API keys or credentials
- `.env` files are **local-only** and must never be committed
- Live trading is **disabled by default** and requires explicit local enablement
- This framework is intended for **research, backtesting, and paper trading**

## 🚀 Getting Started (Safe Mode)

1. Clone the repository
2. Create a local `.env` file in the project root  
   (this file is ignored by Git and never committed)
3. Set execution mode to BACKTEST or PAPER only
4. Run strategies locally for research and testing

⚠️ LIVE execution is intentionally blocked in this public repository.

## 🛡️ Safety Architecture

This project includes:
- Execution guards to prevent accidental live trading
- Git hooks that block secrets before push
- Configuration separation between public templates and private values
