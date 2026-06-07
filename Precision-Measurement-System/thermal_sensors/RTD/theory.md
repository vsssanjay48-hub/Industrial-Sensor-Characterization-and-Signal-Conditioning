# RTD — Theory
 
## Introduction
 
A Resistance Temperature Detector (RTD) is a sensor that exploits the predictable, repeatable relationship between the electrical resistance of a metal and its temperature. As temperature increases, metallic resistance increases — a phenomenon rooted in quantum mechanical electron-phonon scattering. RTDs are among the most accurate, stable, and reproducible temperature sensors available in industrial metrology.
 
The most common RTD is the **PT100** — a platinum element with 100 Ω nominal resistance at 0°C. Platinum is used almost universally for industrial RTDs, and understanding *why* reveals the physical and engineering reasoning behind sensor selection.
 
---
 
## Physical Basis: Why Metallic Resistance Increases with Temperature
 
At the atomic level, metals consist of a lattice of positive ions immersed in a "sea" of free electrons (the conduction electrons). When a voltage is applied, electrons drift through the lattice, constituting an electric current.
 
Resistance arises because electrons are scattered as they move through the lattice. The key scattering mechanisms are:
 
**Electron-Phonon Scattering (Dominant at Normal Temperatures)**
 
Phonons are quantized lattice vibrations — they represent the thermal motion of atoms in the crystal. As temperature increases:
- Atoms vibrate with larger amplitudes
- More phonons are excited (higher phonon density)
- The mean free path of electrons between collisions decreases
- Resistance increases
The Bloch-Grüneisen model gives the temperature dependence of resistance at normal temperatures (T >> Debye temperature, typically above ~50–100 K for platinum):
 
```
R(T) ∝ T    [approximately linear for T >> θ_Debye]
```
 
This linear behavior is what makes platinum RTDs so useful — the resistance changes predictably and near-linearly with temperature over a wide range.
 
**Impurity and Defect Scattering (Temperature-Independent)**
 
Even a perfect crystal at absolute zero would have zero resistance from phonon scattering, but real metals contain impurities and crystal defects that scatter electrons regardless of temperature. This gives a residual resistance R₀ at 0 K (the Residual Resistance Ratio, RRR = R(293K)/R(4K), is a measure of metal purity).
 
