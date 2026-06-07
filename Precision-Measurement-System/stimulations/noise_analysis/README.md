# Simulation: Noise Analysis

## Objective

Simulate the noise floor of the complete RTD measurement chain in LTspice. Identify each noise contributor, compute total referred-to-input (RTI) noise, and determine the minimum resolvable temperature change. Understand how bandwidth reduction improves resolution.

---

## Noise Sources in the Measurement Chain

```
RTD (100 Ω)          Johnson noise: V_n = √(4kTR·BW)
     ↓
Bridge fixed resistors    Each 100 Ω arm contributes Johnson noise
     ↓
INA (G = 10)         Voltage noise: e_n (nV/√Hz)
                      Current noise: i_n (pA/√Hz)
     ↓
Low-pass filter      Noise bandwidth ≠ -3dB bandwidth
     ↓
ADC                  Quantization noise = LSB/√12
```

---

## Theoretical Noise Calculation (Pre-Simulation Reference)

### Step 1: Johnson Noise of RTD at 300 K, BW = 1.57 Hz (noise BW of 1 Hz filter)

```
V_n,RTD = √(4 × 1.38×10⁻²³ × 300 × 100 × 1.57)
        = √(2.60×10⁻¹⁸)
        = 1.61 nV_rms
```

### Step 2: Johnson Noise of Three Bridge Resistors (each 100 Ω in series with signal path)

Effective noise resistance seen at bridge output ≈ R₀||R₀ + R₀||R₀ = 100 Ω:
```
V_n,bridge_R = √(4 × 1.38×10⁻²³ × 300 × 100 × 1.57) = 1.61 nV_rms
```

### Step 3: INA Input Voltage Noise (LT1001 based: e_n = 10 nV/√Hz)

```
V_n,INA = e_n × √(BW_noise) = 10×10⁻⁹ × √1.57 = 12.5 nV_rms
```

### Step 4: INA Current Noise × Source Impedance

Source impedance seen by INA input = R₀||R₀ = 50 Ω (bridge Thevenin resistance).

INA current noise i_n = 0.12 pA/√Hz (LT1001):
```
V_n,current = i_n × Z_source × √BW = 0.12×10⁻¹² × 50 × √1.57 = 7.5 pV_rms
```

Negligible compared to voltage noise.

### Step 5: Total RTI Noise (RSS)

```
V_n,total,RTI = √(V_n,RTD² + V_n,bridge² + V_n,INA²)
              = √(1.61² + 1.61² + 12.5²) nV
              = √(2.59 + 2.59 + 156.25) nV
              = √161.43 nV
              = 12.7 nV_rms
```

The INA amplifier noise dominates (98% of total noise power).

### Step 6: Referred-to-Temperature (RTT) Noise

Bridge sensitivity at G=10: S_total = G × (V_ex × α/4) = 10 × 4.81 mV/°C = 48.1 mV/°C

```
T_n = V_n,total,RTI / S_total = 12.7×10⁻⁹ / 48.1×10⁻³ = 2.64×10⁻⁷ °C_rms
```

**This is 0.26 μK RMS noise — extraordinarily low.**

In practice, the limit is not thermal noise but 1/f noise, EMI, and ADC quantization.

---

## LTspice Noise Simulation

### Netlist

```spice
* Noise Analysis — RTD Measurement Chain
* Precision Measurement System

* Supply
Vpos vcc 0 DC 15
Vneg vee 0 DC -15

* Bridge supply
Vex  vex  0  DC 5

* Bridge: RTD at 25°C = 109.73 Ω
R_RTD  vex   nodeA  109.73    NOISE=1    ; noise enabled
R2     nodeA 0      100        NOISE=1
R3     vex   nodeB  100        NOISE=1
R4     nodeB 0      100        NOISE=1

* INA — simplified as voltage-controlled voltage source with noise
* In LTspice use actual op-amp models for realistic noise simulation

* Stage 1 op-amp A1 (top)
XA1  nodeA  negA1  outA1  vcc  vee  LT1001

* Stage 1 op-amp A2 (bottom)  
XA2  nodeB  negA2  outA2  vcc  vee  LT1001

* Gain resistors (R1 internal = 25k, Rg sets gain)
Ra1  outA1  rg1  25k
Rg   rg1   rg2  5.56k        ; G = 1 + 50k/5.56k = 10
Ra2  rg2   negA2  25k

* Feedback for A1 and A2
; (simplified — use INA128 subcircuit for full accuracy)

* Stage 2 differential
Rb1  outA1  neg3  10k
Rb2  neg3   vout  10k
Rb3  outA2  pos3  10k
Rb4  pos3   0    10k
XA3  pos3  neg3  vout  vcc  vee  LT1001

* Output filter (1 Hz, 1st order)
Rfilt  vout  vfilt  160k
Cfilt  vfilt  0     1u

* Noise analysis
.noise V(vfilt) Vex dec 100 0.01 100000

* Operating point (needed before noise)
.op

.end
```

