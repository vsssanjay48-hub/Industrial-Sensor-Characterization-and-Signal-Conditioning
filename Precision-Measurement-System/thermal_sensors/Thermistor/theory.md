# Thermistor — Theory
 
## Introduction
 
A thermistor is a thermally sensitive resistor — a device whose resistance changes significantly with temperature. Unlike RTDs (which use metal), thermistors use **semiconductor ceramic materials** whose resistance-temperature behavior is governed by semiconductor band theory. The result is an extremely large, highly non-linear resistance change with temperature.
 
The word *thermistor* is a contraction of "thermally sensitive resistor." They are made in two fundamental types:
- **NTC (Negative Temperature Coefficient):** Resistance decreases with increasing temperature. By far the most common type in temperature measurement.
- **PTC (Positive Temperature Coefficient):** Resistance increases with temperature (can be very abrupt). Primarily used for over-temperature protection, self-regulating heaters, not precision temperature measurement.
This document focuses on NTC thermistors, which dominate precision temperature sensing applications in the narrow-range, high-sensitivity domain.
 
---
 
## Physical Mechanism of NTC Behavior
 
### Semiconductor Band Theory
 
In a semiconductor, electron energy levels are organized into:
- **Valence band:** Normally filled with electrons
- **Conduction band:** Normally empty, electrons here can move freely and conduct current
- **Band gap E_g:** The energy difference between valence and conduction band tops
At absolute zero (0 K), all electrons are in the valence band, none in the conduction band → resistance = ∞.
 
As temperature increases, thermal energy excites some electrons across the band gap into the conduction band, leaving "holes" in the valence band. Both electrons and holes can carry current.
 
**The number of charge carriers (n) available for conduction:**
```
n ∝ exp(-E_g / 2k_B T)
```
 
Where:
- E_g = band gap energy (eV)
- k_B = Boltzmann constant (8.617 × 10⁻⁵ eV/K)
- T = absolute temperature (K)
**Resistance is proportional to 1/n (fewer carriers → higher resistance):**
```
R(T) ∝ exp(+E_g / 2k_B T)
```
 
This exponential relationship is the fundamental origin of the NTC thermistor's large resistance change with temperature. It also makes the response highly non-linear — an inherent feature of semiconductor physics.
 
### Thermistor Materials
 
NTC thermistors are made from metal oxide ceramics, sintered at high temperatures to produce polycrystalline structures with controlled electrical properties. Common materials:
 
| Material System | Temperature Range | Characteristics |
|---|---|---|
| Mn-Ni-Co oxide | -50 to +150°C | General purpose, most common |
| Mn-Cu oxide | -80 to +50°C | Low-temperature applications |
| Fe-Mn oxide | Up to +300°C | High-temperature NTC |
| Co-Mn oxide | -60 to +200°C | Stable, precision types |
 
The specific material composition determines the band gap E_g and therefore the B (beta) constant that characterizes the sensitivity.
 
### Why Sensitivity is So High
 
The sensitivity of a thermistor at temperature T₀ is:
```
S = dR/dT = -R(T₀) × B / T₀²
```
 
For a typical NTC thermistor at 25°C (298 K) with B = 3950 K and R = 10 kΩ:
```
S = -10000 × 3950 / 298² = -445 Ω/°C
```
 
Compare to PT100 RTD: 0.385 Ω/°C.
 
The thermistor is **1157× more sensitive** at 25°C. This enormous sensitivity advantage comes at the cost of non-linearity and narrower operating range.
 
---
 
## The Beta (B) Constant Model
 
The simplest practical model for NTC thermistor resistance:
 
```
R(T) = R_ref × exp[B × (1/T - 1/T_ref)]
```
 
Where:
- T = temperature in Kelvin
- T_ref = reference temperature (typically 298.15 K = 25°C)
- R_ref = resistance at T_ref (e.g., 10,000 Ω for a 10 kΩ NTC)
- B = Beta constant (material constant, units = K, typically 2000–5000 K)
**Derivation from semiconductor theory:**
 
Starting from R(T) ∝ exp(E_g/2k_BT):
```
R(T)/R(T_ref) = exp[(E_g/2k_B) × (1/T - 1/T_ref)]
```
 
The combination E_g/2k_B is the Beta constant:
```
B = E_g / (2 k_B)    [K]
```
 
For E_g ≈ 0.68 eV (typical NTC thermistor material):
```
B = 0.68 / (2 × 8.617×10⁻⁵) ≈ 3946 K
```
 
