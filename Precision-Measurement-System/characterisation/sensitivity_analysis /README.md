# Sensitivity Analysis

## Objective

Quantify and compare the sensitivity of each sensor type at every stage of the measurement chain. Understand how sensitivity propagates from sensor to bridge to amplifier to ADC counts, and how sensitivity varies with temperature.

---

## Definition

Sensitivity is defined as the rate of change of a quantity with respect to the measurand (temperature):

```
S_x = dx / dT
```

Where x is the quantity at a given point in the chain (resistance, voltage, ADC count).

---

## Stage 1: Sensor Sensitivity

### PT100 RTD

Local sensitivity from the CVD equation:

```
S_RTD(T) = dR/dT = R₀ × (A + 2B·T)
```

With R₀ = 100 Ω, A = 3.9083×10⁻³, B = -5.775×10⁻⁷:

```
S_RTD(0°C)   = 100 × 3.9083×10⁻³ = 0.3908 Ω/°C
S_RTD(100°C) = 100 × (3.9083×10⁻³ + 2×(-5.775×10⁻⁷)×100)
             = 100 × (3.9083 - 1.155)×10⁻³ = 0.2753... 
```

Wait, recomputing:
```
S_RTD(100°C) = 100 × (3.9083×10⁻³ + 2×(-5.775×10⁻⁷)×100)
             = 100 × (3.9083×10⁻³ - 1.155×10⁻⁴)
             = 100 × 3.7928×10⁻³
             = 0.3793 Ω/°C
```

**RTD sensitivity table:**

| T (°C) | S_RTD (Ω/°C) | % change from 0°C |
|---|---|---|
| -200 | 0.4138 | +5.9% |
| -100 | 0.4022 | +2.9% |
| 0 | 0.3908 | 0% |
| 100 | 0.3793 | -2.9% |
| 200 | 0.3677 | -5.9% |
| 400 | 0.3446 | -11.8% |
| 600 | 0.3215 | -17.7% |
| 850 | 0.2926 | -25.1% |

**Key finding:** RTD sensitivity decreases by 25% over the full range. This is accounted for by the CVD equation, but simplified systems using constant α = 0.385 will have temperature-dependent gain error.

### NTC Thermistor (10 kΩ, B = 3950 K)

```
S_NTC(T) = dR/dT = -R(T) × B / T²
```

| T (°C) | T (K) | R(T) (Ω) | S_NTC (Ω/°C) | |S_NTC| / S_RTD |
|---|---|---|---|---|
| -20 | 253 | 96,358 | -5,989 | 14,470× |
| 0 | 273 | 32,116 | -1,717 | 4,395× |
| 25 | 298 | 10,000 | -445 | 1,139× |
| 50 | 323 | 3,594 | -136 | 348× |
| 100 | 373 | 649 | -23 | 59× |

**Key finding:** Thermistor sensitivity varies by 260× over -20°C to +100°C. It is enormously more sensitive than RTD near 25°C, but this advantage collapses at higher temperatures.

### Type K Thermocouple

Sensitivity = Seebeck coefficient S_K(T):

| T (°C) | S_K (μV/°C) | Ratio to RTD bridge equivalent |
|---|---|---|
| 0 | 39.4 | — |
| 100 | 41.3 | — |
| 500 | 43.1 | — |
| 1000 | 38.3 | — |

Note: To compare thermocouple sensitivity to RTD, both must be considered at the amplifier input. RTD bridge at V_ex = 5V gives 4.81 mV/°C. Thermocouple gives 0.041 mV/°C. RTD bridge is ~117× more sensitive at the amplifier input.

---

## Stage 2: Bridge Sensitivity

For a quarter-bridge with PT100:

```
S_bridge(T) = dV_out/dT = V_ex / (4R₀ + 2δR(T)) × S_RTD(T)
```

Near balance (δR ≈ 0):
```
S_bridge ≈ V_ex × S_RTD / (4R₀) = 5 × 0.3908 / 400 = 4.885 mV/°C
```

