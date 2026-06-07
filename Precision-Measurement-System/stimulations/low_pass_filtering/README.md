# Simulation: Low-Pass Filtering

## Objective

Design and simulate a low-pass filter for the precision thermal measurement system. Demonstrate noise reduction, attenuation of 50 Hz power-line interference, and the trade-off between bandwidth and noise floor.

---

## Filter Design Requirements

**Signal characteristics:**
- Thermal sensor signal bandwidth: DC to ~0.5 Hz (temperature changes slowly)
- RTD time constant τ ≈ 3 s → f_c,sensor ≈ 0.053 Hz

**Noise sources to reject:**
- 50 Hz power-line hum (dominant industrial noise)
- Switching regulator noise (typically 50–500 kHz)
- Broadband amplifier noise

**Design goal:** Attenuate 50 Hz by at least 40 dB while passing DC to 1 Hz with less than 1 dB attenuation.

---

## Stage 1: Single-Pole RC Filter (f_c = 1 Hz)

```
R = 160 kΩ
C = 1 μF
f_c = 1/(2π RC) = 1/(2π × 160k × 1μ) = 0.995 Hz ≈ 1 Hz
```

**Transfer function:**
```
H(s) = 1 / (1 + s/ω_c)    where ω_c = 2π × 1 Hz = 6.28 rad/s
```

**Attenuation at 50 Hz:**
```
|H(j×2π×50)| = 1/√(1 + (50/1)²) = 1/50.01 = -34 dB
```

Close to the 40 dB goal but not quite there. Use a 2-stage filter.

---

## Stage 2: Two-Pole Active Filter (Sallen-Key, Butterworth)

For 40 dB at 50 Hz with 1 dB passband ripple up to 1 Hz:

A 2nd-order Butterworth (Q = 0.707) with f_c = 1 Hz:
```
Attenuation at 50 Hz = (50/1)^2 / √(1 + (50/1)^4) ≈ 2500/2500 = 1 → -68 dB
```

Wait, correct calculation for 2nd order Butterworth:
```
|H(jω)| = 1 / √(1 + (ω/ω_c)^(2×2)) = 1 / √(1 + (50/1)^4) = 1/2500 = -68 dB
```

**68 dB attenuation at 50 Hz** — more than sufficient.

### Sallen-Key Circuit (Unity Gain Butterworth 2nd Order)

```
V_in ── R1 ──┬── R2 ──┬── op-amp(+) ── V_out
             │         │
             C2       C1
             │         │
            GND       GND
             │
          op-amp(-) (feedback from V_out)
```

For 2nd-order Butterworth with f_c = 1 Hz, unity gain (Q = 0.707):
```
R1 = R2 = R = 112 kΩ
C1 = 2Q × C = 2 × 0.707 × C = 1.414 C
C2 = C / (2Q) = C / 1.414 = 0.707 C
```

Choose C = 1 μF:
```
C1 = 1.414 μF → use 1.5 μF
C2 = 0.707 μF → use 680 nF

R = 1/(2π × f_c × √(C1 × C2)) = 1/(2π × 1 × √(1.5μ × 0.68μ))
  = 1/(2π × 1.01×10⁻³) = 157.6 kΩ → use 160 kΩ
```

---

## SPICE Netlist

```spice
* Low-Pass Filter Simulation
* 2nd Order Butterworth Sallen-Key, f_c = 1 Hz
* Precision Measurement System

Vcc  vcc  0  DC 15
Vee  vee  0  DC -15

* Input: combination of signal + 50 Hz noise + DC
Vsig  vin  0  SIN(1.0  0.1  0.1)  ; 0.1 V amplitude, 0.1 Hz signal + 1V DC bias
Vnoise  vnoise  0  SIN(0  0.01  50)  ; 10 mV at 50 Hz

* Sum sources (use VCVS)
Esum  vin_total  0  VALUE { V(vin) + V(vnoise) }

* Sallen-Key filter
R1  vin_total  n1  160k
R2  n1  noninv  160k
C1  noninv  0    1.5u
C2  n1  vfilt   0.68u

* Op-amp (unity gain buffer for Sallen-Key)
XA1  noninv  vfilt  vfilt  vcc  vee  ideal_opamp

.subckt ideal_opamp inp inn out vcc vee
Eout  out  0  VALUE { LIMIT(1e6*(V(inp)-V(inn)), V(vcc)-0.5, V(vee)+0.5) }
.ends

* Transient: observe filtering of 50 Hz noise
.tran 1m 10    ; 10 seconds, 1 ms steps

* AC analysis for Bode plot
.ac dec 100 0.01 1000    ; 0.01 Hz to 1000 Hz

.end
```

