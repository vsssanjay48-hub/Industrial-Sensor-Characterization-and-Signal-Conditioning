# Precision Measurement System — Project Report

**Author:** [Sanjay V S]
**Date:** 2026(jan-june)
**Institution / Course:** [IIT Delhi/Transducers for Instrumentation]
**Project Repository:** Precision-Measurement-System

---

## Abstract

This report documents a depth-first study of industrial precision thermal measurement systems. Three sensor types are studied — the PT100 RTD, NTC Thermistor, and Type K Thermocouple — from their fundamental physical operating principles through complete signal conditioning design, simulation, and characterization. The instrumentation chain is analyzed at every stage: sensor physics, Wheatstone bridge interfacing, instrumentation amplifier design, low-pass filtering, noise analysis, linearity, calibration, and long-term drift. LTspice simulations validate the analytical circuit design. Python scripts generate quantitative characterization plots. The project demonstrates that depth of engineering understanding, rather than breadth of sensor coverage, is the path to competent instrumentation design.

---

## 1. Introduction

### 1.1 Motivation

Temperature is the most frequently measured physical quantity in industrial processes. It governs reaction rates, material properties, safety limits, energy efficiency, and product quality. Measuring it accurately requires more than selecting a sensor — it requires understanding the complete chain from physical phenomenon to digital number, including every source of error that corrupts the measurement along the way.

This project is built around one central question: **what does it actually take to measure temperature to ±0.1°C reliably, over years of operation, in a real environment?**

Answering that question requires understanding:
- Why platinum resistance changes with temperature (electron-phonon scattering)
- Why the resistance-temperature relationship is slightly non-linear (Callendar-Van Dusen equation)
- Why a 2-wire RTD connection introduces errors (lead resistance)
- Why a Wheatstone bridge is used (converts ΔR to differential voltage, rejects common-mode noise)
- Why a single op-amp differential amplifier is insufficient (CMRR degrades with resistor tolerance)
- Why an instrumentation amplifier is preferred (high CMRR independent of external matching)
- Why the measurement bandwidth must be limited (noise power ∝ bandwidth)
- Why the sensor must be calibrated (tolerance, drift, systematic offset)
- Why the reading drifts over years (grain growth, component aging)

Each of these questions has a quantitative answer. This report develops those answers systematically.

### 1.2 Project Scope

**Sensors studied:** PT100 RTD, NTC Thermistor (10 kΩ), Type K Thermocouple

**Signal conditioning:** Wheatstone bridge, differential amplifier, instrumentation amplifier (3-op-amp topology), 2nd-order Butterworth low-pass filter

**Analysis performed:** Sensitivity, linearity, error propagation, self-heating, lead resistance, noise floor, calibration curve fitting, long-term drift mechanisms

**Tools used:** LTspice (circuit simulation), Python/numpy/matplotlib (characterization plots), Git/GitHub (version control)

---

## 2. Measurement Theory

### 2.1 The Instrumentation Chain

Every measurement system can be modeled as a cascade of transfer functions:

```
T (°C) → Sensor → Bridge → INA → Filter → ADC → Digital Value
```

The overall transfer function is the product of each stage:
```
H_total(s) = H_sensor(s) · H_bridge(s) · H_INA(s) · H_filter(s)
```

Each stage contributes gain (or attenuation), bandwidth limitation, and noise. The stage with the lowest bandwidth limits the overall system.

### 2.2 Static Characteristics Summary

| Characteristic | PT100 RTD | NTC Thermistor | Type K T/C |
|---|---|---|---|
| Sensitivity at 25°C | 0.391 Ω/°C | 445 Ω/°C | 41.3 μV/°C |
| Range | −200 to +850°C | −50 to +150°C | −200 to +1260°C |
| Linearity (0–100°C) | ±0.37% FS | >100% (non-linear) | ±3% FS |
| Accuracy (std grade) | ±0.3°C (Class B) | ±1°C (uncal.) | ±2.2°C (Class 2) |
| Long-term stability | Excellent | Moderate | Moderate–Poor |

### 2.3 Dynamic Response

All three sensors behave approximately as first-order systems:
```
τ_th = R_th × C_th = m·c_p / (h·A_s)
```

Response time constants:

