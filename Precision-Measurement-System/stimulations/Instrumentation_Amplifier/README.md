# Simulation: Instrumentation Amplifier

## Objective

Simulate a three-op-amp instrumentation amplifier (INA topology) receiving the Wheatstone bridge output. Demonstrate:
1. High input impedance (does not load the bridge)
2. High CMRR independent of external resistor matching
3. Gain set by a single resistor R_G
4. Clean amplification of the bridge's differential signal

---

## Three-Op-Amp INA Topology

```
Stage 1: Buffered pre-amplification
Stage 2: Differential output stage

         R1 = 25kΩ         R1 = 25kΩ
V_A ──┤A1(+)                          ┤─ V_A'
      │A1(-) ─── R_G/2 ─┬─ R_G/2 ─── │A2(-) ─┐
      └──────────────────┘             └───────┤
                                               │
      ┌──────────────────┐             ┌───────┤
      │A3(-) ─── R_G/2 ─┘─ R_G/2 ─── │A4(-) ─┤
V_B ──┤A3(+)                          ┤─ V_B' │
         R1 = 25kΩ         R1 = 25kΩ         │
                                              A5 (diff stage)
                                              │
                                           V_out
```

### Gain Equation

Stage 1 gain (for each input buffer, referred to differential):
```
A₁ = 1 + 2R₁/R_G
```

Stage 2 gain (unity differential with R2=R3=R4=R5 matched):
```
A₂ = 1 (unity for matched stage 2 resistors)
```

Total:
```
G_total = (1 + 2R₁/R_G) × A₂
```

For INA128 equivalent (R₁ = 25 kΩ internal):
```
G = 1 + 50kΩ/R_G
```

---

## Component Values

| Component | Value | Notes |
|---|---|---|
| A1, A2 (Stage 1) | LT1001 or ideal | Input buffers |
| A3 (Stage 2) | LT1001 or ideal | Differential stage |
| R1 (×4) | 25 kΩ | Internal, precisely matched |
| R_G | 5.56 kΩ | Sets G ≈ 10 |
| R2 = R3 = R4 = R5 | 10 kΩ | Stage 2 resistors (1% matched) |
| R_ref | 0 Ω to GND | Reference pin, tied to GND for single-ended output |

**Common gain resistor values (INA128-style):**
| R_G | Gain |
|---|---|
| 499 Ω | 101 |
| 1 kΩ | 51 |
| 5.56 kΩ | 10 |
| 11.1 kΩ | 5.5 |

---

## SPICE Netlist

```spice
* Three-Op-Amp Instrumentation Amplifier
* Gain = 1 + 50k/R_G
* Precision Measurement System

* Supply
Vpos  Vcc  0   DC 15
Vneg  Vee  0   DC -15

* Input signals
* Differential = 100 mV (simulates bridge output at ~21°C)
* Common-mode = 2.5V
Va  nodeA  0  DC 2.55
Vb  nodeB  0  DC 2.45

* ── Stage 1 ──────────────────────────────────────────
* Op-amp A1 (top buffer)
* (+) = Va, (-) feedback through R1 and Rg
XA1  nodeA  negA1  outA1  Vcc  Vee  ideal_opamp

Ra1  outA1  rg_top  25k
Rg   rg_top  rg_bot  5.56k    ; gain resistor
Ra2  rg_bot  negA2  25k

* Op-amp A2 (bottom buffer)
XA2  nodeB  negA2  outA2  Vcc  Vee  ideal_opamp

* Feedback connections (Stage 1 output feeds back to negative inputs)
Rfb1  outA1  negA1  0       ; this is the feedback in the actual INA topology
; Note: In real INA topology, the feedback makes outA1 = Va + G×(Va-Vb)/2
; and outA2 = Vb - G×(Va-Vb)/2

* ── Stage 2 (Differential) ──────────────────────────
Rb1  outA1  neg_A3  10k
Rb2  neg_A3  vout   10k
Rb3  outA2  pos_A3  10k
Rb4  pos_A3  0      10k

XA3  pos_A3  neg_A3  vout  Vcc  Vee  ideal_opamp

* Op-amp subcircuit
.subckt ideal_opamp inp inn out vcc vee
Eout  out  0  VALUE { LIMIT(1e6*(V(inp)-V(inn)), V(vcc)-0.5, V(vee)+0.5) }
.ends

.op
.tran 0.1m 10m     ; transient if needed

.end
```

---

## Simulation Tests

### Test 1: Gain Verification

- V_A = 2.55V, V_B = 2.45V → V_diff = 100 mV
- Expected V_out = G × V_diff = 10 × 100 mV = 1.0 V
- Verify output from `.op` simulation

Change R_G and verify gain follows G = 1 + 50k/R_G:
| R_G | Expected G | V_out |
|---|---|---|
| 5.56 kΩ | 10.0 | 1.00 V |
| 1 kΩ | 51.0 | 5.10 V |
| 499 Ω | 101.2 | 10.12 V |
| 50 Ω | 1001 | Output saturates |

### Test 2: CMRR Measurement

- Set V_A = V_B = 2.5V (zero differential, 2.5V common-mode)
- Measure V_out — should be 0V for ideal case
- In LTspice, deliberately mismatch R3 to 10.1 kΩ (1% error)
- Measure non-zero output → calculate CMRR

For ideal Stage 2 with perfectly matched resistors: CMRR → ∞
For 1% mismatch in Stage 2: CMRR ≈ 86 dB (much better than single diff amp!)

**Why is INA CMRR so much better?**

Because Stage 1 pre-amplifies the differential signal by factor G before Stage 2. Stage 2 still has the same absolute CM error (determined by its resistor matching), but the differential signal has been boosted by G. So:

```
CMRR_INA ≈ G × CMRR_stage2
```

For G = 10 and CMRR_stage2 = 66 dB (0.1% matching):
```
CMRR_INA ≈ 66 + 20 = 86 dB
```

### Test 3: Input Impedance

Replace Va source with a Thevenin source: Va + R_source = 500 Ω (simulating bridge source impedance).

Compare V_out with and without R_source. Ideal INA: no difference (infinite input impedance).

Quantify: If input impedance Z_in >> R_source, output is essentially unchanged. LT1001 has Z_in ≈ 40 GΩ || 5 pF differential.

### Test 4: Full Bridge + INA System

Connect the Wheatstone bridge simulation (from simulations/wheatstone_bridge/) to the INA input:
- nodeA from bridge → Va input of INA
- nodeB from bridge → Vb input of INA
- Sweep R_RTD from 100 to 138.51 Ω (0 to 100°C)

Observe V_out ranges from 0 V to G × V_bridge_max = 10 × 373.7 mV = 3.737 V.

Verify the output is well within the ±15V supply range (it is, with headroom).

---

## Key Takeaways

| Characteristic | Single Diff Amp | INA (G=10) |
|---|---|---|
| CMRR (1% resistors) | ~28 dB | ~86 dB |
| Input impedance | ~R1 = 10 kΩ | ~40 GΩ |
| Gain setting | Two matched resistor pairs | One R_G |
| Bridge loading | Significant (loading error) | Negligible |

The INA solves all three fundamental limitations of the single op-amp differential amplifier. It is the correct choice for precision bridge measurements.

---

## Plots to Generate

1. **V_out vs V_diff** (linearity and gain verification)
2. **CMRR comparison** — matched vs 1% mismatch Stage 2 resistors
3. **Full system: V_out vs Temperature** (bridge + INA combined)
4. **Gain accuracy vs R_G** (measure actual vs theoretical gain)
