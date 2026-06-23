# Thermocouple Equations

## 1. Seebeck EMF
```
V ≈ S_AB × (T_hot − T_ref)              [approximate, constant S_AB]
V = ∫[T_ref to T_hot] S_AB(T) dT        [exact, use NIST tables]
```

## 2. Cold Junction Compensation
```
V_corrected = V_measured + V_table(T_CJ)
T_hot = V_table_inverse(V_corrected)
```
Example (Type K): V_measured = 12.000 mV, T_CJ = 25°C
- V_table(25°C) = 1.000 mV
- V_corrected = 13.000 mV
- T_hot = ~316°C
- Without CJC: T_hot = ~292°C  → 24°C error

## 3. Type K Inverse Polynomial (0 to 500°C, 0 to 20.644 mV)
```
T = d₀ + d₁V + d₂V² + ... + d₉V⁹
```
Key coefficients:
```
d₀ =  0.0000000
d₁ =  2.5083550×10¹
d₂ =  7.8601460×10⁻²
d₃ = −2.5031720×10⁻¹
d₄ =  8.3152700×10⁻²
d₅ = −1.2280340×10⁻²
```
Error < ±0.05°C over range.

## 4. Required Amplifier Gain
Type K, 0 to 1000°C, max EMF = 41.276 mV, ADC FS = 5V:
```
G = 5000 mV / 41.276 mV = 121  → use G = 100
```

## 5. Noise and Resolution
With G = 100, INA noise 50 nV/√Hz, BW = 10 Hz:
```
V_n,in = 50×10⁻⁹ × √10 = 158 nV
T_n = 158×10⁻⁹ / (41×10⁻⁶ V/°C) = 3.9 m°C
```
Noise floor excellent. In practice CJC error (±0.5–1°C) dominates.

## 6. Thermocouple Response Time
Bare 1 mm bead in flowing air (h = 100 W/m²·K):
```
m ≈ 4.6 μg,   c_p ≈ 444 J/kg·K
C_th = 4.6×10⁻⁶ × 444 = 2.04×10⁻³ J/K
A_s = π × (10⁻³)² = 3.14×10⁻⁶ m²
R_th = 1/(100 × 3.14×10⁻⁶) = 3183 K/W
τ = R_th × C_th = 6.5 s
```
Fine-wire thermocouples (0.1 mm): τ < 0.1 s in flowing media.
