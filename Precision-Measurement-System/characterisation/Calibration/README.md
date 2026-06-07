# Calibration

## Objective

Develop a complete calibration procedure for the RTD measurement system: from selecting calibration points, to fitting correction curves, to verifying residuals and documenting uncertainty.

---

## Why Calibration is Necessary

Even a Class B PT100 RTD with a perfectly designed circuit has:
- Sensor tolerance: ±0.3°C at 0°C (IEC 60751 Class B)
- Amplifier gain error: ±0.5%
- Bridge resistor tolerance: ±1% (if 1% resistors used)
- ADC gain/offset error: ±0.1%

The combined systematic error before calibration: potentially ±2–4°C.

After a proper multi-point calibration, this reduces to < ±0.1°C.

Calibration maps the system's raw output (ADC counts or resistance value) to the true physical temperature using reference standards traceable to ITS-90.

---

## Calibration Equipment

| Item | Purpose | Accuracy |
|---|---|---|
| Stirred liquid calibration bath | Provides stable, uniform reference temperature | ±0.05°C |
| Reference SPRT or calibrated RTD | Reference thermometer traceable to national standards | ±0.02°C |
| Precision resistance bridge (4-wire) | Reads reference sensor resistance | ±0.001 Ω |
| Data acquisition system | Records DUT output and reference simultaneously | |
| Ice-point reference (0°C) | Optional fixed-point verification | ±0.01°C |

---

## Calibration Procedure

### Step 1: Soak at Reference Temperature

Immerse both the Device Under Test (DUT, the sensor being calibrated) and the reference thermometer in the calibration bath.

Set bath to the first calibration temperature. Allow to stabilize until temperature drift < 0.01°C per minute (typically 10–30 minutes).

### Step 2: Record Data

At each stable temperature point, record:
- T_ref: temperature from reference thermometer (°C)
- V_DUT: voltage output from DUT measurement system (V) or
- R_DUT: resistance of DUT element (Ω) from 4-wire measurement

Record 10 readings at 1-second intervals and average to reduce random noise.

### Step 3: Repeat at All Calibration Points

**For two-point calibration (offset + gain correction):**
- Two bath temperatures spanning the measurement range (e.g., 0°C and 100°C)

**For three-point calibration (adds one non-linearity correction):**
- Three temperatures (e.g., 0°C, 50°C, 100°C)

**For multi-point calibration (full curve fit):**
- 5–10 temperatures evenly spaced across range
- More points allow polynomial curve fitting → lower residual error

### Step 4: Fit Correction Curve

Using the calibration data pairs (T_ref, R_DUT) or (T_ref, V_DUT), fit a correction function.

---

## Two-Point Calibration (Offset + Gain)

Assumes the error is a linear function of temperature: ΔT = a + b×T_DUT.

With two calibration points (T_ref,1, V_DUT,1) and (T_ref,2, V_DUT,2):

**Gain:**
```
b = (T_ref,2 - T_ref,1) / (V_DUT,2 - V_DUT,1)
```

**Offset:**
```
a = T_ref,1 - b × V_DUT,1
```

**Corrected temperature:**
```
T_corrected = a + b × V_DUT
```

**Example:**

| Point | T_ref (°C) | V_DUT (mV) |
|---|---|---|
| 1 | 0.00 | -12.5 |
| 2 | 100.00 | 475.3 |

Gain: b = 100.00 / (475.3 - (-12.5)) = 100.00 / 487.8 = 0.20499 °C/mV
Offset: a = 0.00 - 0.20499 × (-12.5) = +2.562°C

Corrected: T = 2.562 + 0.20499 × V_DUT

**Residual after two-point calibration:** Up to ±0.37°C (from RTD non-linearity over 0–100°C) — the linearization error is now the dominant error.

---

## Multi-Point Polynomial Calibration

For best accuracy, use 5+ calibration points and fit a polynomial correction:

```
T_corrected = c₀ + c₁ × R_DUT + c₂ × R_DUT² + c₃ × R_DUT³
```

(Or equivalently, fit T_ref vs V_DUT as a polynomial.)

**Fitting procedure (least squares):**

Given N calibration pairs (R_i, T_i):

Minimize:
```
Σ [T_i - (c₀ + c₁R_i + c₂R_i² + c₃R_i³)]²
```

This is a standard least-squares polynomial regression, solved using numpy in Python:

```python
import numpy as np

# Calibration data
R_cal = np.array([100.00, 109.73, 119.40, 128.98, 138.51])   # Ω
T_cal = np.array([0.00,   25.00,  50.00,  75.00,  100.00])   # °C

# Fit 3rd-order polynomial: T = f(R)
coefficients = np.polyfit(R_cal, T_cal, deg=3)
poly = np.poly1d(coefficients)

# Evaluate calibration fit
T_fitted = poly(R_cal)
residuals = T_cal - T_fitted

print("Max residual:", np.max(np.abs(residuals)), "°C")
```

**Residual after 3rd-order polynomial fit over 0–100°C:** < 0.005°C.
**Residual after 3rd-order fit over -200°C to +850°C:** < 0.1°C.

---

## Calibration Uncertainty Budget

The calibration itself introduces uncertainty:

| Source | Uncertainty (k=2, 95%) |
|---|---|
| Reference thermometer | ±0.04°C |
| Bath uniformity (spatial) | ±0.05°C |
| Bath stability (temporal) | ±0.02°C |
| DUT measurement noise | ±0.01°C |
| Curve fit residual (RTD, 3rd order) | ±0.01°C |
| **Total calibration uncertainty (RSS)** | **±0.07°C** |

This means the calibrated system has an uncertainty floor of ±0.07°C, regardless of how precise the sensor or circuit is. Better calibration equipment reduces this floor.

---

## Calibration Documentation

Each calibration must be documented with:

```
Calibration Record
==================
Sensor Type:        PT100 RTD, Class B
Serial Number:      SN-2024-0142
Calibration Date:   [Date]
Calibration By:     [Engineer name]

Reference Equipment:
  Thermometer: [Make/Model/Cal date]
  Bath:        [Make/Model]

Calibration Data:
  Point 1: T_ref = 0.00°C,  R_DUT = 100.21 Ω
  Point 2: T_ref = 25.00°C, R_DUT = 110.01 Ω
  Point 3: T_ref = 50.00°C, R_DUT = 119.78 Ω
  Point 4: T_ref = 75.00°C, R_DUT = 129.52 Ω
  Point 5: T_ref = 100.00°C, R_DUT = 138.97 Ω

Correction Polynomial: T = -2.41 + 2.614×R - 0.00312×R²
Max residual: ±0.08°C
Calibration uncertainty (k=2): ±0.12°C
Valid range: 0 to 100°C
Next calibration due: [Date + 1 year]
```

---

## In-Situ Verification (Check Calibration)

Between full calibrations, perform periodic check calibrations using fixed-point references:
- **Ice point (0°C):** Water/ice slurry, provides 0.000°C ± 0.01°C
- **Steam point (100°C at 1 atm):** Boiling water, provides 100°C ± 0.05°C (pressure-corrected)
- **Thermostat check:** Known stable temperature source

If check calibration deviation > acceptance criterion (typically 0.5× the allowed measurement uncertainty), perform full recalibration.

---

## Python Script

See `plots/calibration_plot.py` for:
- Loading calibration data from CSV
- Fitting correction polynomial (NumPy polyfit)
- Plotting T_ref vs T_DUT (raw) with ideal line
- Plotting residuals T_cal - T_fit
- Computing and printing calibration uncertainty