### Running Noise Analysis in LTspice

1. Set up netlist as above
2. Run `.noise` analysis — this computes noise spectral density V²/Hz at the output
3. In waveform viewer: plot `onoise` (output noise) and `inoise` (referred-to-input noise)
4. Use **CTRL+click** on the waveform to integrate — gives total RMS noise over bandwidth

**Key plots from noise analysis:**
- Output noise spectral density `V_n(f)` in nV/√Hz — should be flat above 1/f corner
- Input-referred noise `V_n,in(f)` = V_n,out / G
- 1/f noise corner frequency (where 1/f and white noise are equal)
- Integrated output noise from 0.01 Hz to 1 Hz (total noise in measurement band)

---

## Expected Noise Spectrum (LTspice Output)

| Frequency | Dominant Noise Source | Expected V_n,out (nV/√Hz) |
|---|---|---|
| 0.01 Hz | 1/f noise of INA | ~200 |
| 0.1 Hz | 1/f noise | ~60 |
| 1 Hz | White noise floor | ~127 |
| 10 Hz | White noise (filter cuts here) | ~127 |
| 100 Hz | Filtered by LP filter | ~1.3 (at -40dB) |
| 1 kHz | Filtered | ~0.013 |

The white noise floor at output: V_n,out ≈ G × e_n = 10 × 10 nV/√Hz = 100–130 nV/√Hz (including bridge resistors).

The 1/f noise dominates below ~10 Hz for most op-amps. For thermal measurement (very low frequency), low 1/f noise op-amps (AD8628, OPA188 — autozero types with 0.1 Hz noise corner) are preferred.

---

## SNR Calculation

**Signal level** at 25°C (bridge balanced → zero output, so evaluate at 1°C change):
```
V_signal = G × S_bridge × 1°C = 10 × 4.81 mV/°C × 1°C = 48.1 mV
```

**Total integrated noise** (1 Hz bandwidth, white noise dominated):
```
V_n,rms = √(S₀ × BW_noise) = 130 nV/√Hz × √1.57 Hz = 163 nV_rms
```

**SNR for 1°C step:**
```
SNR = 20 × log₁₀(48.1 mV / 163 nV) = 20 × log₁₀(295,000) = 109 dB
```

**Minimum detectable temperature change (SNR = 0 dB):**
```
T_min = 163 nV / (48.1 mV/°C) = 3.4 × 10⁻⁶ °C = 3.4 μK
```

In practice, 1/f noise at 0.1 Hz is ~5× higher → T_min,practical ≈ 20 μK.

---

## Effect of Bandwidth on Noise

Reducing the filter cutoff frequency directly reduces integrated noise:

| Filter f_c | Noise BW | V_n,rms | T_min |
|---|---|---|---|
| 10 Hz | 15.7 Hz | 515 nV | 10.7 μK |
| 1 Hz | 1.57 Hz | 163 nV | 3.4 μK |
| 0.1 Hz | 0.157 Hz | 51.5 nV | 1.07 μK |
| 0.01 Hz | 0.0157 Hz | 16.3 nV | 0.34 μK |

Narrowing bandwidth 100× (from 10 Hz to 0.1 Hz) reduces noise 10× (√100). This is the fundamental noise-bandwidth trade-off.

The price: slower response. At f_c = 0.01 Hz, settling time ≈ 5/f_c = 500 seconds.

---

## 1/f Noise Comparison: Standard vs Autozero Op-Amp

| Op-Amp | White Noise (nV/√Hz) | 1/f Corner | Total Noise (0.01–1 Hz) |
|---|---|---|---|
| LT1001 | 10 | ~3 Hz | ~50 nV_rms |
| OPA188 (autozero) | 8.8 | 0.1 Hz | ~12 nV_rms |
| AD8628 (autozero) | 22 | 0.1 Hz | ~32 nV_rms |
| AD8551 (autozero) | 28 | < 0.1 Hz | ~40 nV_rms |

Autozero (chopper-stabilized) amplifiers suppress 1/f noise by modulating the signal to a higher frequency, amplifying it, and demodulating. This makes them ideal for low-frequency precision measurement where 1/f noise would otherwise dominate.

---

## Key Takeaways

1. The INA amplifier noise dominates over RTD Johnson noise by ~8× in this design
2. 1/f noise dominates below 3–10 Hz for standard op-amps
3. Narrowing the measurement bandwidth reduces noise proportionally to √BW
4. Autozero op-amps dramatically reduce low-frequency noise
5. The theoretical noise floor (3–20 μK) is far below any practical calibration or systematic error — thermal noise is not the limiting factor in this system
