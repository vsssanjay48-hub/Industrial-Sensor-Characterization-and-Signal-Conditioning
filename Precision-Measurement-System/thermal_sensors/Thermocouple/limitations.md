# Thermocouple Limitations

## 1. Cold Junction Compensation Error
Largest practical error source. CJC sensor accuracy ±0.5–2°C becomes system error on every channel. For < ±0.5°C: use calibrated RTD as CJC sensor and isothermal reference block.

## 2. Very Low Output Voltage
Type K: 41 μV/°C. At 100°C above reference: only 4.1 mV. Requires G = 100–500 amplifier. Long cable runs in industrial environments pick up 50 Hz hum that can exceed signal amplitude. Mitigation: shielded twisted pair, high CMRR amplifier, low-pass filter.

## 3. Drift and Contamination
- Grain growth above 700°C: Type K drifts 2–4°C per 100 operating hours above 1000°C
- Elemental migration along wire: changing temperature profile causes reading change even if hot junction T is constant
- "Green rot" in Type K: selective oxidation of Chromel Cr above 900°C in reducing atmosphere — rapid drift
- Fix: select type matched to environment, protective sheath, recalibration schedule

## 4. Non-Linearity
Seebeck coefficient S_AB(T) varies with temperature. Type K varies from 25 μV/°C at −200°C to 43 μV/°C at 500°C. Must use NIST polynomial — treating as linear causes several percent error.

## 5. Parasitic Thermoelectric EMFs
Every dissimilar metal junction in the circuit contributes EMF. Terminal blocks, connectors, and PCB traces must all be at the same temperature as the CJC sensor. Temperature gradients across terminal blocks cause systematic offset errors (±0.2–1°C).

## Summary
| Limitation | Typical Error | Mitigation |
|---|---|---|
| CJC error | ±1–2°C | Precision CJC sensor, isothermal block |
| EMI on long cables | ±0.5–5°C | Shielded twisted pair, LPF |
| High-temp drift | 1–5°C/year | Recalibration, type matching, sheath |
| Non-linearity | Up to 10% | NIST polynomial in firmware |
| Parasitic EMFs | ±0.2–1°C | Isothermal terminal block |