This matches typical thermistor B values of 3800–4200 K.
 
**B value interpretation:**
 
- Higher B → steeper R-T curve → higher sensitivity → narrower useful range
- Lower B → shallower R-T curve → lower sensitivity → wider range
- B is approximately constant but changes slightly with temperature → reason why the Steinhart-Hart model is more accurate
**Computing resistance at any temperature from the Beta model:**
 
Example: R_ref = 10,000 Ω, B = 3950 K, T_ref = 298.15 K. Find R at 50°C = 323.15 K:
```
R(323.15) = 10000 × exp[3950 × (1/323.15 - 1/298.15)]
           = 10000 × exp[3950 × (0.003095 - 0.003354)]
           = 10000 × exp[3950 × (-2.59×10⁻⁴)]
           = 10000 × exp[-1.023]
           = 10000 × 0.3594
           = 3594 Ω
```
 
The resistance dropped from 10,000 Ω to 3,594 Ω for a 25°C increase — a 64% decrease. Compare to PT100: a 25°C increase changes resistance by only 9.6 Ω (9.6% change from 100 Ω).
 
---
 
## Steinhart-Hart Equation
 
The Beta model is a two-parameter approximation that assumes B is constant. In reality, B varies with temperature by a few percent, causing errors up to 2–3°C over wide temperature ranges.
 
The **Steinhart-Hart equation** is a three-parameter empirical model that fits the NTC thermistor characteristic far more accurately:
 
```
1/T = A + B·ln(R) + C·[ln(R)]³
```
 
Where:
- T = absolute temperature (K)
- R = thermistor resistance (Ω)
- A, B, C = Steinhart-Hart coefficients (device-specific constants)
**Note:** The A, B, C here are Steinhart-Hart coefficients, not the same B as in the Beta model.
 
**Accuracy:** The Steinhart-Hart equation fits NTC thermistor behavior to better than ±0.01°C over a 100°C range when calibrated with three data points.
 
**Determining coefficients from three-point calibration:**
 
Measure resistance at three temperatures (T₁, T₂, T₃):
 
Form a system of three equations:
```
1/T₁ = A + B·ln(R₁) + C·[ln(R₁)]³
1/T₂ = A + B·ln(R₂) + C·[ln(R₂)]³
1/T₃ = A + B·ln(R₃) + C·[ln(R₃)]³
```
 
Solve simultaneously for A, B, C (linear system in the unknowns A, B, C).
 
For best accuracy, choose calibration temperatures spanning the full expected measurement range, with one point near each end and one in the middle.
 
---
 
## Non-Linearity: Visualization
 
The non-linearity of NTC thermistors is extreme compared to RTDs. Consider a 10 kΩ NTC at 25°C with B = 3950:
 
| Temperature (°C) | R (Ω) | ΔR/ΔT (Ω/°C) |
|---|---|---|
| -20 | 98,061 | -4,700 |
| 0 | 32,650 | -1,860 |
| 25 | 10,000 | -440 |
| 50 | 3,594 | -136 |
| 75 | 1,453 | -47 |
| 100 | 649 | -18 |
 
The sensitivity at -20°C is 4700 Ω/°C, but at 100°C it has dropped to only 18 Ω/°C — a 261-fold reduction over the 120°C span. This is why simple linear approximation is completely inadequate for thermistors beyond ±5°C from the calibration point.
 
---
 
## NTC vs PTC Comparison
 
| Property | NTC | PTC |
|---|---|---|
| Resistance vs T | Decreases | Increases (sometimes abruptly) |
| Mechanism | Semiconductor band conduction | Grain boundary effect (BaTiO₃) or polymer-carbon |
| Temperature range | -80 to +300°C | Narrow useful range around switching temperature |
| Sensitivity | Very high | Very high (at switching point) |
| Primary use | Temperature measurement | Over-temperature protection, self-regulating heaters |
| Accuracy | ±0.1°C (calibrated) | Not used for precision measurement |
 
---
 
## Conclusion
 
The NTC thermistor's high sensitivity — rooted in exponential semiconductor carrier generation — makes it exceptional for measuring temperature over a narrow range with high precision. Its fundamental limitation is non-linearity, which requires the Steinhart-Hart equation for accurate inversion. Within the temperature range where the specific thermistor is characterized, it can outperform RTDs in terms of sensitivity and resolution at lower cost.