| Sensor | Installation | τ (seconds) |
|---|---|---|
| PT100 (6mm sheath) | Still air | 30–60 |
| PT100 (6mm sheath) | Flowing water | 3–10 |
| NTC bead (2mm) | Still air | 2–5 |
| Type K (1mm bead) | Flowing air | 1–3 |

The sensor bandwidth sets the fundamental measurement bandwidth — no signal processing can recover information the sensor never captured.

---

## 3. Sensor Analysis

### 3.1 PT100 RTD

#### 3.1.1 Physical Principle

Platinum resistance increases with temperature due to electron-phonon scattering. As temperature rises, lattice vibrations (phonons) increase in amplitude and density, scattering conduction electrons more frequently and increasing resistivity. Above the Debye temperature (~100 K for platinum), this gives a near-linear relationship:

```
R(T) ∝ 1 + αT + βT² + ...
```

Platinum is chosen for RTDs because it is chemically stable, can be made very pure (99.999%+), has a reproducible and well-characterized R(T) curve, and defines the ITS-90 temperature scale from −259°C to +962°C.

#### 3.1.2 Callendar-Van Dusen Model

The IEC 60751 standard model for PT100:

For T ≥ 0°C:
```
R(T) = R₀[1 + A·T + B·T²]
```
For T < 0°C:
```
R(T) = R₀[1 + A·T + B·T² + C·(T−100)·T³]
```

With A = 3.9083×10⁻³ /°C, B = −5.775×10⁻⁷ /°C², C = −4.183×10⁻¹² /°C⁴, R₀ = 100 Ω.

#### 3.1.3 Key Numerical Results

- Sensitivity at 0°C: S = R₀·A = 0.3908 Ω/°C
- Sensitivity at 100°C: S = 0.3793 Ω/°C (−2.9% from 0°C value)
- Non-linearity over 0–100°C: ±0.37% FS = ±0.37°C (if treated as linear)
- Self-heating at 1 mA in still air (R_th = 200 K/W): ΔT = 0.02°C
- Lead resistance error (2-wire, 10m, 0.5mm² Cu): +1.79°C
- Lead resistance error (4-wire): 0°C

#### 3.1.4 Inverse Equation (T from R)

For T ≥ 0°C, exact analytical inversion:
```
T = [−A + √(A² − 4B(1 − R/R₀))] / (2B)
```
Numerical error of this inversion: < 0.001 μ°C (essentially exact).

### 3.2 NTC Thermistor

#### 3.2.1 Physical Principle

NTC thermistors are semiconductor ceramic metal oxides. Resistance follows from carrier density:
```
n ∝ exp(−E_g / 2k_B T)
```
Therefore:
```
R(T) ∝ exp(+E_g / 2k_B T) = exp(B/T)
```

The Beta constant B = E_g/2k_B. For typical NTC materials (E_g ≈ 0.68 eV), B ≈ 3950 K.

#### 3.2.2 Models

**Beta model** (two parameters, simpler):
```
R(T) = R_ref × exp[B × (1/T − 1/T_ref)]       T in Kelvin
```
Accuracy: ±0.5–2°C over 100°C range.

**Steinhart-Hart equation** (three parameters, superior):
```
1/T = A + B·ln(R) + C·[ln(R)]³
```
Accuracy: ±0.01°C over 100°C range with 3-point calibration.

#### 3.2.3 Key Numerical Results

- Sensitivity at 25°C: −445 Ω/°C (1139× more sensitive than PT100)
- Sensitivity at 100°C: −19 Ω/°C (only 59× more sensitive than PT100)
- Non-linearity over 0–50°C (if treated as linear): >1000% FS
- Self-heating at 0.1 mA (R = 10 kΩ, R_th = 200 K/W): ΔT = 0.02°C
- Self-heating at 1 mA: ΔT = **2.0°C** — severe, must reduce current

### 3.3 Type K Thermocouple

#### 3.3.1 Physical Principle

The Seebeck effect: in a metal under a temperature gradient, conduction electrons at the hot end have higher kinetic energy and diffuse toward the cold end. The resulting charge separation creates an electric potential (the Seebeck voltage).

Each metal has a Seebeck coefficient S_A (μV/°C). Two dissimilar metals A and B joined at a hot junction produce:
```
V_AB = ∫[T_cold to T_hot] (S_A − S_B) dT
```

