# modular conversion functions and validation

ABS_ZERO_C = -273.15

def c_to_f(c):
    return (c * 9/5) + 32

def f_to_c(f):
    return (f - 32) * 5/9

def c_to_k(c):
    return c + 273.15

def k_to_c(k):
    return k - 273.15

def validate_temperature(value, unit):
    """Return None if valid, otherwise an error message string."""
    if value is None or str(value).strip() == '':
        return 'please provide a temperature value'
    try:
        v = float(value)
    except ValueError:
        return 'temperature must be a valid number'
    # enforce absolute zero constraints when possible
    if unit == 'c' and v < ABS_ZERO_C:
        return f'temperature cannot be below absolute zero ({ABS_ZERO_C} °c)'
    if unit == 'k' and v < 0:
        return 'kelvin cannot be negative'
    # fahrenheit absolute zero check converted to c
    if unit == 'f' and f_to_c(v) < ABS_ZERO_C:
        return f'temperature cannot be below absolute zero ({ABS_ZERO_C} °c)'
    return None
