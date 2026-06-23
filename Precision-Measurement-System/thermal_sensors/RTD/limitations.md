# RTD Limitations

## 1. Self-Heating
P_self = I²R raises sensor temperature above ambient. At 1 mA: +0.02°C (acceptable). At 5 mA: +0.5°C (significant). Scales as I² — double current = 4× error. Fix: reduce I, use PT1000, pulse excitation, or apply correction.

## 2. Lead Wire Resistance
2-wire: lead R adds directly to reading. 10m of 0.5mm² cable introduces ~0.9°C error. Error also drifts with ambient temperature (copper TCR = 3.93×10⁻³/°C). Fix: 3-wire (industrial), 4-wire (precision).

## 3. Slow Response
Wire-wound RTDs in SS sheaths: τ = 30–60 s in still air, 3–10 s in flowing water. Cannot track rapid temperature changes. Fix: thin-film element, smaller sheath, higher fluid velocity.

## 4. Non-Linearity
CVD B coefficient causes ~0.37% non-linearity over 0–100°C (0.37°C error), growing to >6% over the full range. Fix: CVD inverse equation in firmware.

## 5. Cost
Platinum is a precious metal. Class B PT100: $5–$20. Class A: $20–$60. Class AA: $50–$200. Justified for stable long-term precision.

## 6. Vibration Sensitivity
Wire-wound elements can fatigue and break under vibration. Fix: use thin-film RTDs with vibration rating.