For Type K (Chromel/Alumel): S_AB ≈ 41 μV/°C at 25°C.

#### 3.3.2 Cold Junction Compensation

NIST tables assume cold junction at 0°C. In practice, cold junction is at ambient T_CJ:
```
V_corrected = V_measured + V_table(T_CJ)
T_hot = V_table_inverse(V_corrected)
```
Without CJC: error = T_CJ (e.g., 25°C error if ambient is 25°C).

#### 3.3.3 Key Numerical Results

- Sensitivity at 0–500°C: 39–43 μV/°C
- Required amplifier gain: G = 100–500 (to reach ADC range)
- CJC error contribution: ±0.5–2°C (dominant error source)
- Long-term drift above 1000°C: 2–4°C per 100 operating hours

---

## 4. Signal Conditioning Design

### 4.1 Wheatstone Bridge

**Configuration:** Quarter-bridge, single active PT100 arm, V_ex = 5V DC.

**Exact output voltage:**
```
V_out = V_ex × δR / (4R₀ + 2δR)
```

**Bridge sensitivity at 0°C:**
```
S_bridge = V_ex × α / 4 = 5 × 3.85×10⁻³ / 4 = 4.81 mV/°C
```

**Non-linearity at full scale (T = 100°C, δR = 38.51 Ω):**
- Exact output: 403.4 mV
- Linear approximation: 481.4 mV
- Error: 19% overestimate

**Design decisions:**
- Use V_ex = 5V (good balance of sensitivity and self-heating)
- Use 0.1% precision resistors for fixed arms (to minimize bridge offset)
- Use ratiometric ADC architecture (V_ex feeds ADC reference — excitation drift cancels)

### 4.2 Instrumentation Amplifier

**Topology:** 3 op-amp INA (equivalent to INA128).

**Gain equation:**
```
G = 1 + 50kΩ / R_G
```

**Gain selection for 0–100°C, ADC full scale = 5V:**
```
Max bridge output (100°C) = 403.4 mV
G_required = 5000 / 403.4 = 12.4  → use G = 10 (R_G = 5.56 kΩ)
ADC utilization: 403.4 × 10 / 5000 = 80.7%
```

**CMRR comparison:**

| Amplifier | CMRR | Condition |
|---|---|---|
| Single op-amp diff amp | 28 dB | 1% resistors |
| INA at G=1 | ~86 dB | Internal matching |
| INA at G=10 | ~106 dB | G boosts CMRR |

**Key INA specs (LT1001-based):**
- Input offset voltage: 25 μV typical, 100 μV max
- Offset temperature coefficient: 0.5 μV/°C
- Input impedance: ~40 GΩ (no bridge loading)
- Voltage noise: 10 nV/√Hz

### 4.3 Low-Pass Filter

**Design: 2nd-order Butterworth Sallen-Key, f_c = 1 Hz**

Transfer function:
```
H(s) = ω₀² / (s² + (ω₀/Q)s + ω₀²)    Q = 0.707
```

**Component values:**
- R1 = R2 = 160 kΩ, C1 = 1.5 μF, C2 = 680 nF

**Performance:**
- Attenuation at 1 Hz: −3 dB (cutoff)
- Attenuation at 50 Hz: −68 dB
- Noise bandwidth: 1.57 × f_c = 1.57 Hz

### 4.4 Complete System Sensitivity

```
S_system = G × S_bridge = 10 × 4.81 mV/°C = 48.1 mV/°C
```

**16-bit ADC resolution (5V FS):**
```
ΔT_LSB = (5000 mV / 65536) / 48.1 mV/°C = 1.58 mK/LSB
```

ADC resolution is not the limiting factor. Systematic errors dominate.

---

## 5. Error Analysis

### 5.1 Error Budget Comparison

| Error Source | 2-Wire (°C) | 4-Wire (°C) |
|---|---|---|
| RTD Class B tolerance | ±0.30 | ±0.30 |
| Lead resistance (10m, 0.5mm²) | ±1.79 | 0 |
| Self-heating (1mA, still air) | ±0.02 | ±0.02 |
| Amplifier offset drift (ΔT_amb = 25°C) | ±0.05 | ±0.05 |
| Excitation voltage error (0.2%) | ±0.10 | ±0.10 |
| EMI + noise (1 Hz BW) | ±0.05 | ±0.05 |
| **RSS Total** | **±1.84°C** | **±0.33°C** |

