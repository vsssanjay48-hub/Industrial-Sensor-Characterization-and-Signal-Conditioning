# Signal Conditioning

## Introduction

A raw sensor output is rarely in a form suitable for direct measurement, digitization, or control. The signal may be:
- Too small (a PT100 RTD produces only ~0.385 mV per °C change at 1 mA excitation)
- Contaminated with noise (50/60 Hz hum, switching transients, EMI)
- Non-differential (referenced to ground, losing noise rejection)
- Non-linear (thermistors can span decades of resistance)
- At high impedance (susceptible to loading by downstream circuitry)

Signal conditioning is the art and engineering of transforming the raw sensor signal into a clean, amplified, bandwidth-limited signal suitable for accurate measurement.

The signal conditioning chain in this project:

```
RTD Resistance Change
        ↓
Wheatstone Bridge    → Converts ΔR to differential voltage
        ↓
Instrumentation Amplifier  → Amplifies differential signal, rejects CM noise
        ↓
Low-Pass Filter      → Removes high-frequency noise, limits bandwidth
        ↓
ADC Input            → Clean, scaled signal ready for digitization
```

---

## Wheatstone Bridge

### Purpose and Operating Principle

A Wheatstone bridge converts a resistance change (from a sensor) into a voltage. It is the standard interface circuit for resistive sensors: RTDs, thermistors, and strain gauges.

The basic bridge circuit:

```
        V_ex (+)
           |
       R1 (RTD)   R3 (fixed)
           |            |
     A ───────────────── B     ← Differential output taken here
           |            |
       R2 (fixed)  R4 (fixed)
           |
        GND (-)
```

Output voltage (general case):
```
V_out = V_A - V_B = V_ex × [R1/(R1+R2) - R4/(R3+R4)]
```

**Balance condition** (V_out = 0):
```
R1/R2 = R4/R3
```

For a balanced bridge with R1=R2=R3=R4=R₀ (all arms equal):
```
V_out = V_ex × [R₀/(2R₀) - R₀/(2R₀)] = 0
```

### Sensitivity Analysis

When one arm (R1 = RTD) changes by δR from the balanced value R₀:

```
V_out = V_ex × [(R₀+δR)/(2R₀+δR) - 1/2]
      = V_ex × [δR / (2(2R₀+δR))]
```

For small δR << R₀ (linearized, quarter-bridge):
```
V_out ≈ V_ex × δR / (4R₀)
```

Bridge sensitivity in V/Ω:
```
S_bridge = ∂V_out/∂R1 ≈ V_ex / (4R₀)
```

Combined with RTD sensitivity (dR/dT = α R₀ for PT100, α = 3.85×10⁻³ /°C):
```
dV_out/dT = S_bridge × dR/dT = (V_ex / 4R₀) × (α R₀) = V_ex × α / 4
```

For V_ex = 5V:
```
dV_out/dT = 5 × 3.85×10⁻³ / 4 = 4.81 mV/°C
```

This 4.81 mV/°C is the bridge sensitivity — the signal level the instrumentation amplifier must work with.

### Non-Linearity of the Bridge

The quarter-bridge equation without linearization:
```
V_out = V_ex × δR / (2(2R₀ + δR))
```

The linearized approximation (δR << R₀):
```
V_out,linear = V_ex × δR / (4R₀)
```

The non-linearity error:
```
ε_NL = (V_out,linear - V_out) / V_out,full_scale × 100%
```

For a PT100 RTD measuring 0 to +100°C, δR_max = 100 × 0.385 = 38.5 Ω:
```
δR_max / R₀ = 38.5 / 100 = 0.385
```

Non-linearity error at full scale ≈ δR/(4R₀ + 2δR) × 100% ≈ 4.6% of reading

This is acceptable for moderate precision but must be corrected for better than ±1% accuracy. Correction methods:
- Software linearization using the Callendar-Van Dusen equation
- Half-bridge or full-bridge configurations (reduce non-linearity)
- Ratio-metric measurement techniques

### Full Bridge Configuration

For maximum sensitivity and linearity, use a full (Wheatstone) bridge with all four arms active — two increasing and two decreasing in opposite arms:

```
V_out = V_ex × δR / R₀    [full bridge, all four arms active]
```

This gives 4× the sensitivity of a quarter bridge and inherently cancels non-linearity to first order. Used in precision load cells, pressure sensors, and strain gauges.

### Bridge Excitation

**Voltage excitation:** Provides stable output sensitivity (V_out/V_ex ratio is constant). Used in most precision systems. Requires a stable voltage reference.

**Current excitation:** Output is V_out = I_ex × δR/2 (for small δR). Immunity to lead wire resistance variations. But self-heating power I²R changes with temperature.

**Ratiometric measurement:** Feed the same excitation voltage to both the bridge and the ADC reference. Supply variations cancel out:
```
V_out / V_ex = δR / (4R₀)    [independent of V_ex magnitude]
```

---

## Differential Amplifier

