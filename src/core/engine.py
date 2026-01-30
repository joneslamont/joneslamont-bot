import os
from src.core.rust_bridge import RustCore
from src.execution.backtest import BacktestExecution
from src.execution.paper import PaperExecution
from src.execution.live import LiveExecution

class Engine:
    def __init__(self):
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

def submit_order(self, qty: float, price: float, max_risk: float) -> None:
    # ---------- HARD RUST FIREWALL ----------
    rc = self.rust.validate_order(qty, price, max_risk)
    if rc != 0:
        raise ValueError(
            f"Rust validate_order failed rc={rc}, "
            f"last_error={self.rust.last_error()}"
        )

    position_size = qty * price

    rc = self.rust.risk_check(position_size, max_risk)
    if rc != 0:
        raise ValueError(
            f"Rust risk_check failed rc={rc}, "
            f"last_error={self.rust.last_error()}"
        )

    # ---------- FIREWALL PASSED ----------
    self.executor.execute(qty, price)