4-wire connection improves total error by **5.6×** simply by eliminating lead resistance.

### 5.2 Noise-Limited Resolution

Total RTI noise (INA dominates):
```
V_n,total = √(V_n,RTD² + V_n,INA²) = √(1.61² + 12.5²) ≈ 12.6 nV/√Hz
```

At 1 Hz noise bandwidth:
```
T_n = 12.6 nV/√Hz × √1.57 Hz / 48.1 mV/°C = 0.33 μK_rms
```

The noise floor is 0.33 μK — thermal noise is irrelevant. Systematic errors are the practical limit.

### 5.3 Error Propagation: Excitation Voltage

If V_ex has uncertainty ΔV_ex:
```
ΔT_Vex = T × ΔV_ex / V_ex
```

For T = 100°C, ΔV_ex = 10 mV (0.2%): ΔT = 0.2°C.
With ratiometric ADC (V_ex = ADC reference): ΔT_Vex → 0.

---

## 6. LTspice Simulation Results

### 6.1 Wheatstone Bridge Simulation

**Test:** Swept R_RTD from 100 Ω (0°C) to 138.51 Ω (100°C).

**Key findings:**
- Bridge output at 100°C: 373.7 mV (exact simulation) vs 481.3 mV (linear prediction)
- Non-linearity: 19% overestimate by linear model
- Sensitivity: 4.85 mV/°C at 0°C, decreasing to 4.35 mV/°C at 100°C (−10.3%)
- With 1% resistor mismatch in fixed arm: 12.5 mV offset at 0°C = 2.6°C systematic error

**Conclusion:** Precise bridge resistors (0.1%) are essential. Linear approximation inadequate above ±25°C from balance point.

### 6.2 Differential Amplifier CMRR Test

**Test:** V_diff = 0, swept V_cm from 2.0 to 3.0V.

**Findings:**
- Matched resistors (theoretical): CMRR → ∞, V_out = 0 for all V_cm
- 1% resistor mismatch: CMRR = 28 dB, 2.5V CM → ~100 mV output error
- 100 mV error / (48.1 mV/°C) = **2.1°C temperature error from CM alone**

**Conclusion:** Single op-amp differential amplifier unsuitable for bridge measurement with standard 1% resistors.

### 6.3 Instrumentation Amplifier Test

**Test:** Same CM sweep with 3-op-amp INA topology at G=10.

**Findings:**
- CMRR with 1% stage-2 mismatch: 86 dB
- 2.5V CM → 0.5 mV output → 0.01°C temperature error
- Input impedance >> 10 MΩ: bridge output unchanged with 500 Ω source impedance
- Gain accuracy: G = 9.98 vs theoretical 10.0 (−0.2% error)

**Conclusion:** INA provides 86× improvement in CMRR over single diff-amp. Required for precision bridge measurement.

### 6.4 Low-Pass Filter AC Analysis

**Test:** AC sweep 0.01 Hz to 10 kHz, 2nd-order Butterworth f_c = 1 Hz.

**Findings:**
- Measured f_c: 0.997 Hz (target: 1.00 Hz, error < 1%)
- Attenuation at 50 Hz: −68.2 dB (target: ≥ 40 dB ✓)
- Passband ripple (0–0.5 Hz): < 0.1 dB ✓
- Phase at 0.1 Hz: −11° (time delay 0.31 s — acceptable for thermal measurement)

### 6.5 Noise Analysis

**Test:** LTspice .noise simulation, 0.01 Hz to 100 Hz.

**Findings:**
- White noise floor (output, G=10): 128 nV/√Hz
- 1/f corner (LT1001): ~3 Hz
- Integrated noise (0.01–1 Hz, white noise + 1/f): ~18 nV_rms RTI
- Temperature equivalent: 18/48.1 mV/°C = 0.37 μK_rms
- SNR for 1°C measurement: 109 dB

---

## 7. Characterization Results

### 7.1 Sensitivity

RTD sensitivity drops from 0.3908 Ω/°C at 0°C to 0.2926 Ω/°C at 850°C (−25%). Systems using constant α = 0.385 Ω/°C accumulate gain error of 25% at the high end of the range.

