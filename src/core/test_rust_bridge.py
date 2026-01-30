from src.core.rust_bridge import RustCore


def test_rust_version():
    rc = RustCore()
    v = rc.version()
    assert isinstance(v, int)
    assert v > 0


def test_validate_order_ok():
    rc = RustCore()
    rc_code = rc.validate_order(qty=1.0, price=100.0, max_risk=1000.0)
    assert rc_code == 0

