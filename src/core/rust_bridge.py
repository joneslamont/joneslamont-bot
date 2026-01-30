import ctypes
from ctypes import c_int32, c_double
from pathlib import Path


class RustCore:
    """
    Thin ABI bridge (ctypes) to Rust dylib.
    Python orchestrates. Rust enforces contracts.
    """

    def __init__(self):
        lib_path = self._resolve_lib_path()
        self.lib = ctypes.CDLL(str(lib_path))

        # ---- int32 jl_version(void)
        self.lib.jl_version.argtypes = []
        self.lib.jl_version.restype = c_int32

        # ---- int32 jl_last_error(void)
        self.lib.jl_last_error.argtypes = []
        self.lib.jl_last_error.restype = c_int32

        # ---- int32 jl_risk_check(double position_size, double max_risk)
        self.lib.jl_risk_check.argtypes = [c_double, c_double]
        self.lib.jl_risk_check.restype = c_int32

        # ---- int32 jl_validate_order(double qty, double price, double max_risk)
        self.lib.jl_validate_order.argtypes = [c_double, c_double, c_double]
        self.lib.jl_validate_order.restype = c_int32

    def _resolve_lib_path(self) -> Path:
        # Repo root is: src/core/rust_bridge.py -> src/core -> src -> repo_root
        repo_root = Path(__file__).resolve().parents[2]
        # Prefer release (Step 4), fall back to debug if needed
        release_so = repo_root / "rust" / "target" / "release" / "libjoneslamont_rust.so"
        debug_so = repo_root / "rust" / "target" / "debug" / "libjoneslamont_rust.so"

        if release_so.exists():
            return release_so
        if debug_so.exists():
            return debug_so

        raise FileNotFoundError(
            f"Rust dylib not found.\nChecked:\n- {release_so}\n- {debug_so}\n"
            f"Build it with:\n  cargo build --manifest-path rust/Cargo.toml --release"
        )

    # ---------- public python API ----------
    def version(self) -> int:
        return int(self.lib.jl_version())

    def last_error(self) -> int:
        return int(self.lib.jl_last_error())

    def risk_check(self, position_size: float, max_risk: float) -> int:
        rc = int(self.lib.jl_risk_check(position_size, max_risk))
        return rc

    def validate_order(self, qty: float, price: float, max_risk: float) -> int:
        rc = int(self.lib.jl_validate_order(qty, price, max_risk))
        return rc




