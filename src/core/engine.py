import os

EXECUTION_MODE = os.getenv("EXECUTION_MODE", "BACKTEST")
ALLOW_LIVE_EXECUTION = os.getenv("ALLOW_LIVE_EXECUTION", "false").lower() == "true"

if EXECUTION_MODE == "LIVE":
    assert ALLOW_LIVE_EXECUTION is True, "LIVE execution blocked by safety gate"
