# Thermal Modeling

## Introduction

Every thermal sensor is embedded in a physical environment. The sensor does not instantly assume the temperature of its surroundings — it exchanges heat through conduction, convection, and radiation, and its temperature evolves according to thermal dynamics governed by mass, heat capacity, and thermal resistance.

Understanding this thermal model is essential for:
- Predicting sensor response time to temperature changes
- Quantifying self-heating errors from excitation current
- Designing adequate thermal coupling between sensor and medium
- Correctly interpreting dynamic temperature measurements

The model used here is the **lumped-parameter RC thermal model** — the thermal analog of an electrical RC circuit.

---

## The Thermal-Electrical Analogy

| Thermal Domain | Symbol | Electrical Analog | Symbol |
|---|---|---|---|
| Temperature (°C or K) | T | Voltage (V) | V |
| Heat flow (W) | Q̇ | Current (A) | I |
| Thermal resistance (K/W) | R_th | Electrical resistance (Ω) | R |
| Thermal capacitance (J/K) | C_th | Electrical capacitance (F) | C |
| Power dissipation (W) | P | Power dissipation (W) | P |

This analogy lets us apply RC circuit mathematics — step response, frequency response, time constants — directly to thermal problems.

---

## Thermal Resistance

Thermal resistance relates temperature difference to heat flow:
```
ΔT = Q̇ × R_th
```

### Conduction (Fourier's Law)
```
R_th,conduction = L / (k × A)
```
Where L = path length (m), k = thermal conductivity (W/m·K), A = cross-section (m²)

**Material thermal conductivities:**
| Material | k (W/m·K) |
|---|---|
| Platinum | 71.6 |
| Stainless steel (sheath) | 16 |
| Alumina (ceramic fill) | 30 |
| Still air | 0.026 |
| Silicone thermal grease | 3–8 |

### Convection (Newton's Law of Cooling)
```
R_th,convection = 1 / (h × A_s)
```
Where h = convective heat transfer coefficient (W/m²·K), A_s = surface area (m²)

**Typical h values:**
| Condition | h (W/m²·K) |
|---|---|
| Natural convection, air | 5–25 |
| Forced convection, air | 25–250 |
| Natural convection, water | 200–1000 |
| Forced convection, water | 1000–15000 |

This is why RTDs respond 5–10× faster in flowing liquid than still air — h is 40–600× higher, making R_th much smaller.

### Radiation (Stefan-Boltzmann, linearized)
```
R_th,radiation ≈ 1 / (4 ε σ T_mean³ × A_s)
```
Radiation is minor below 300°C for small sensors. Significant above 500°C.

---

## Thermal Capacitance

```
C_th = m × c_p
```

**Material heat capacities:**
| Material | c_p (J/kg·K) | Density (kg/m³) |
|---|---|---|
| Platinum | 133 | 21,450 |
| Stainless steel | 500 | 7,900 |
| Alumina | 850 | 3,960 |

**Example — 6mm OD stainless sheath, 50mm long:**
```
Volume = π × 0.003² × 0.05 = 1.41×10⁻⁶ m³
Mass   = 1.41×10⁻⁶ × 7900 = 0.011 kg
C_th   = 0.011 × 500 = 5.6 J/K    (+ internal fill ≈ 7 J/K total)
```

---

## First-Order Lumped Thermal Model

```
        P_self (self-heating, W)
              |
    T_sensor ─┤ C_th
              |
           R_th
              |
           T_ambient
```

Governing differential equation:
```
C_th × dT_sensor/dt = (T_ambient - T_sensor)/R_th + P_self
```

Thermal time constant:
```
τ_th = R_th × C_th = m·c_p / (h·A_s)
```

---

## Step Response

When T_ambient steps from T₀ to T₁ at t=0 (P_self = 0):
```
T_sensor(t) = T₁ - (T₁ - T₀) × e^(-t/τ_th)
```

Key milestones:
| Time | % of final temperature reached |
|---|---|
| t = τ | 63.2% |
| t = 2τ | 86.5% |
| t = 3τ | 95.0% |
| t = 5τ | 99.3% (settled) |

**Datasheet time constants:**
- t50 (50%): τ × ln(2) = 0.693τ
- t90 (90%): τ × ln(10) = 2.303τ

**Typical RTD time constants:**
| Configuration | Medium | τ (s) |
|---|---|---|
| Bare wire | Flowing air (1 m/s) | 0.1–0.5 |
| Thin-film, unsheathed | Still air | 2–10 |
| 6mm SS sheath | Still air | 30–60 |
| 6mm SS sheath | Flowing water | 3–10 |

---

## Frequency Domain (Sensor as Low-Pass Filter)

Transfer function of first-order thermal sensor:
```
H(jω) = K / (1 + jω τ_th)
```

-3 dB bandwidth:
```
f_c = 1 / (2π τ_th)
```

For τ = 5 s:
```
f_c = 0.032 Hz   → sensor can only follow changes slower than ~31 s period
```

Temperature changes faster than f_c are **attenuated and delayed** — the sensor physically cannot follow them. This sets the fundamental measurement bandwidth, which no signal processing can overcome.

---

## Self-Heating Analysis

Excitation current I through resistance R(T) dissipates:
```
P_self = I² × R(T)
```

Steady-state temperature elevation:
```
ΔT_self = R_th × I² × R(T)
```

**PT100 self-heating table (R_th = 200 K/W, still air):**
| I (mA) | P_self (mW) | ΔT_self (°C) |
|---|---|---|
| 0.1 | 0.001 | 0.0002 |
| 0.5 | 0.025 | 0.005 |
| 1.0 | 0.100 | 0.020 |
| 2.0 | 0.400 | 0.080 |
| 5.0 | 2.500 | 0.500 |

Maximum current for ΔT_self < 0.05°C, still air:
```
I_max = √(0.05 / (200 × 100)) = √(2.5×10⁻⁶) = 1.58 mA
```
Standard practice: use 1 mA for PT100 in air.

For PT1000 same conditions: I_max = √(0.05 / (200 × 1000)) = 0.5 mA — lower current but 10× more bridge output voltage per degree.

---

## Two-Body Model (Sheathed RTD)

More accurate: treat sheath and element as separate thermal masses:

```
T_ambient → [R_th,ext] → T_sheath → [R_th,int] → T_element
                     C_th,sheath              C_th,element
```

This gives a two-time-constant (second-order) step response:
```
T_element(t) = T_final + A₁·e^(-t/τ₁) + A₂·e^(-t/τ₂)
```

- τ₁ (fast): internal resistance × element mass
- τ₂ (slow): external resistance × total mass — the one specified in datasheets

---

## Improving Response Time

| Method | Effect on τ |
|---|---|
| Reduce sheath diameter (6→3 mm) | Reduces C_th by 4×, τ by ~2–3× |
| Increase fluid velocity | Reduces R_th,ext (higher h), τ decreases |
| Thermal grease in air gaps | Reduces R_th,int dramatically |
| Use bare thin-film element | Removes sheath mass entirely |
| Increase immersion depth | Reduces conduction loss along sheath stem |

---

## Conclusion

The thermal RC model gives quantitative answers to:
- Why does this sensor respond slowly? → high C_th or high R_th
- How much does self-heating shift the reading? → ΔT = R_th × I² × R
- Can this sensor track a 0.1 Hz temperature oscillation? → check f_c vs 0.1 Hz
- How long to wait after a step change before reading? → 5τ

Every number in this model can be estimated from sensor geometry and material properties, or read from the manufacturer's response time specification.