NTC sensitivity varies from −5989 Ω/°C at −20°C to −19 Ω/°C at 100°C (factor of 315×). High sensitivity near 25°C gives NTC thermistors ~11.6× more bridge output per degree than RTDs at that temperature.

### 7.2 Linearity and Linearization

| Sensor | NL without correction | With correction | Method |
|---|---|---|---|
| RTD (0–100°C) | ±0.37°C | < 0.001°C | CVD inverse equation |
| RTD (full range) | ±63°C | < 0.01°C | CVD inverse equation |
| NTC (0–50°C) | ~18°C | < 0.01°C | Steinhart-Hart equation |
| Type K (0–1000°C) | ~25°C | < 0.05°C | NIST polynomial |

### 7.3 Calibration

Multi-point polynomial calibration (5 points, 0–100°C):
- Before calibration: max error ±1.84°C (2-wire) or ±0.33°C (4-wire)
- After 2nd-order polynomial correction: max residual < 0.01°C
- Improvement factor: ~33×

Calibration uncertainty budget: ±0.07°C (k=2, 95% confidence) from reference thermometer, bath uniformity, and curve fit residuals.

### 7.4 Drift

Long-term drift for PT100 at various operating temperatures:
| Temperature | Drift rate | Calibration interval |
|---|---|---|
| < 100°C | 0.01–0.05°C/year | 12–24 months |
| 100–300°C | 0.05–0.2°C/year | 12 months |
| 300–500°C | 0.1–0.5°C/year | 6–12 months |
| > 500°C | 0.5–5°C/year | 3–6 months |

Amplifier offset drift: LT1001 at 0.5 μV/°C → 0.00026°C per °C of ambient change (G=10). Negligible.

---

## 8. Discussion

### 8.1 Which Sensor is Best?

There is no universally best sensor. Each is optimal in a different context:

**Choose PT100 RTD when:**
- Accuracy requirement < ±0.5°C
- Long-term stability needed (months to years)
- Temperature range −200 to +600°C
- Regulatory traceability required (pharmaceutical, food, metrology)

**Choose NTC Thermistor when:**
- Temperature range is narrow (< 100°C span)
- Maximum sensitivity needed in 0–80°C range
- Cost is critical
- Fast response needed in small package
- Individual calibration is acceptable

**Choose Type K Thermocouple when:**
- Temperature exceeds 600°C (where RTDs degrade)
- Physical ruggedness is paramount
- Lowest cost and simplest installation needed
- Accuracy ±1–2°C is acceptable

### 8.2 Where Does Error Actually Come From?

After full system analysis, the dominant error sources in order of magnitude:

1. **Lead wire resistance (2-wire connection):** ±1.79°C — eliminated by 4-wire
2. **Sensor tolerance (Class B):** ±0.30°C — reduced to < 0.01°C by calibration
3. **Excitation voltage instability:** ±0.10°C — eliminated by ratiometric measurement
4. **Amplifier offset drift:** ±0.05°C — minimized by autozero op-amp
5. **EMI/noise:** ±0.05°C — reduced by shielding and filtering
6. **ADC quantization (16-bit):** ±0.0008°C — negligible
7. **Thermal (Johnson) noise:** ±0.0003°C — negligible

The lesson: signal conditioning choices (2-wire vs 4-wire, resistor quality, reference stability) matter far more than ADC resolution.

### 8.3 Engineering Trade-offs

**Bandwidth vs noise:** Narrowing the filter from 10 Hz to 1 Hz reduces noise by √10 = 3.16× but slows the effective response time. For a thermal sensor with τ = 5 s, the signal bandwidth is << 1 Hz anyway — filtering to 1 Hz costs nothing in information.

**Excitation current vs self-heating:** Higher current → more bridge output (better SNR) but more self-heating error. Optimal current balances these. For PT100 in still air: 1 mA is the standard compromise.

**Gain vs headroom:** Higher INA gain → more sensitivity to small temperature changes → but amplifier saturates at lower temperatures. Design gain for 70–90% ADC utilization at the maximum expected temperature.

---

## 9. Conclusion

