# Linearity Analysis

## Objective

Quantify the non-linearity of each sensor's transfer function. Define linearity error formally, compute it numerically for RTD and thermistor, and describe software linearization methods.

---

## Definition of Non-Linearity

Non-linearity error is the maximum deviation of the actual transfer curve from the best-fit straight line, expressed as a percentage of full-scale output (FSO):

```
NL% = max|R_actual(T) - R_linear(T)| / FSO × 100%
```

Where R_linear(T) is the best-fit (or end-point) straight line through the transfer curve.

**Independent Non-Linearity (INL):** Uses the best-fit straight line (minimizes maximum deviation). Gives the most optimistic number.

**Terminal Non-Linearity (End-Point):** Line through the two endpoints of the range. More reproducible specification. Used here.

---

## RTD Non-Linearity

### Over 0 to +100°C Range

**Actual curve:** CVD equation R(T) = 100 × [1 + A·T + B·T²]

**End-point line:** Passes through (0°C, 100.00 Ω) and (100°C, 138.51 Ω):
```
R_linear(T) = 100 + (138.51 - 100) / 100 × T = 100 + 0.3851 × T
```

**Deviation = R_actual - R_linear:**

```
ΔR(T) = R₀ × [A·T + B·T²] - 0.3851 × T
       = [100 × A - 0.3851] × T + 100 × B × T²
       = [0.39083 - 0.3851] × T + 100×(-5.775×10⁻⁷)×T²
       = 5.73×10⁻³ × T - 5.775×10⁻⁵ × T²
```

**Maximum deviation** occurs where dΔR/dT = 0:
```
5.73×10⁻³ - 11.55×10⁻⁵ × T_max = 0
T_max = 5.73×10⁻³ / 11.55×10⁻⁵ = 49.6°C
```

**Deviation at T = 50°C:**
```
ΔR(50) = 5.73×10⁻³ × 50 - 5.775×10⁻⁵ × 2500
        = 0.2865 - 0.1444
        = 0.142 Ω
```

**Non-linearity as percentage of FSO (38.51 Ω):**
```
NL% = 0.142 / 38.51 × 100% = 0.37%
```

**Temperature equivalent error:**
```
ΔT_NL = 0.142 / 0.3851 = 0.37°C
```

So a naive linear interpolation between 0°C and 100°C calibration points introduces a maximum error of 0.37°C at 50°C. This is acceptable for Class C applications but not Class A.

### Over -200°C to +850°C (Full Range)

Over the full 1050°C range, non-linearity becomes much more significant:

| T (°C) | R_actual (Ω) | R_linear (Ω) | Error (Ω) | Error (°C) |
|---|---|---|---|---|
| -200 | 18.52 | 24.21 | -5.69 | -13.8 |
| -100 | 60.26 | 62.10 | -1.84 | -4.5 |
| 0 | 100.00 | 100.00 | 0 | 0 |
| 100 | 138.51 | 137.90 | +0.61 | +1.5 |
| 200 | 175.86 | 175.80 | +0.06 | +0.1 |
| 400 | 247.09 | 251.60 | -4.51 | -11.0 |
| 600 | 313.71 | 327.40 | -13.69 | -33.3 |
| 850 | 390.48 | 416.60 | -26.12 | -63.5 |

Non-linearity over the full range is enormous. The CVD equation (or its inverse) is absolutely essential for wide-range RTD measurements.

---

## Thermistor Non-Linearity

The NTC thermistor is fundamentally exponential. Treating it as linear is even more inadequate.

### Over 0°C to +50°C (Narrow Range)

End-point line: R(0°C) = 32,116 Ω, R(50°C) = 3,594 Ω:
```
R_linear(T) = 32116 - (32116-3594)/50 × T = 32116 - 570.44 × T
```

| T (°C) | R_actual (Ω) | R_linear (Ω) | ΔR (Ω) | ΔT (°C) |
|---|---|---|---|---|
| 0 | 32,116 | 32,116 | 0 | 0 |
| 10 | 19,143 | 26,412 | -7,269 | +36.5 |
| 25 | 10,000 | 17,895 | -7,895 | — |
| 40 | 6,530 | 9,378 | -2,848 | +21.0 |
| 50 | 3,594 | 3,594 | 0 | 0 |

