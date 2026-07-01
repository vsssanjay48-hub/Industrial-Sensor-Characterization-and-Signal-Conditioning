# Industrial-Sensor-Characterization-and-Signal-Conditioning
To study industrial sensors from physical principle to signal conditioning and practical limitations.
# Precision Measurement System

A depth-first study of industrial thermal sensing and signal conditioning — from sensor physics to calibrated measurement.

---

## What This Project Covers

**Sensors:** PT100 RTD · NTC Thermistor · Type K Thermocouple

**Signal Chain:**
```
Sensor → Wheatstone Bridge → Instrumentation Amplifier → Low-Pass Filter → ADC
```

**Topics:**
- Callendar-Van Dusen equation, Steinhart-Hart model, Seebeck effect
- Error propagation, self-heating, lead resistance, noise analysis
- Wheatstone bridge sensitivity and non-linearity
- 3 op-amp INA topology and CMRR analysis
- Multi-point calibration and polynomial correction
- Long-term drift mechanisms and recalibration intervals

---

## Repository Structure

```
├── docs/                  ← Measurement theory, error analysis, signal conditioning, thermal modeling
├── thermal_sensors/
│   ├── RTD/               ← Theory, equations, limitations, applications
│   ├── Thermistor/        ← Theory, equations, limitations, applications
│   └── Thermocouple/      ← Theory, equations, limitations, applications
├── simulations/           ← LTspice guides: bridge, diff-amp, INA, filter, noise
├── characterization/      ← Sensitivity, linearity, calibration, drift analysis
├── plots/                 ← Python scripts (numpy + matplotlib)
├── report/                ← Full project report
└── references/            ← Standards, textbooks, datasheets
```

---

## Key Results

| Stage | Result |
|---|---|
| Bridge sensitivity | 4.81 mV/°C (PT100, V_ex = 5V) |
| INA CMRR (G=10) | ~86 dB |
| Filter 50 Hz rejection | −68 dB |
| 16-bit ADC resolution | 1.58 mK/LSB |
| Total error (4-wire, calibrated) | ±0.07°C |
| Noise floor (1 Hz BW) | 0.37 μK |

---

## Tools

`LTspice` · `Python` · `numpy` · `matplotlib` · `Git`

---

## Status

- [x] Theory documentation — all three sensors
- [x] Signal conditioning analysis
- [x] LTspice simulation guides
- [x] Python characterization scripts
- [x] Full project report
- [ ] Hardware prototype
- [ ] Experimental validation
