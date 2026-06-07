# Thermocouple — Theory
 
## Introduction
 
A thermocouple is the most widely used temperature sensor in industry — not because it is the most accurate or stable, but because it is simple, rugged, inexpensive, and capable of measuring temperatures that would destroy any other sensor. Industrial furnaces, jet engines, gas turbines, molten metal, and rocket nozzles are measured exclusively with thermocouples.
 
A thermocouple consists of two wires of dissimilar metals joined at one end (the **hot junction** or **measuring junction**). When this junction is placed at a temperature different from the other end (the **cold junction** or **reference junction**), a small EMF (electromotive force) is generated. This voltage is the thermocouple's output signal.
 
---
 
## The Seebeck Effect
 
The Seebeck effect was discovered by Thomas Johann Seebeck in 1821. It is one of three related thermoelectric phenomena (the others being the Peltier effect and the Thomson effect).
 
### Physical Origin
 
In a metal, conduction electrons have a distribution of kinetic energies described by Fermi-Dirac statistics. When a temperature gradient exists along a conductor, electrons at the hot end have higher average kinetic energy than at the cold end. This causes them to diffuse toward the cold end — creating a charge buildup and therefore an electric field opposing further diffusion.
 
The steady-state condition is a balance between thermal diffusion and the opposing electric field. This creates an electric potential difference (voltage) along the conductor.
 
**Seebeck coefficient (thermopower) S_A of a material:**
```
S_A = dV_A / dT    [V/K or more practically μV/°C]
```
 
Different metals have different thermopower values because:
- Different electron densities
- Different Fermi energies
- Different phonon-drag contributions at lower temperatures
The Seebeck coefficient can be positive (S > 0: electrons diffuse toward cold end, conventional current flows toward hot end in external circuit) or negative (S < 0: electrons diffuse toward hot end).
 
**Seebeck coefficients of common thermocouple materials at 25°C:**
| Material | S (μV/°C) |
|---|---|
| Chromel (Ni-10%Cr) | +25 |
| Alumel (Ni-2%Al-2%Mn-1%Si) | -16 |
| Platinum (pure) | -5 |
| Platinum-10%Rhodium | +1 |
| Copper | +6.5 |
| Constantan (Cu-40%Ni) | -38 |
| Iron | +19 |
 
### The Seebeck EMF in a Thermocouple Circuit
 
When two materials A and B are joined, the net EMF in the circuit depends on the *difference* in their Seebeck coefficients:
 
**Seebeck coefficient of the thermocouple:**
```
S_AB = S_A - S_B    [μV/°C]
```
 
**Voltage generated (for small temperature range where S_AB is approximately constant):**
```
V = S_AB × (T_hot - T_cold)
```
 
More precisely, for temperature-dependent S_AB:
```
V = ∫[T_cold to T_hot] S_AB(T) dT
```
 
This integral is what thermocouple reference tables (NIST or IEC 60584) tabulate.
 
### The Law of Intermediate Materials
 
A critical practical theorem: **the introduction of any third material into a thermocouple circuit does not affect the measured EMF, provided both new junctions are at the same temperature.**
 
Consequence: Extension wires, terminals, connectors, and the meter itself do not affect the reading, as long as all non-thermocouple junctions are at the same (reference junction) temperature. This allows long runs of ordinary copper cable with only the thermocouple wire in the hot zone.
 
However, any junction at a *different* temperature contributes an additional EMF — this is the basis of the cold junction error.
 
---
 
## Cold Junction Compensation (CJC)
 
### The Problem
 
The standard NIST/IEC thermocouple tables assume the reference junction is at exactly **0°C** (ice point). In practice, the reference junction is at ambient temperature (typically 15–35°C, not 0°C). If we ignore this, we measure:
 
```
V_measured = S_AB × (T_hot - T_ambient)
```
 
But we want:
```
V_true = S_AB × (T_hot - 0°C) = S_AB × T_hot
```
 
The error (for a Type K thermocouple at T_ambient = 25°C):
```
ΔV = S_K × (0 - 25) = 41 μV/°C × (-25) = -1025 μV
```
 
Temperature error from not compensating: 1025 μV / 41 μV/°C = **25°C** — equal to the ambient offset. Clearly catastrophic.
 
### Compensation Methods
 
**Ice bath:** Maintain the reference junction in an ice-water mixture (0°C). Used in laboratory calibration. Impractical for industrial continuous operation.
 
**Electronic CJC:**
1. Measure the ambient temperature at the reference junction using a separate sensor (typically an NTC thermistor, RTD, or semiconductor temperature sensor)
2. Convert this ambient temperature to an equivalent thermocouple voltage using the reference tables
3. Add this compensation voltage to the measured thermocouple voltage
```
V_corrected = V_measured + V_CJC(T_ambient)
```
 
Where V_CJC(T_ambient) is the voltage the thermocouple would produce with hot junction at T_ambient and reference at 0°C.
 
```
T_hot = NIST_inverse(V_corrected)
```
 
