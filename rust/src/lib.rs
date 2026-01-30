#![deny(unsafe_op_in_unsafe_fn)]
#![deny(improper_ctypes_definitions)]
#![deny(non_snake_case)]
#![deny(clippy::all)]

use std::ffi::CStr;
use std::os::raw::c_char;
use std::cell::RefCell;

thread_local! {
    static LAST_ERROR: RefCell<i32> = RefCell::new(0);
}

const JL_OK: i32 = 0;
const JL_ERR_INVALID_INPUT: i32 = -1;
const JL_ERR_INTERNAL: i32 = -99;

#[inline]
fn set_error(code: i32) {
    LAST_ERROR.with(|e| *e.borrow_mut() = code);
}



#[unsafe(no_mangle)]
pub extern "C" fn jl_version() -> i32 {
    // 0.1.0 → 100 (major*100 + minor*10 + patch)
    100
}


#[unsafe(no_mangle)]
pub extern "C" fn jl_last_error() -> i32 {
    LAST_ERROR.with(|e| *e.borrow())
}

#[unsafe(no_mangle)]
pub extern "C" fn jl_risk_check(
    position_size: f64,
    max_risk: f64,
) -> i32 {
    if position_size.is_nan() || max_risk.is_nan() {
        set_error(JL_ERR_INVALID_INPUT);
        return JL_ERR_INVALID_INPUT;
    }

    if position_size > max_risk {
        set_error(JL_ERR_INVALID_INPUT);
        return JL_ERR_INVALID_INPUT;
    }

    set_error(JL_OK);
    JL_OK
}

#[unsafe(no_mangle)]
pub extern "C" fn jl_validate_order(
    qty: f64,
    price: f64,
    max_risk: f64,
) -> i32 {
    if qty.is_nan() || price.is_nan() || max_risk.is_nan() {
        set_error(JL_ERR_INVALID_INPUT);
        return JL_ERR_INVALID_INPUT;
    }

    if qty <= 0.0 || price <= 0.0 || max_risk <= 0.0 {
        set_error(JL_ERR_INVALID_INPUT);
        return JL_ERR_INVALID_INPUT;
    }

    let notional = qty * price;
    if notional > max_risk {
        set_error(JL_ERR_INVALID_INPUT);
        return JL_ERR_INVALID_INPUT;
    }

    set_error(JL_OK);
    JL_OK
}
