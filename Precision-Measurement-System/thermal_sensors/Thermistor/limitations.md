# Thermistor Equations

## 1. Beta Model
```
R(T) = R_ref × exp[B × (1/T − 1/T_ref)]    (T in Kelvin)
T    = 1 / [(1/T_ref) + (1/B)×ln(R/R_ref)]
```

## 2. Steinhart-Hart
```
1/T = A + B·ln(R) + C·[ln(R)]³
```
Accuracy: ±0.01°C with 3-point calibration.

## 3. Sensitivity
```
S(T) = dR/dT = −R(T) × B / T²     [Ω/°C]
α(T) = (1/R)×dR/dT = −B/T²        [/°C, negative for NTC]
```
At 25°C: S = −445 Ω/°C,  α = −4.45%/°C

## 4. Self-Heating (more severe than RTD)
```
ΔT_self = R_th × I² × R(T)
```
At I = 1 mA, R = 10 kΩ, R_th = 200 K/W:
```
ΔT_self = 200 × (10⁻³)² × 10000 = 2.0°C    (severe!)
```
At I = 0.1 mA: ΔT_self = 0.02°C (acceptable).
→ Keep excitation current < 0.1 mA for precision thermistor measurement.

## 5. Optimal Voltage Divider Linearization
```
R_fixed_optimal = √(R_min × R_max)    (geometric mean)
```
For 0 to 80°C: R_min = 2339 Ω, R_max = 32116 Ω:
```
R_optimal = √(2339 × 32116) = √(75,119,324) ≈ 8667 Ω → use 8.66 kΩ
```
Reduces non-linearity from >100% to ~2–3% over 80°C span.

## 6. Voltage Divider Output
```
V_out = V_in × R_NTC(T) / (R_fixed + R_NTC(T))
```
Bridge output sensitivity at 25°C (R_fixed = 10 kΩ, V_ex = 5 V):
```
dV/dT ≈ V_ex × |S_NTC| / (R_fixed + R_NTC)²  × R_fixed
       = 5 × 445 / (20000)² × 10000
       ≈ 55.6 mV/°C     (vs 4.81 mV/°C for RTD bridge)
```
NTC bridge output is ~11.6× larger per degree at 25°C.