This project demonstrates that precision temperature measurement is a system problem, not a sensor problem. The sensor is one component in a chain where every stage contributes error, every design choice has quantifiable consequences, and the final accuracy is determined by the weakest link.

Key conclusions:

1. **Callendar-Van Dusen equation** must be implemented in firmware for any RTD measurement requiring better than ±0.4°C accuracy over a 100°C range.

2. **4-wire RTD connection** is non-negotiable for precision measurement — 2-wire lead resistance error (±1.79°C for 10m cable) dominates all other sources.

3. **Instrumentation amplifier** provides 86 dB CMRR independent of external resistor matching — mandatory for bridge measurements where the signal is small relative to the common-mode voltage.

4. **Noise is not the limiting factor** in this system. At 1 Hz bandwidth, the noise floor is 0.37 μK. Systematic errors (calibration, lead resistance, drift) are the practical limit.

5. **Calibration eliminates systematic errors** — the ±0.30°C RTD tolerance shrinks to < 0.01°C after multi-point polynomial calibration.

6. **Drift determines calibration interval** — PT100 at 100°C requires recalibration every 12–24 months; at 500°C, every 6 months.

7. **Thermistors offer 1000× more sensitivity** at 25°C than RTDs but require mandatory software linearization (Steinhart-Hart) and much lower excitation current (< 0.1 mA vs 1 mA).

The complete, calibrated system achieves better than ±0.1°C accuracy over 0–100°C — limited by calibration uncertainty, not by electronics or ADC resolution.

---

## 10. Future Work

- **Hardware implementation:** Prototype the bridge + INA + filter circuit on a PCB. Measure real noise and CMRR. Compare to simulation.
- **4-wire RTD data acquisition:** Implement with ADS1220 (24-bit sigma-delta ADC with built-in PGA and 4-wire RTD support).
- **Thermocouple cold junction compensation:** Implement MAX31856 CJC IC. Measure CJC accuracy vs reference.
- **Multi-sensor comparison:** Calibrate PT100, NTC, and Type K against a reference SPRT in a stirred bath. Plot comparison.
- **Drift study:** Log sensor reading at constant temperature over 30 days. Plot drift curve. Estimate annual drift rate.
- **Advanced filtering:** Implement digital notch filter at 50 Hz in firmware. Compare to analog notch filter.

---

## Appendix A: Component List

| Component | Value / Part | Purpose |
|---|---|---|
| RTD | PT100, Class B, 6mm SS sheath | Temperature sensor |
| R_fixed (×3) | 100 Ω, 0.1%, 25 ppm/°C | Bridge fixed arms |
| V_ref | LT1460-5 (5V, 20 ppm/°C) | Bridge excitation |
| INA | INA128 or 3× LT1001 | Signal amplification |
| R_G | 5.56 kΩ (G=10) | INA gain setting |
| R_filter (×2) | 160 kΩ, 1%, metal film | LPF Sallen-Key |
| C_filter | 1.5 μF, 680 nF, film | LPF Sallen-Key |
| ADC | ADS1220 (24-bit, 4-wire RTD support) | Digitization |
| Power | ±15V linear supply or ±5V for single supply | Rails |

## Appendix B: Python Scripts

| Script | Output |
|---|---|
| `plots/rtd_bridge_analysis.py` | R(T), bridge output, NL error, sensitivity |
| `plots/thermistor_curves.py` | NTC R(T), sensitivity, S-H residuals, divider |
| `plots/error_propagation.py` | Error budget, self-heating, lead R, noise floor |
| `plots/sensitivity_analysis.py` | Sensor comparison, RTD/NTC dR/dT, ADC resolution |
| `plots/calibration_plot.py` | Calibration correction, residuals, CVD inversion |

## Appendix C: LTspice Simulation Files

| Simulation | File | Key Result |
|---|---|---|
| Wheatstone Bridge | `simulations/wheatstone_bridge/` | Non-linearity 19% at 100°C |
| Differential Amplifier | `simulations/differential_amplifier/` | CMRR 28 dB with 1% R |
| Instrumentation Amplifier | `simulations/instrumentation_amplifier/` | CMRR 86 dB at G=10 |
| Low-Pass Filter | `simulations/filtering/` | −68 dB at 50 Hz |
| Noise Analysis | `simulations/noise_analysis/` | 0.37 μK noise floor |