### Purpose

The bridge output is a differential voltage floating above a common-mode voltage of approximately V_ex/2. A differential amplifier amplifies the difference V_A - V_B while rejecting the common-mode component (V_A + V_B)/2.

### Basic Circuit (Single Op-Amp)

```
           R2
    R1     
V_A ──/\/\/─┬─────┤-\
            │         \
           R3          >── V_out
    R4     │         /
V_B ──/\/\/─┴─────┤+/
          GND
```

Transfer function (when R1=R3 and R2=R4):
```
V_out = (R2/R1) × (V_A - V_B)
```

The gain is R2/R1.

### Common-Mode Rejection Ratio (CMRR)

The CMRR quantifies how well the amplifier rejects common-mode signals:
```
CMRR = 20 × log₁₀(A_differential / A_common-mode)    [dB]
```

An ideal differential amplifier has CMRR = ∞ (perfectly rejects CM). Real amplifiers have finite CMRR.

**CMRR of single op-amp differential amplifier depends critically on resistor matching.** For resistors with tolerance ε:
```
CMRR ≈ 20 × log₁₀(1 / 4ε)    [dB]
```

With 1% resistors: CMRR ≈ 28 dB (poor!)
With 0.01% resistors: CMRR ≈ 68 dB (good)
With precision monolithic resistor network: CMRR ≈ 86 dB (excellent)

This is why the single op-amp differential amplifier is rarely used alone in precision instrumentation — the achievable CMRR is limited by resistor matching.

### Input Impedance Problem

The single op-amp differential amplifier has moderate input impedance (~R1+R2 on each input, typically 10–100 kΩ). When driven from a bridge with non-zero source impedance, any imbalance in source impedance causes gain error.

---

## Instrumentation Amplifier (INA)

### Three Op-Amp Topology

The instrumentation amplifier solves both the CMRR and input impedance problems. The standard 3-op-amp INA topology:

```
Stage 1: Buffer + Pre-amplification (two op-amps)
Stage 2: Differential gain (one op-amp)
```

**Stage 1 (input buffer pair):**
```
V_A ──┤+\           /── V_A'
      |  >─ R1 ─┬─ R_gain ─┬─ R1 ─
      |  <─────/   |        |     \
      |              R_gain |      >── V_B'
      ├─────────────────────┘      |
V_B ──┤+\                        /
      |  >─────────────────────/
```

Stage 1 gain:
```
A₁ = 1 + 2R₁/R_gain
```

**Stage 2 (differential amplifier):**
```
A₂ = R2/R1    (with matched R2 and R1)
```

**Total gain:**
```
A_total = A₁ × A₂ = (1 + 2R₁/R_gain) × (R2/R1)
```

For INA128 (Texas Instruments) style:
```
G = 1 + 50kΩ/R_G
```

Common gain resistor values and resulting gain:
| R_G | Gain |
|---|---|
| 49.9 Ω | 1002 |
| 499 Ω | 101 |
| 4.99 kΩ | 11 |
| Open | 1 |

### Key INA Specifications

**CMRR:** 80–120 dB depending on device. Independent of gain resistor matching because Stage 1 pre-amplifies the differential signal before the differential stage — the CM signal appears unchanged at Stage 2 while the differential signal is amplified.

**Input impedance:** Very high — typically 10 GΩ differential, 10 GΩ to each supply rail. Stage 1 uses unity-gain buffer inputs. Loading of the bridge source is negligible.

**Offset voltage:** INAs have specified offset voltage (e.g., INA128: 25 μV typical, 100 μV maximum). Over temperature, this drifts (e.g., 0.5 μV/°C).

Referred-to-temperature error from offset drift:
```
ΔT_offset = V_os_drift × ΔT_ambient / (G × S_bridge)
```

For G=100, S_bridge = 4.81 mV/°C, V_os_drift = 0.5 μV/°C, ΔT_ambient = 25°C:
```
ΔT_offset = (0.5×10⁻⁶ × 25) / (100 × 4.81×10⁻³) ≈ 0.0026°C
```

Negligible — the INA is well-suited for this application.

**Gain error:** Typically ±0.5% for INA128. This is a systematic gain error that scales with temperature measurement range.

**Gain bandwidth product:** At high gains, bandwidth is reduced. Check that the INA bandwidth at the operating gain exceeds the required measurement bandwidth.

### Gain Selection

Choose gain G to map the expected bridge output range to the ADC input range:

Example: Bridge output range 0 to 481 mV (for 0 to 100°C at 4.81 mV/°C), ADC input range 0 to 5V:
```
G_required = 5V / 481 mV ≈ 10.4
```

Use G = 10 (R_G = 5.56 kΩ for INA128). This leaves a small headroom below the ADC full scale.

---

## Filtering

### Why Filter?

The conditioned signal contains:
- The desired measurement signal (low frequency, << 10 Hz for thermal systems)
- Noise within the signal bandwidth (cannot be removed without signal loss)
- Out-of-band noise (50/60 Hz power line hum, switching noise at kHz)
- Aliases that would fold back into the signal band when sampled by an ADC