**Total Resistance (Matthiessen's Rule):**
```
R(T) = R_residual + R_phonon(T)
```
 
For high-purity metals at temperatures above a few hundred K:
```
R(T) ≈ R₀(1 + αT + βT² + ...)
```
 
The higher-order terms (βT², ...) are what make the response slightly non-linear.
 
---
 
## Why Platinum?
 
Platinum is the dominant RTD material for rigorous physical and engineering reasons:
 
**1. Chemical Stability**
Platinum is a noble metal — it resists oxidation, corrosion, and chemical attack up to very high temperatures (stable to above 1000°C in air). Other metals (copper, nickel) oxidize or degrade, causing drift. Platinum remains chemically inert over the full measurement range.
 
**2. Highly Reproducible Resistance-Temperature Relationship**
The R(T) curve of pure platinum is reproducible to within a few millikelvins between different wire samples of the same purity. This means a PT100 calibrated in one laboratory will give nearly the same reading as one calibrated in another. This is why platinum defines the International Temperature Scale (ITS-90) from -259.35°C to +961.78°C.
 
**3. Near-Linear Response**
Platinum exhibits a near-linear R(T) relationship over a wide range, with deviations from linearity well-characterized by the Callendar-Van Dusen (CVD) equation. The non-linearity is small and correctable.
 
**4. High Purity Achievability**
Platinum can be refined to very high purity (99.999%+ is commercially achievable), minimizing lot-to-lot variability and ensuring close conformance to the standard R(T) table.
 
**5. Wide Temperature Range**
PT100 sensors are specified from -200°C to +850°C — a 1050°C span in a single sensor type. Thermocouples cover wider ranges, but RTDs provide better accuracy at lower temperatures.
 
**6. Moderate Sensitivity**
The temperature coefficient of platinum (α ≈ 3.85 × 10⁻³/°C) gives a sensitivity of ~0.385 Ω/°C for a PT100. While this is lower than thermistors, it is highly stable and predictable.
 
---
 
## Callendar-Van Dusen Equation
 
The industry standard mathematical model for platinum RTD resistance as a function of temperature is the **Callendar-Van Dusen (CVD) equation**, defined in IEC 60751.
 
**For temperatures 0°C ≤ T ≤ +850°C:**
```
R(T) = R₀ [1 + A·T + B·T²]
```
 
**For temperatures -200°C ≤ T < 0°C:**
```
R(T) = R₀ [1 + A·T + B·T² + C·(T-100)·T³]
```
 
**Standard coefficients for IEC 60751 Class B platinum (99.99% pure platinum):**
```
A = 3.9083 × 10⁻³  °C⁻¹
B = -5.775 × 10⁻⁷  °C⁻²
C = -4.183 × 10⁻¹²  °C⁻⁴   (only for T < 0)
```
 
These coefficients are derived from the fundamental Debye model of metallic conduction and are universal for high-purity platinum. The small negative value of B accounts for the slight downward curvature of the R-T relationship at higher temperatures.
 
**Computed resistance values (PT100):**
 
| Temperature (°C) | R(T) (Ω) | ΔR from previous |
|---|---|---|
| -200 | 18.52 | — |
| -100 | 60.26 | +41.74 |
| 0 | 100.00 | +39.74 |
| 100 | 138.51 | +38.51 |
| 200 | 175.86 | +37.35 |
| 300 | 212.05 | +36.19 |
| 400 | 247.09 | +35.04 |
| 500 | 280.98 | +33.89 |
| 600 | 313.71 | +32.73 |
| 700 | 345.28 | +31.57 |
| 850 | 390.48 | +45.20 |
 
The decreasing ΔR with increasing temperature clearly shows the slight non-linearity — sensitivity decreases at higher temperatures. This is captured by the B coefficient in the CVD equation.
 
---
 
## PT100 vs PT1000
 
Both use platinum with the same R/R₀ ratio at every temperature. The difference is the nominal resistance at 0°C:
 
| Type | R₀ | Sensitivity | Advantage |
|---|---|---|---|
| PT100 | 100 Ω | 0.385 Ω/°C | Industry standard, wide availability |
| PT1000 | 1000 Ω | 3.850 Ω/°C | 10× higher output, less affected by lead resistance |
 
PT1000 is preferred when:
- Lead wire resistance is significant (higher R₀ means lead resistance is a smaller fraction)
- Higher signal level is needed (the bridge output is 10× larger for the same bridge ratio)
- Lower excitation current is needed to limit self-heating (for the same power dissipation, a PT1000 needs only 1/√10 the current of a PT100 for the same thermal noise level)
---
 
## IEC 60751 Accuracy Classes
 
IEC 60751 defines tolerance classes for PT100 RTDs:
 
| Class | Tolerance (°C) | Formula |
|---|---|---|
| AA | ±(0.1 + 0.0017|T|) | ±0.1°C at 0°C, ±0.27°C at 100°C |
| A | ±(0.15 + 0.002|T|) | ±0.15°C at 0°C, ±0.35°C at 100°C |
| B | ±(0.3 + 0.005|T|) | ±0.3°C at 0°C, ±0.8°C at 100°C |
| C | ±(0.6 + 0.01|T|) | ±0.6°C at 0°C, ±1.6°C at 100°C |
 
Class AA is used for laboratory instruments, primary calibration, and pharmaceutical monitoring.
Class B is the most common industrial grade.
Class C is used for non-critical industrial applications.
 
---
 
## RTD Construction Types
 
**Wire-Wound RTD:**
- Fine platinum wire (0.05–0.1 mm diameter) wound on a ceramic or glass mandrel
- Most stable and accurate type (reference-grade instruments)
- Fragile — susceptible to vibration damage
- Large thermal mass → slower response
**Thin-Film RTD:**
- Platinum deposited as a thin film on a ceramic substrate
- More robust than wire-wound, suitable for vibration
- Lower cost, faster production
- Slightly less stable than wire-wound
- Faster response time (less thermal mass)
- Most common type in industrial applications
**Coiled Element RTD:**
- Loose coil of platinum wire inside a ceramic tube
- Allows thermal expansion without mechanical stress on the element
- Used in high-precision laboratory standards
---
 
## Connection Methods
 
The choice of connection method determines how much lead wire resistance corrupts the measurement. See `limitations.md` for full quantitative analysis.
 
**2-Wire:** Simple but includes lead resistance. Acceptable only for short leads or rough accuracy.
 
**3-Wire:** Compensates for lead resistance assuming lead resistances are equal. Standard industrial method.
 
**4-Wire (Kelvin):** Completely eliminates lead resistance error. Gold standard for precision measurement. Two wires carry current; two separate wires measure voltage.
 
---
 
## Conclusion
 
The PT100 RTD stands out among temperature sensors for the rigor of its physical model, the purity and stability of its platinum element, and the international standardization that makes sensors interchangeable. Its slight non-linearity is completely characterized by the Callendar-Van Dusen equation and correctable in software. Its main limitations — self-heating, lead resistance, and slower response compared to thermocouples — are well-understood and have established engineering solutions.
 
