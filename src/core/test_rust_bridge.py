from src.core.rust_bridge import RustCore

rcore = RustCore()
print("version:", rcore.version())

# invalid
rc = rcore.validate_order(qty=-1.0, price=100.0, max_risk=50.0)
print("invalid rc:", rc, "last_error:", rcore.last_error())

# valid
rc = rcore.validate_order(qty=1.0, price=100.0, max_risk=200.0)
print("valid rc:", rc, "last_error:", rcore.last_error())