---

## Simulation Tests

### Test 1: AC Frequency Response (Bode Plot)

Run `.ac dec 100 0.01 1000` simulation.

Plot V(vfilt)/V(vin_total) in dB vs frequency.

**Expected Bode plot:**
- DC to 1 Hz: flat at 0 dB (no attenuation)
- At 1 Hz: -3 dB (cutoff)
- At 10 Hz: -40 dB (2 decades below 1 Hz, 2nd order = -40 dB/decade)
- At 50 Hz: -68 dB
- At 100 Hz: -80 dB

Measure actual -3 dB frequency. Verify it is within 10% of 1 Hz.

### Test 2: 50 Hz Noise Suppression (Transient)

Input: 1 V DC + 10 mV at 0.1 Hz (signal) + 10 mV at 50 Hz (noise).

Without filter: Signal + 10 mV noise → SNR = 20 × log(10/10) = 0 dB.

After filter (at 0.1 Hz signal, ~0 dB attenuation):
- Signal passes essentially unchanged
- 50 Hz noise attenuated by -68 dB → residual noise = 10 mV × 10^(-68/20) = 0.4 μV

Post-filter SNR: 20 × log(10 mV / 0.4 μV) = 88 dB improvement.

Run transient simulation. Plot V(vin_total) and V(vfilt) together. The 50 Hz ripple on vin_total should be invisible on vfilt.

### Test 3: Phase Response

From the AC simulation, plot phase of V(vfilt)/V(vin_total) vs frequency.

At 1 Hz: phase = -90° (second order system at cutoff).
At 0.1 Hz: phase ≈ -11° (some phase delay even within passband).

For dynamic temperature measurement, phase delay means the output lags the true temperature change. Quantify:

Time delay at 0.1 Hz: φ = 11° → t_delay = 11/(360 × 0.1) = 0.31 s.

### Test 4: Effect of Cutoff Frequency on Noise

Change R1 = R2 to vary f_c from 0.1 Hz to 10 Hz:
| f_c | R (kΩ) | Noise BW (Hz) | 50 Hz attenuation (dB) |
|---|---|---|---|
| 0.1 Hz | 1.6 MΩ | 0.157 | -108 dB |
| 0.5 Hz | 332 kΩ | 0.785 | -82 dB |
| 1 Hz | 160 kΩ | 1.57 | -68 dB |
| 5 Hz | 32 kΩ | 7.85 | -40 dB |
| 10 Hz | 16 kΩ | 15.7 | -28 dB |

The noise bandwidth = π/2 × f_c for a single-pole filter, and different for higher-order filters. Lower cutoff → less noise, but slower response and more phase delay.

---

## Component Selection Notes

**Resistors:** Use metal film (25 ppm/°C TCR), 1% tolerance. Tighter tolerance improves Q accuracy and therefore the sharpness of the -3 dB point.

**Capacitors:** Film capacitors (polyester, polypropylene) for stability. Avoid ceramic capacitors for values above 10 nF in precision filters — they have voltage coefficient and microphonics issues.

**Op-amp:** Choose an op-amp with:
- Input offset voltage < 1 mV (to avoid output offset)
- Low 1/f noise corner (< 100 Hz)
- Rail-to-rail output if using single supply
- Slew rate >> 2π × f_c × V_amplitude (not an issue for 1 Hz filters)

Recommended: LT1001, OPA188, AD8628 (autozero, ultralow offset).

---

## Plots to Generate

1. **Bode plot** (magnitude and phase) — AC analysis, 0.01 Hz to 1 kHz
2. **Step response** — input step, observe filter settling time (≈ 1/f_c × 5 = 5 s)
3. **Noise suppression transient** — input with 50 Hz noise, compare pre/post filter
4. **f_c variation** — overlay Bode plots for f_c = 0.1, 1, 10 Hz
