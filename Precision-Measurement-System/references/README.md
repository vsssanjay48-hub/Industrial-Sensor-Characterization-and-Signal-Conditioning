# References

## Standards

| Standard | Title | Relevance |
|---|---|---|
| IEC 60751:2022 | Industrial platinum resistance thermometers and platinum temperature sensors | Defines PT100/PT1000 R(T) table, CVD coefficients, tolerance classes AA/A/B/C |
| IEC 60584-1:2013 | Thermocouples — Part 1: EMF specifications and tolerances | Defines thermocouple type specifications, reference tables, tolerances |
| IEC 60584-2:2021 | Thermocouples — Part 2: Tolerances | Type-by-type tolerance specifications |
| NIST Monograph 175 | Temperature-Electromotive Force Reference Functions and Tables | NIST thermocouple polynomial coefficients, all types |
| ITS-90 | International Temperature Scale of 1990 | Defines thermodynamic temperature scale from 0.65 K to highest practical temperature |
| ASTM E1137 | Standard Specification for Industrial Platinum Resistance Thermometers | US standard for industrial RTDs |

---

## Textbooks

**Measurement and Instrumentation**

- Doebelin, E.O. *Measurement Systems: Application and Design*, 5th ed. McGraw-Hill, 2004.
  - Chapters 3–4: Static and dynamic characteristics of measurement systems.

- Fraden, J. *Handbook of Modern Sensors: Physics, Designs, and Applications*, 5th ed. Springer, 2016.
  - Comprehensive reference for all sensor types including thermal sensors.

- Bentley, J.P. *Principles of Measurement Systems*, 4th ed. Pearson Prentice Hall, 2005.
  - Excellent treatment of Wheatstone bridges and signal conditioning.

**Electronics and Signal Conditioning**

- Horowitz, P. and Hill, W. *The Art of Electronics*, 3rd ed. Cambridge University Press, 2015.
  - Chapter 8: Low-noise techniques. Chapter 15: Measurement and control.

- Franco, S. *Design with Operational Amplifiers and Analog Integrated Circuits*, 4th ed. McGraw-Hill, 2015.
  - Chapters 1–2: Op-amp fundamentals. Chapter 8: Sensor amplifiers.

- Kitchin, C. and Counts, L. *A Designer's Guide to Instrumentation Amplifiers*, 3rd ed. Analog Devices, 2006.
  - Free PDF from Analog Devices. Essential reference for INA design.

**Precision Measurement**

- Morris, A.S. *Measurement and Instrumentation Principles*, 3rd ed. Butterworth-Heinemann, 2001.
  - Good treatment of error analysis and calibration.

- Nicholas, J.V. and White, D.R. *Traceable Temperatures: An Introduction to Temperature Measurement and Calibration*, 2nd ed. Wiley, 2001.
  - Authoritative text on thermometry and calibration uncertainty.

---

## Application Notes and Technical Documents

**RTD and Thermistor**

- Omega Engineering. *The Temperature Handbook*, Vol. 29.
  - Available free from omega.com. Comprehensive sensor reference.

- Texas Instruments. *RTD Measurement With a High-Resolution Delta-Sigma ADC* (SBAA275, 2018).
  - Practical circuit design for 4-wire RTD with ADS1220.

- Analog Devices. *Precision Temperature Sensing with RTD Circuits* (AN-709, Rev. B).
  - Op-amp and INA configurations for RTD measurement.

- Vishay Intertechnology. *NTC Thermistors: Accuracy and Interchangeability* (Application Note).
  - Steinhart-Hart equation, tolerance analysis, interchangeability.

**Thermocouple**

- National Instruments. *Measuring Temperature with Thermocouples*.
  - Practical CJC implementation and noise considerations.

- Analog Devices. *MAX31856 Datasheet*. 2019.
  - SPI thermocouple-to-digital converter with built-in CJC and polynomial linearization.

- Maxim Integrated. *Thermocouple Amplification and Cold-Junction Compensation* (AN-3654).
  - Detailed treatment of CJC error sources.

**Signal Conditioning**

- Analog Devices. *MT-087 Tutorial: Voltage-to-Current Signal Conversion* (2009).

- Texas Instruments. *Op Amp Noise Theory and Applications* (SLOA082, 2007).
  - Johnson noise, 1/f noise, noise bandwidth, design for low noise.

- Analog Devices. *MT-049 Tutorial: Op Amp Total Output Noise Calculations for Single-Pole System* (2009).

**Wheatstone Bridge**

- Analog Devices. *Analog Dialogue 34-3: Precision Strain Gauge Measurement Using the AD7730 ADC* (2000).
  - Bridge balancing, ratiometric measurement, drift analysis.

- Texas Instruments. *Precision Measurement Using Bridge Sensors* (SBAA197, 2013).

**Calibration and Error Analysis**

- BIPM/ISO/OIML/ILAC. *Guide to the Expression of Uncertainty in Measurement (GUM)*, 2008.
  - The definitive international standard for measurement uncertainty calculation.
  - Available free: https://www.bipm.org/utils/common/documents/jcgm/JCGM_100_2008_E.pdf

- NIST Technical Note 1297: *Guidelines for Evaluating and Expressing the Uncertainty of NIST Measurement Results* (1994).
  - US implementation of GUM methodology.

---

## Datasheets

| Device | Manufacturer | Relevance |
|---|---|---|
| PT100 (IEC Class B) | Heraeus, Vishay, TE Connectivity | Standard RTD element |
| INA128 | Texas Instruments | Precision instrumentation amplifier |
| LT1001 | Linear Technology / Analog Devices | Low-noise, low-offset op-amp |
| OPA188 | Texas Instruments | Zero-drift (autozero) op-amp, ultra-low 1/f |
| AD8628 | Analog Devices | Auto-zero op-amp for precision DC measurement |
| LT1460 | Analog Devices | Micropower precision voltage reference (20 ppm/°C) |
| ADR4525 | Analog Devices | 2.5V precision reference (2 ppm/°C B-grade) |
| MAX31856 | Maxim Integrated | Multi-type thermocouple-to-digital converter |
| ADS1220 | Texas Instruments | 24-bit ADC with PGA, for RTD and bridge sensors |
| LTC2986 | Analog Devices | Multi-sensor temperature measurement IC |

---

## Online Resources

| Resource | URL | Notes |
|---|---|---|
| NIST Thermocouple Tables | https://srdata.nist.gov/its90/main/ | Official polynomial coefficients for all types |
| Omega Engineering Handbook | https://www.omega.com/en-us/resources/ | Free sensor reference library |
| Analog Devices University | https://university.analog.com | Free circuit and sensor tutorials |
| LTspice Resources | https://www.analog.com/en/design-center/design-tools-and-calculators/ltspice-simulator.html | Simulator download, model libraries |
| PyPI: numpy, scipy, matplotlib | https://pypi.org | Python libraries used in this project |

---

## LTspice Model Sources

- **LT1001, LT1460:** Included in LTspice standard library (Analog Devices / Linear Technology)
- **INA128:** Download from Texas Instruments (ti.com/product/INA128 → Design resources)
- **Generic instrumentation amplifier:** Use the LTspice INA model or build three-op-amp subcircuit manually

---

*References last reviewed: 2024. Standards and application notes should be verified for the latest revision before use in design.*