**Maximum non-linearity error ≈ 7,895 Ω** near 25°C, equivalent to roughly 18°C error. The thermistor cannot be treated as linear over even a 50°C range.

### Steinhart-Hart Linearization Accuracy

Using the three-parameter Steinhart-Hart equation with coefficients calibrated at 0°C, 25°C, and 50°C:

| T (°C) | T_SH (computed) (°C) | Error (°C) |
|---|---|---|
| 0 | 0.000 | 0.000 |
| 10 | 10.003 | +0.003 |
| 20 | 20.001 | +0.001 |
| 25 | 25.000 | 0.000 |
| 30 | 29.999 | -0.001 |
| 40 | 39.997 | -0.003 |
| 50 | 50.000 | 0.000 |

**Maximum error with Steinhart-Hart: ±0.003°C** over 50°C — three orders of magnitude better than linear approximation.

---

## Software Linearization Methods

### Method 1: Exact Model Inversion

**RTD:** Solve the CVD equation (quadratic for T ≥ 0°C):
```
T = [-A + √(A² - 4B(1 - R/R₀))] / (2B)
```

Error: < 0.01°C over the full range.

**Thermistor:** Apply Steinhart-Hart equation:
```
T = 1 / [A + B·ln(R) + C·(ln(R))³]
```

Error: < 0.01°C over calibrated range.

**Thermocouple:** Apply NIST polynomial inverse (9th order for Type K):
```
T = Σ dₙ × Vⁿ
```

Error: < 0.05°C over the range.

### Method 2: Lookup Table with Interpolation

Store N equally-spaced temperature points and their corresponding resistance values in firmware:

```
Table: [(T₀, R₀), (T₁, R₁), ..., (Tₙ, Rₙ)]
```

For a measured resistance R_meas:
1. Find index i such that R_i > R_meas > R_{i+1} (for NTC)
2. Linear interpolation: T = T_i + (R_meas - R_i)/(R_{i+1} - R_i) × (T_{i+1} - T_i)

**RTD with 1°C table spacing:** 1050 entries × 4 bytes each = 4.2 kB flash. Error < 0.01°C (CVD non-linearity within 1°C interval is negligible).

**Thermistor with 1°C spacing (0 to 100°C):** 101 entries = 0.4 kB. Error < 0.05°C with linear interpolation.

### Method 3: Polynomial Correction to a Linear Fit

For systems already using linear approximation, add a polynomial correction term:

```
T_corrected = T_linear + c₂(T_linear)² + c₃(T_linear)³
```

Fit coefficients c₂, c₃ by minimizing the residual from the exact model. This approach is efficient for microcontrollers where the linear calculation is already done.

---

## Integral Non-Linearity (INL) and Differential Non-Linearity (DNL)

These terms (from ADC characterization) also apply to sensor characterization:

**INL:** Maximum deviation from the ideal straight line over the full range. Discussed above.

**DNL:** The maximum deviation of the local sensitivity (slope) from the ideal constant sensitivity:

```
DNL(T) = [S_actual(T) - S_ideal] / S_ideal × 100%
```

For RTD at 0°C (S_ideal = 0.3851 Ω/°C):
```
DNL(0°C) = [0.3908 - 0.3851] / 0.3851 × 100% = +1.48%
DNL(100°C) = [0.3793 - 0.3851] / 0.3851 × 100% = -1.51%
DNL(850°C) = [0.2926 - 0.3851] / 0.3851 × 100% = -24.0%
```

High DNL means the gain of the system is not constant — the same degree of change in the physical quantity produces different output changes at different points in the range.

---

## Conclusion

| Sensor | NL over typical range | Software correction | Residual error |
|---|---|---|---|
| RTD (0–100°C) | ±0.37% FS | CVD inverse | < 0.001°C |
| RTD (full range) | ±6% FS | CVD inverse | < 0.01°C |
| Thermistor (0–50°C) | >>100% FS | Steinhart-Hart | < 0.01°C |
| Type K (0–1000°C) | ±5% FS | NIST polynomial | < 0.05°C |

Every sensor in this project requires software linearization for precision measurement. The error without linearization is many degrees — completely unacceptable for any serious application.
