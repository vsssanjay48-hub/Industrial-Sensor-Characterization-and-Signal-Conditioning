# RTD Equations

## 1. CVD Equation

For T ≥ 0°C:
```
R(T) = R₀[1 + A·T + B·T²]
```
For T < 0°C:
```
R(T) = R₀[1 + A·T + B·T² + C·(T−100)·T³]
```
A = 3.9083×10⁻³, B = −5.775×10⁻⁷, C = −4.183×10⁻¹², R₀ = 100 Ω

**Example — R(250°C):**
```
R(250) = 100×[1 + 3.9083×10⁻³×250 + (−5.775×10⁻⁷)×250²]
       = 100×[1 + 0.9771 − 0.0361]
       = 100×1.9410 = 194.10 Ω
```

---

## 2. Linear Approximation

```
R(T) = R₀(1 + αT)      α = 3.850×10⁻³ /°C
```
Error at 200°C: linear gives 177.0 Ω vs CVD 175.86 Ω → **2.96°C error**.
Do not use beyond ±50°C from reference without correction.

---

## 3. Inverse CVD — Temperature from Resistance

For T ≥ 0°C (quadratic formula):
```
T = [−A + √(A² − 4B(1 − R/R₀))] / (2B)
```

**Example — T from R = 150 Ω:**
```
a = B×R₀ = −5.775×10⁻⁷×100 = −5.775×10⁻⁵
b = A×R₀ = 3.9083×10⁻³×100 = 0.39083
c = R₀−R = 100−150 = −50

discriminant = 0.39083² − 4×(−5.775×10⁻⁵)×(−50)
             = 0.15275 − 0.01155 = 0.14120
T = (−0.39083 + √0.14120) / (2×(−5.775×10⁻⁵))
  = (−0.39083 + 0.37577) / (−1.155×10⁻⁴)
  = −0.01506 / (−1.155×10⁻⁴)
  = 130.4°C    ✓
```

---

## 4. Local Sensitivity

```
S(T) = dR/dT = R₀×(A + 2B·T)     [Ω/°C,  T ≥ 0]
```

| T (°C) | S(T) (Ω/°C) |
|---|---|
| −200 | 0.4138 |
| 0 | 0.3908 |
| 100 | 0.3793 |
| 300 | 0.3562 |
| 600 | 0.3215 |
| 850 | 0.2926 |

Sensitivity drops 25% over the full range — must use local sensitivity for precision.

---

## 5. Self-Heating

```
ΔT_self = R_th × I² × R(T)
```

Max current for ΔT < 0.05°C (still air, R_th = 200 K/W):
```
I_max = √(0.05 / (200×100)) = 1.58 mA
```
Standard: use **I = 1 mA** → ΔT = 0.02°C.

---

## 6. Lead Wire Resistance Error (2-wire)

Copper wire: ρ = 1.72×10⁻⁸ Ω·m

```
R_lead (per wire) = ρ × L / A
```

| Length | 0.5 mm² wire | Error (2-wire PT100) |
|---|---|---|
| 10 m | 0.344 Ω | 0.89°C |
| 50 m | 1.72 Ω | 4.47°C |
| 100 m | 3.44 Ω | 8.94°C |

→ Use 4-wire for any run > 2 m in precision applications.

---

## 7. Bridge + INA Full Output

Combined sensitivity:
```
dV_out/dT = G × V_ex × α / 4 = 10 × 5 × 3.85×10⁻³ / 4 = 48.1 mV/°C
```

16-bit ADC resolution (5V FS):
```
ΔT_LSB = (5000 mV / 65536) / 48.1 mV/°C = 1.58 mK/LSB
```

---

## Quick Reference

| Parameter | Value |
|---|---|
| R₀ | 100.00 Ω |
| α (mean 0–100°C) | 3.850×10⁻³ /°C |
| S at 0°C | 0.3908 Ω/°C |
| S at 100°C | 0.3793 Ω/°C |
| Range (IEC 60751) | −200 to +850°C |
| Class B tolerance at 0°C | ±0.30°C |
| Self-heating (1mA, still air) | +0.02°C |