As temperature increases (δR increases), bridge sensitivity decreases:

| T (°C) | δR (Ω) | S_bridge exact (mV/°C) | S_bridge linear (mV/°C) | Error |
|---|---|---|---|---|
| 0 | 0 | 4.885 | 4.885 | 0% |
| 25 | 9.63 | 4.748 | 4.750 | -2.9% |
| 50 | 19.40 | 4.621 | 4.614 | -5.6% |
| 100 | 38.51 | 4.380 | 4.341 | -11.0% |
| 200 | 75.86 | 3.941 | 3.804 | -21.2% |

**Key finding:** The bridge non-linearity means the sensitivity drops by 21% from 0°C to 200°C. The linearized model significantly underestimates the true output at high temperatures.

---

## Stage 3: Amplifier Sensitivity

After INA with gain G:

```
S_total(T) = G × S_bridge(T)
```

For G = 10:

| T (°C) | S_total (mV/°C) |
|---|---|
| 0 | 48.85 |
| 25 | 47.48 |
| 100 | 43.80 |
| 200 | 39.41 |

**ADC input range utilization** (16-bit ADC, 5V reference):

For 0–100°C measurement with G = 10:
- Output swing = 4.380 × 100 × (1 + non-linearity correction) ≈ 403.6 mV (from simulation)
- With G = 10: V_out_max = 4.036 V → **80.7% of ADC full scale**

Good utilization. If measuring only 0–50°C, G = 20 would use the ADC range better.

---

## Stage 4: ADC Resolution

For a 16-bit ADC (2¹⁶ = 65,536 counts) with 5V full scale:

```
V_LSB = 5 / 65536 = 76.3 μV/count
```

Minimum resolvable temperature change:
```
ΔT_LSB = V_LSB / S_total(25°C) = 76.3 μV / 47.48 mV/°C = 0.00161°C = 1.61 mK
```

A 16-bit ADC provides 1.6 mK resolution — far better than any systematic error in this system. The ADC is not the limitation.

For a 12-bit ADC (4,096 counts):
```
V_LSB = 5 / 4096 = 1.22 mV
ΔT_LSB = 1.22 mV / 47.48 mV/°C = 25.7 mK = 0.026°C
```

A 12-bit ADC provides 26 mK resolution — still adequate for most industrial applications, but may limit performance for precision work.

---

## Sensitivity Comparison Summary

| Sensor | Measurement Range | Sensitivity at 25°C | Bridge Output (V_ex=5V) | ADC Counts/°C (16-bit) |
|---|---|---|---|---|
| PT100 RTD | -200 to +850°C | 0.391 Ω/°C | 4.75 mV/°C | 62 |
| NTC Thermistor | -50 to +150°C | 445 Ω/°C | 56.9 mV/°C* | 745* |
| Type K T/C | -200 to +1260°C | 41.3 μV/°C | 4.13 mV/°C† | 54† |

*Thermistor bridge at 25°C, high sensitivity but rapidly decreasing
†Thermocouple with G=100 amplifier

---

## Python Script Reference

See `plots/sensitivity_analysis.py` for:
- Plot of S_RTD(T) vs temperature
- Plot of S_NTC(T) vs temperature on same axes
- Plot of bridge sensitivity S_bridge(T) vs temperature
- Comparison of 12-bit vs 16-bit ADC resolution lines

---

## Conclusions

1. **Thermistor has 1000× higher raw sensitivity** than RTD at 25°C but this collapses at temperature extremes
2. **RTD bridge sensitivity drops 11% over 0–100°C** due to non-linearity — must use exact formula for < 0.5% accuracy
3. **16-bit ADC gives 1.6 mK resolution** in this system — not the limiting factor
4. **Amplifier gain selection** should target 70–90% ADC full-scale utilization at maximum expected temperature
5. The sensitivity varies with temperature for all three sensors — this variation is the core reason software linearization (CVD, Steinhart-Hart, NIST polynomials) is necessary
