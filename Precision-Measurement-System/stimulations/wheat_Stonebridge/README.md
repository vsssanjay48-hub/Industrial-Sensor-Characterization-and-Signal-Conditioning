# Simulation: Wheatstone Bridge
 
## Objective
 
Simulate a quarter-bridge Wheatstone bridge with a PT100 RTD as the active element. Verify bridge sensitivity, analyze non-linearity, and measure differential output voltage as a function of temperature.
 
---
 
## Circuit Description
 
```
        V_ex = 5V DC
            │
    ┌───────┴───────┐
    │               │
  R_RTD(T)        R3 = 100 Ω
    │               │
    A               B       ← Differential output: V_out = V_A - V_B
    │               │
  R2 = 100 Ω      R4 = 100 Ω
    │               │
    └───────┬───────┘
           GND
```
 
**Component values:**
| Component | Value | Notes |
|---|---|---|
| V_ex | 5 VDC | Stable supply (use ideal voltage source) |
| R_RTD | Variable (100 Ω at 0°C) | Models PT100 element |
| R2, R3, R4 | 100 Ω each | Fixed resistors (1% tolerance) |
| V_out | V_A - V_B | Measured differentially |
 
---
 
## LTspice Setup
 
### Schematic
 
1. Place a DC voltage source `V1 = 5` between Vex and GND.
2. Place four resistors in bridge configuration.
3. For R_RTD, use a `PARAM` statement to sweep its value:
   - At 0°C: R_RTD = 100.00 Ω
   - At 50°C: R_RTD = 119.40 Ω
   - At 100°C: R_RTD = 138.51 Ω
   - At 200°C: R_RTD = 175.86 Ω
### DC Sweep Simulation
 
Use `.dc param R_RTD 80 180 1` to sweep R_RTD from 80 to 180 Ω (corresponding to roughly -52°C to +207°C).
 
Place voltage probes at nodes A and B. Measure V(A) - V(B).
 
### SPICE Netlist
 
```spice
* Wheatstone Bridge - Quarter Bridge (PT100 RTD)
* Precision Measurement System
 
Vex  vex  0  DC 5
 
R_RTD  vex  nodeA  {R_val}
R2     nodeA  0    100
R3     vex  nodeB  100
R4     nodeB  0    100
 
.param R_val = 100
 
* DC operating point
.op
 
* Sweep R_val (simulates temperature sweep)
.step param R_val list 100 103.85 107.70 111.55 115.40 119.40 123.24 127.08 130.90 134.71 138.51
 
* Measures
.meas op VOUT find V(nodeA,nodeB)
 
.end
```
 
---
 
## Expected Results
 
### Bridge Output vs Temperature
 
| T (°C) | R_RTD (Ω) | V_A (V) | V_B (V) | V_out (mV) | Predicted V_out (mV) |
|---|---|---|---|---|---|
| 0 | 100.00 | 2.500 | 2.500 | 0.000 | 0.000 |
| 10 | 103.85 | 2.548 | 2.500 | 47.6 | 48.1 |
| 25 | 109.63 | 2.613 | 2.500 | 112.6 | 120.3 |
| 50 | 119.40 | 2.716 | 2.500 | 215.7 | 240.6 |
| 100 | 138.51 | 2.874 | 2.500 | 373.7 | 481.3 |
 
*Note: Values from exact formula. Predicted column uses linear approximation V_ex×α×ΔT/4.*
 
The discrepancy at 100°C (373.7 vs 481.3 mV) reveals the **bridge non-linearity** — the linearized formula over-estimates the output.
 
### Exact Bridge Formula
 
```
V_out = V_ex × δR / (4R₀ + 2δR)
```
 
At T = 100°C, δR = 38.51 Ω:
```
V_out = 5 × 38.51 / (400 + 77.02) = 192.55 / 477.02 = 403.6 mV
```
 
Linearized: 5 × 38.51 / 400 = 481.4 mV → 19% overestimate. This non-linearity is visible in simulation.
 
---
 
## Analysis Tasks
 
### Task 1: Verify Sensitivity
 
From simulation results, compute the slope dV_out/dT near T = 0°C and T = 100°C.
 
Compare to theoretical: dV_out/dT = V_ex × α/4 = 5 × 3.85×10⁻³/4 = 4.81 mV/°C near 0°C.
 
### Task 2: Quantify Non-Linearity
 
Plot V_out vs T. Fit a best-fit straight line to the data. Calculate the maximum deviation from the line as a percentage of full-scale output (at T = 100°C).
 
### Task 3: Effect of Excitation Voltage
 
Repeat the simulation with V_ex = 3.3V and V_ex = 10V. Observe how the output scales.
 
Confirm: sensitivity is proportional to V_ex (higher V_ex → more bridge output, but also more self-heating).
 
### Task 4: Tolerance Sensitivity
 
Change R3 from 100 Ω to 101 Ω (1% tolerance error). Measure the output at T = 0°C.
 
Expected: The bridge no longer nulls at 0°C. The offset equals approximately V_ex × ΔR/(4R₀) = 5 × 1/(400) = 12.5 mV → equivalent to 12.5/4.81 = 2.6°C systematic offset error.
 
This demonstrates why precision resistors (0.1% or better) are needed in the fixed bridge arms.
 
---
 
## Plots to Generate
 
1. **V_out vs R_RTD** (linear x-axis in Ω, left y-axis in mV)
2. **V_out vs Temperature** (x-axis in °C, from -50 to +200°C)
3. **Non-linearity error** = V_out,actual - V_out,linear vs Temperature
4. **Sensitivity dV/dT vs Temperature** (shows how sensitivity decreases at higher T)
Generate plots 2–4 in Python using `plots/rtd_bridge_analysis.py` (see plots folder).
 
---
 
## Notes
 
- The bridge is most linear when δR << R₀. For the PT100 from 0 to 100°C, δR_max/R₀ = 38.51/100 = 38.5%, making non-linearity significant.
- For precision systems, always use the full exact formula (or the inverse CVD equation) rather than the linearized bridge formula.
- The simulation assumes ideal resistors (no temperature coefficient). Real resistors have TCR of 25–100 ppm/°C; this adds a small temperature-dependent offset.
