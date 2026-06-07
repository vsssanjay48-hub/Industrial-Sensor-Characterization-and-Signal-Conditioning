# Simulation: Differential Amplifier

## Objective

Simulate a single op-amp differential amplifier receiving the Wheatstone bridge output. Measure gain, offset, and Common-Mode Rejection Ratio (CMRR). Understand the limitations that motivate the use of an instrumentation amplifier.

---

## Circuit Description

```
V_A (from bridge node A) ──── R1 ────┬──── op-amp (−) input
                                      │
                                     R2
                                      │
                                   op-amp output  ──── V_out
V_B (from bridge node B) ──── R3 ────┬──── op-amp (+) input
                                      │
                                     R4
                                      │
                                     GND
```

**Gain = R2/R1 (when R1=R3 and R2=R4)**

---

## Component Values

| Component | Simulation 1 (Gain=10) | Simulation 2 (CMRR test) |
|---|---|---|
| R1 | 10 kΩ | 10 kΩ |
| R2 | 100 kΩ | 100 kΩ |
| R3 | 10 kΩ | 10 kΩ |
| R4 | 100 kΩ | 101 kΩ (1% mismatch) |
| Op-amp | LT1001 (low offset) | LT1001 |
| V_supply | ±15V | ±15V |

---

## SPICE Netlist

```spice
* Single Op-Amp Differential Amplifier
* Precision Measurement System

* Supply rails
Vpos  Vcc  0   DC 15
Vneg  Vee  0   DC -15

* Input sources (bridge outputs)
* Common mode voltage = 2.5V (bridge midpoint)
* Differential voltage = 0 to 400 mV
Vcm  vcm  0   DC 2.5    ; common-mode
Vdiff  vdiff  0   DC 0  ; differential (will sweep)

* Generate Va and Vb from common mode + differential
*  V_A = Vcm + Vdiff/2
*  V_B = Vcm - Vdiff/2
Ea   nodeA   0   vcm  0   1
Ediff_a  nodeA  va_out  vdiff  0  0.5
Eb   nodeB   0   vcm  0   1
Ediff_b  nodeB  vb_out  vdiff  0  -0.5

* Differential amplifier
R1  va_out  inverting_in  10k
R2  inverting_in  vout     100k
R3  vb_out  noninverting_in  10k
R4  noninverting_in  0    100k

* Op-amp (LT1001 model or ideal)
.subckt ideal_opamp inp inn out vcc vee
Eout  out  0  VALUE { LIMIT(1e6*(V(inp)-V(inn)), V(vcc)-1, V(vee)+1) }
.ends

Xopa  noninverting_in  inverting_in  vout  Vcc  Vee  ideal_opamp

.dc Vdiff 0 0.4 0.01

.meas dc GAIN find V(vout)/V(vdiff) WHEN V(vdiff)=0.1

.end
```

---

## Simulation Tests

### Test 1: Differential Gain

- Set V_cm = 2.5V (constant)
- Sweep V_diff from 0 to 400 mV (bridge output range)
- Expected output: 0 to 4.0 V (gain = 10)
- Verify: V_out = (R2/R1) × V_diff = 10 × V_diff

Measure actual gain from slope: G_actual = ΔV_out / ΔV_diff.

### Test 2: Common-Mode Rejection

- Set V_diff = 0 (balance bridge — both inputs equal)
- Sweep V_cm from 2.0 V to 3.0 V (bridge common mode varies with temperature)
- Ideal output: 0 V for all V_cm (differential amplifier should reject CM)
- Actual output: Small, non-zero voltage due to resistor mismatch

**With perfectly matched resistors (R1=R3=10k, R2=R4=100k):**
```
V_out,cm = V_cm × [(R4/(R3+R4)) - (R2/(R1+R2))] × (1 + R2/R1)
         = V_cm × [0.909 - 0.909] × 11 = 0 V    (ideal)
```

**With 1% mismatch (R4 = 101 kΩ instead of 100 kΩ):**
Change R4 = 101 kΩ in simulation.

Measure CM output. Calculate:
```
CMRR = 20 × log₁₀(G_differential / G_common_mode)    [dB]
```

For 1% resistor mismatch, theoretical CMRR ≈ 28 dB (voltage gain of ~25 for CM vs gain of ~10 for differential). In simulation, verify this.

### Test 3: Output Offset

With V_diff = 0 and V_cm = 2.5V, the ideal output should be 0V.

In LTspice, use LT1001 op-amp model (realistic offset voltage ~25 μV). Measure actual output offset. Convert to equivalent temperature error: V_offset / (G × S_bridge) where S_bridge = 4.81 mV/°C.

### Test 4: Frequency Response

Replace DC sweep with AC sweep. Apply small-signal V_diff = 10 mV AC.

Sweep from 1 Hz to 1 MHz. Observe -3 dB bandwidth.

For LT1001 (GBW = 800 kHz) at gain 10:
```
f_-3dB ≈ GBW / G = 800kHz / 10 = 80 kHz
```

For thermal measurement (signal < 1 Hz), this is more than adequate.

---

## Expected Findings

| Test | Expected Observation |
|---|---|
| Differential gain | Very close to R2/R1 = 10 |
| CM rejection (matched R) | > 80 dB |
| CM rejection (1% mismatch) | ~28 dB |
| Output offset (LT1001) | ~0.25 mV → ~0.005°C temperature error |
| Bandwidth | ~80 kHz (excess for thermal measurement) |

---

## Key Conclusions

The single op-amp differential amplifier has one critical weakness: **CMRR degrades drastically with resistor mismatch**. With 1% resistors, CMRR is only ~28 dB — meaning a 2.5V common-mode signal produces ~56 mV of output noise.

For the bridge output range of ~400 mV and CM level of 2.5V, the CM error is:
```
V_cm_error = 2.5V × 10^(-28/20) = 2.5 × 0.04 = 100 mV
```

This is larger than the signal itself at low temperatures. **The single op-amp differential amplifier is inadequate for this application without precision matched resistors.**

This motivates the instrumentation amplifier (INA) in the next simulation — which achieves high CMRR independent of individual resistor matching.

---

## Plots to Generate

1. **V_out vs V_diff** — verify linearity and gain
2. **V_cm output vs V_cm input** — quantify CMRR
3. **Bode plot** — V_out magnitude vs frequency