A low-pass filter removes the out-of-band components, improving SNR.

### Anti-Aliasing

When an ADC samples at rate f_s, any signal component at frequency f_s - f_signal will alias back to f_signal in the digital domain. To prevent aliasing:

**Shannon-Nyquist theorem:**
```
f_s ≥ 2 × f_max_signal
```

The anti-aliasing filter must attenuate all signal components above f_s/2 before the ADC input. This filter is part of the signal conditioning chain.

### RC Low-Pass Filter

The simplest low-pass filter: one resistor and one capacitor.

Transfer function:
```
H(jω) = 1 / (1 + jωRC)
```

-3 dB cutoff frequency:
```
f_c = 1 / (2π RC)
```

Magnitude response (Bode plot):
- Below f_c: |H| ≈ 1 (0 dB attenuation)
- At f_c: |H| = 1/√2 = -3 dB
- Above f_c: |H| rolls off at -20 dB/decade

For thermal measurements, choose f_c to match the sensor bandwidth:
```
f_c_filter ≈ 2 to 5 × f_c_sensor
```

This passes the full sensor signal with < 1 dB loss while rejecting higher frequency noise.

**Design example:** τ_sensor = 3 s (RTD), f_c_sensor = 0.053 Hz. Choose f_c_filter = 0.5 Hz:
```
RC = 1 / (2π × 0.5) = 0.318 s
```

If R = 10 kΩ: C = 31.8 μF (use 33 μF)

Check: The 50 Hz rejection at this filter cutoff:
```
Attenuation at 50 Hz = 1 / √(1 + (50/0.5)²) = 1/100 = -40 dB
```

50 Hz noise is attenuated by 40 dB (100×) — typically sufficient.

### Higher-Order Filters

For steeper roll-off, cascade multiple RC stages or use active filter designs:

**Butterworth filter:** Maximally flat passband. Roll-off = -20n dB/decade for nth order.
- 2nd order: -40 dB/decade
- 4th order: -80 dB/decade

Transfer function (2nd order Butterworth):
```
H(s) = ω₀² / (s² + (ω₀/Q)s + ω₀²)
```

Where Q = 1/√2 ≈ 0.707 for Butterworth (maximally flat).

**Active Sallen-Key topology (2nd order low-pass):**
- Uses one op-amp plus two RC sections
- Unity-gain (voltage follower) or fixed-gain configuration
- Low output impedance, easy to cascade

### Notch Filter (50/60 Hz rejection)

In environments with severe 50/60 Hz interference, a narrow notch filter can be added:

**Twin-T notch filter:**
```
f_notch = 1 / (2π RC)
```

Provides very high attenuation (theoretically infinite) at f_notch, with minimal effect on other frequencies. Sensitive to component tolerance — use precision components.

### Noise Bandwidth vs -3 dB Bandwidth

The -3 dB bandwidth is not the same as the noise bandwidth. For a first-order RC filter:
```
BW_noise = π/2 × f_c = 1.57 × f_c
```

This is important for calculating integrated noise power:
```
V_n,rms = √(S₀ × BW_noise) = √(S₀ × π/(2RC) / (2π)) = √(S₀ / (4RC))
```

---

## Practical PCB Considerations

These aspects are beyond theory but critical for real implementation:

**Decoupling capacitors:** Place 100 nF ceramic capacitors between supply pins of every active device and ground, as close to the device as possible. Prevents supply noise coupling.

**Guard traces:** For high-impedance nodes, surround PCB traces with a guard ring at the same potential as the signal. Prevents leakage currents across the board surface.

**Differential routing:** Route differential pairs (bridge output to INA) as closely coupled as possible, with equal trace lengths. This ensures common-mode noise couples equally to both lines.

**Ground plane:** Use a solid copper ground plane on one PCB layer. This provides a low-impedance return path and shields signal traces from electric fields.

**Separation of analog and digital circuitry:** Keep ADC and microcontroller (digital switching noise) physically separated from the analog front end. Connect the two ground planes at a single point.

**Input protection:** Add ESD protection diodes and series resistors at any input that could be exposed to overvoltage. Especially important for thermocouple inputs, which are often connected to high-voltage equipment.

---

## Summary

| Circuit | Function | Key Specification |
|---|---|---|
| Wheatstone Bridge | ΔR → V_diff | Sensitivity, linearity |
| Differential Amplifier | Amplify V_diff, reject CM | CMRR, gain |
| Instrumentation Amplifier | High-Z input, precise gain | CMRR, offset, gain error |
| Low-Pass Filter | Noise reduction, anti-aliasing | f_c, order, roll-off |
| Notch Filter | 50/60 Hz rejection | f_notch, attenuation |

The complete signal conditioning chain must be designed as an integrated system — each stage affects the noise, bandwidth, and accuracy of the overall measurement.
