import os
from src.core.rust_bridge import RustCore
from src.execution.backtest import BacktestExecution
from src.execution.paper import PaperExecution
from src.execution.live import LiveExecution
from src.core.intent_validator import validate_intent
from src.core.intent import OrderIntent


class Engine:
    def __init__(self, strategy=None) -> None:
        # Strategy (optional, import-safe)
        self.strategy = strategy

        # Rust firewall
        self.rust = RustCore()
        print("RustCore version:", self.rust.version())

        # Execution mode (MUST live on self)
        self.execution_mode = os.getenv("EXECUTION_MODE", "BACKTEST")
        self.allow_live = os.getenv("ALLOW_LIVE_EXECUTION", "false").lower() == "true"

        if self.execution_mode == "LIVE":
            assert self.allow_live is True, "LIVE execution blocked by safety gate"

        # Select executor ONCE
        if self.execution_mode == "BACKTEST":
            self.executor = BacktestExecution()
        elif self.execution_mode == "PAPER":
            self.executor = PaperExecution()
        elif self.execution_mode == "LIVE":
            self.executor = LiveExecution()
        else:
            raise RuntimeError(f"Unknown execution mode: {self.execution_mode}")

    def step(self, market_data):
        """
        Strategy evaluation step.
        Returns intent ONLY. No execution.
        """
        if self.strategy is None:
            return None

        intent = self.strategy.on_tick(market_data)
        return intent

def submit_intent(self, intent: OrderIntent) -> OrderIntent:
    """
    Accepts strategy intent.
    Validates invariants.
    NO execution.
    """
    validate_intent(intent, allow_live=False)
    return intent