CJC accuracy depends on the accuracy of the reference temperature sensor. Most industrial thermocouple transmitters achieve ±0.5–1°C CJC accuracy. Precision CJC ICs (like MAX31856 or AD8495) achieve ±0.5°C.
 
**Isothermal block:** All reference junctions are brought to a common isothermal block whose temperature is measured by one precision sensor. Used in multi-channel measurement systems.
 
---
 
## Thermocouple Types
 
IEC 60584 defines standard thermocouple types, each with a specific material pair, designated by a letter:
 
| Type | Materials | Range (°C) | Sensitivity | Characteristics |
|---|---|---|---|---|
| K | Chromel / Alumel | -200 to +1260 | ~41 μV/°C | Most common, general purpose |
| J | Iron / Constantan | -40 to +750 | ~52 μV/°C | High sensitivity, lower range |
| T | Copper / Constantan | -200 to +350 | ~43 μV/°C | Excellent at low temp, food industry |
| E | Chromel / Constantan | -200 to +900 | ~68 μV/°C | Highest sensitivity, nonmagnetic |
| N | Nicrosil / Nisil | -200 to +1300 | ~36 μV/°C | Improved stability vs K |
| R | Pt-13%Rh / Pt | 0 to +1480 | ~10 μV/°C | High temp, laboratory calibration |
| S | Pt-10%Rh / Pt | 0 to +1480 | ~10 μV/°C | High temp, very stable |
| B | Pt-30%Rh / Pt-6%Rh | +200 to +1820 | ~6 μV/°C | Highest temperature range |
 
**Type K** is by far the most widely used in industry due to its good combination of range, sensitivity, cost, and chemical resistance.
 
### Type K Non-Idealities
 
Type K has a known non-linearity in the 200–350°C range related to magnetic ordering transitions in the Alumel alloy. This creates a hysteresis effect (different readings on heating vs cooling). Above 400°C, this effect largely disappears.
 
---
 
## Seebeck Voltage Reference Tables
 
The NIST/IEC thermocouple tables give EMF in mV as a function of temperature with reference at 0°C. An excerpt for **Type K:**
 
| T (°C) | EMF (mV) | Sensitivity (μV/°C) |
|---|---|---|
| -200 | -5.891 | 25.3 |
| -100 | -3.554 | 38.0 |
| 0 | 0.000 | 39.4 |
| 100 | 4.096 | 41.3 |
| 200 | 8.138 | 40.3 |
| 300 | 12.209 | 41.0 |
| 500 | 20.644 | 43.1 |
| 800 | 33.275 | 41.2 |
| 1000 | 41.276 | 38.3 |
| 1200 | 48.838 | 37.3 |
| 1260 | 51.000 | ~37 |
 
The sensitivity varies from ~25 μV/°C at -200°C to a peak of ~45 μV/°C around 500°C, then decreasing. This non-linearity is accounted for in the polynomial approximations below.
 
---
 
## Polynomial Approximation
 
For computation in firmware, the IEC 60584 reference function is approximated by polynomial:
 
**Type K, 0 to 1372°C:**
```
E(T) = Σ cₙ × Tⁿ    [n = 0 to 10]
```
 
Key coefficients (IEC 60584-1, abbreviated):
```
c₀ = 0.000000000000 mV
c₁ = 3.9450128025×10⁻² mV/°C
c₂ = 2.3622373598×10⁻⁵ mV/°C²
c₃ = -3.2858906784×10⁻⁷ mV/°C³
... (10 terms total)
```
 
Plus an exponential correction term for Type K between 0 and 1372°C to account for the Alumel magnetic transition.
 
**Inverse function (T from measured mV):** Separate polynomial coefficients for different voltage ranges. From 0 to 20.644 mV (0 to 500°C), a 9th-order polynomial achieves < 0.05°C accuracy.
 
---
 
## Signal Conditioning Requirements
 
Thermocouples produce very low voltages. A Type K thermocouple at 100°C above the reference junction produces only:
```
V = 4.096 mV
```
 
This requires:
- High-gain, low-noise amplification (gain 100–500 to bring to ADC full-scale)
- Cold junction compensation circuitry or IC
- Good common-mode rejection (thermocouple may float at high potential relative to ground)
- EMI filtering (the long wire runs typical of thermocouple installations act as antennas)
- Input protection (thermocouples often used in electrically harsh environments)
These requirements make thermocouple amplifiers a specialized design. Dedicated ICs (AD8495, AD8495, MAX31855, MAX31856, LTC2986) handle all of this in one package.
 
---
 
## Conclusion
 
The thermocouple's operating principle — the Seebeck effect — is elegant and physically robust. The sensor itself is just two wires joined at a point, requiring no electronics at the hot junction. This is why thermocouples remain the workhorse of high-temperature industrial measurement: nothing else is as simple, rugged, and capable of surviving the environments where thermocouples are deployed. Understanding the Seebeck effect, cold junction compensation, and the non-linearity of the output is essential for implementing a thermocouple measurement system correctly.
