# Measurement Theory

## Introduction

A measurement system is any device or chain of devices that converts a physical quantity of interest into a form that can be read, recorded, or processed. In industrial instrumentation, the output is almost always an electrical signal — a voltage, current, resistance, or frequency that encodes the value of the physical variable.

The quality of a measurement system is not defined by a single number. It is described by a set of characteristics — some static, some dynamic — that together tell you how faithfully the system represents the physical quantity across all operating conditions.

Understanding these characteristics mathematically is the foundation for everything else in this project.

---

## The Generalized Measurement System

A measurement system can be modeled as a chain of functional blocks:

```
Physical Input → Sensor / Transducer → Signal Conditioner → Output Stage → Display / ADC
```

Each block has a transfer characteristic — a mathematical relationship between its input and output.

For a sensor:

```
q_out = f(q_in)
```

Where `q_in` is the physical quantity (e.g., temperature in °C) and `q_out` is the electrical output (e.g., resistance in Ω or voltage in mV).

The ideal transfer characteristic is a perfectly linear, time-invariant function. Real sensors deviate from this ideal in ways that are described by the static and dynamic characteristics.

---

## Static Characteristics

Static characteristics describe the sensor's behavior when the input is held constant, or changes so slowly that time-dependent effects are negligible. These are the "DC" properties of the measurement system.

### 1. Accuracy

Accuracy is the closeness of a measurement to the true value of the physical quantity.

It is expressed as:
- An absolute value (e.g., ±0.5°C)
- A percentage of full-scale (e.g., ±0.1% FS)
- A percentage of reading (e.g., ±0.5% of reading)

Accuracy encompasses all sources of error — systematic and random — in a single specification. A sensor manufacturer specifying "accuracy ±1°C" is telling you that, after calibration, the reading will be within ±1°C of the true temperature under specified conditions.

**Important:** Accuracy is not the same as resolution. A sensor can have very high resolution (tiny steps between readings) and still be inaccurate if there is a large systematic offset.

### 2. Precision (Repeatability)

Precision is the ability of a sensor to give the same output reading each time the same input is applied, under the same conditions.

A precise but inaccurate sensor produces readings that are tightly clustered together but consistently away from the true value — this is the hallmark of systematic error.

Statistical measure of precision:

```
σ = standard deviation of repeated measurements
```

A 3σ precision specification means 99.7% of readings fall within ±3σ of the mean.

### 3. Sensitivity

Sensitivity is the ratio of the change in output to the change in input:

```
S = dq_out / dq_in
```

For a linear sensor:

```
S = (q_out,2 - q_out,1) / (q_in,2 - q_in,1)    [constant]
```

For a non-linear sensor, sensitivity is the local slope of the transfer curve at a given operating point:

```
S(T) = dR/dT    (for a resistance sensor)
```

Units of sensitivity depend on the sensor type:
- RTD: Ω/°C (typically 0.385 Ω/°C for PT100)
- Thermistor: Ω/°C (much larger, e.g., -100 Ω/°C near 25°C — note negative sign for NTC)
- Thermocouple: μV/°C (called the Seebeck coefficient, e.g., ~41 μV/°C for Type K)

Higher sensitivity is generally desirable — it means the sensor produces a larger output signal per unit change in the physical quantity, improving resolution and signal-to-noise ratio.

### 4. Resolution

Resolution is the smallest change in input that produces a detectable change in output.

In analog systems, resolution is limited by:
- Electrical noise floor (noise sets the minimum detectable signal)
- Quantization in ADCs (1 LSB = full-scale / 2^N for an N-bit converter)
- Mechanical or physical hysteresis

For an ADC with N-bit resolution and full-scale range FS:

```
Resolution = FS / 2^N
```

A 16-bit ADC measuring a 0–100°C range:

```
Resolution = 100°C / 65536 ≈ 0.0015°C per LSB
```

This theoretical resolution can only be achieved if the analog noise entering the ADC is less than 0.5 LSB. If the noise is larger, effective resolution (ENoBits) is reduced.

### 5. Linearity

An ideal sensor has a perfectly linear transfer characteristic. Linearity error is the maximum deviation of the actual transfer curve from the best-fit straight line, expressed as a percentage of full-scale:

```
Linearity error = (Maximum deviation / Full-scale range) × 100%
```

Types of linearity error specification:
- **Independent linearity (best-fit straight line):** The reference line is chosen to minimize the maximum deviation — gives the best-case number
- **Terminal linearity (end-point linearity):** The reference line passes through the endpoints of the range — more conservative and reproducible
- **Zero-based linearity:** Reference line passes through zero and the full-scale endpoint

For RTDs, linearity is very good (deviation < 0.5% over -200 to +850°C using the Callendar-Van Dusen equation). Thermistors are highly non-linear (deviation > 10% if treated as linear).

### 6. Hysteresis

Hysteresis is the difference in output for the same input value when approached from two different directions (increasing vs decreasing input).

```
Hysteresis error = |Output(increasing) - Output(decreasing)|
```

Hysteresis is caused by:
- Mechanical strain in sensor elements
- Thermal gradients in the sensor body
- Magnetic domain effects in core materials

For precision thermal sensors, hysteresis is typically small (<0.1°C for good RTDs) but must be characterized for high-precision applications.

### 7. Drift

Drift is a slow, continuous change in sensor output that occurs even when the input is held perfectly constant. It represents a time-dependent change in the sensor's characteristics.

Types of drift:
- **Zero drift (offset drift):** The output at zero input changes over time. Expressed in μV/°C or mV/hour.
- **Sensitivity drift (span drift):** The slope of the transfer curve changes. Expressed as % of reading per °C.
- **Long-term drift (aging):** Slow changes due to material aging, contamination, or structural relaxation. Expressed as ppm/year or °C/year.

Causes of drift:
- Temperature changes in the conditioning electronics
- Mechanical stress relaxation in the sensor element
- Chemical contamination or oxidation
- Component aging in amplifier circuits

### 8. Span and Range

- **Range:** The region of the input variable over which the sensor is intended to operate (e.g., -200 to +850°C for a PT100 RTD)
- **Span:** The algebraic difference between the upper and lower limits of the range (e.g., 1050°C span for the above example)
- **Full-Scale Output (FSO):** The output at maximum input

---

## Dynamic Characteristics

Dynamic characteristics describe how the measurement system responds to time-varying inputs. A sensor with excellent static characteristics may still be inadequate if it cannot follow rapid changes in the physical quantity.

### First-Order Systems

Most thermal sensors (RTD, thermistor, thermocouple) behave approximately as first-order systems. The governing differential equation is:

```
τ · dq_out/dt + q_out = K · q_in(t)
```

Where:
- `τ` = time constant (seconds)
- `K` = static sensitivity (or gain)
- `q_in(t)` = time-varying input

For a step input of magnitude A starting at t=0:

```
q_out(t) = K · A · (1 - e^(-t/τ))
```

This gives:
- At t = τ: output reaches 63.2% of final value
- At t = 2τ: 86.5%
- At t = 5τ: 99.3% (considered "settled")

The time constant for a thermal sensor is:

```
τ = m · c_p / (h · A_s)
```

Where:
- `m` = sensor mass (kg)
- `c_p` = specific heat capacity (J/kg·K)
- `h` = heat transfer coefficient (W/m²·K)
- `A_s` = sensor surface area (m²)

This explains why larger, more massive sensors (like sheathed RTDs) have larger time constants and respond more slowly.

### Step Response Parameters

When a step input is applied, the response is characterized by:

| Parameter | Definition |
|---|---|
| Rise time (t_r) | Time to go from 10% to 90% of final value |
| Settling time (t_s) | Time to remain within ±ε% of final value |
| Time constant (τ) | Time to reach 63.2% of final value |
| Delay time (t_d) | Time to reach 50% of final value |

For a first-order system:
- Rise time: `t_r ≈ 2.2 τ`
- Settling time (2%): `t_s ≈ 4 τ`

### Frequency Response

The frequency domain representation of a first-order sensor is the transfer function:

```
H(jω) = K / (1 + jωτ)
```

Magnitude:

```
|H(jω)| = K / √(1 + (ωτ)²)
```

Phase:

```
∠H(jω) = -arctan(ωτ)
```

The -3 dB bandwidth (cutoff frequency) is:

```
f_c = 1 / (2π τ)
```

At frequencies above f_c, the sensor output is attenuated — it cannot follow the input accurately. This sets the maximum rate of change that can be measured.

**Example:** A PT100 RTD with τ = 3 seconds has a bandwidth of:

```
f_c = 1 / (2π × 3) ≈ 0.053 Hz
```

This means it can only accurately track temperature changes slower than about 1 cycle per 19 seconds. Rapid thermal transients will be underestimated in magnitude.

### Dead Time

Some measurement systems introduce a pure delay (dead time) before any response occurs. This is modeled as:

```
q_out(t) = K · q_in(t - t_dead)
```

Dead time is particularly problematic in feedback control systems, where it introduces phase lag and reduces stability margins.

---

## The Transfer Function Perspective

For a complete measurement chain, the overall transfer function is the product of individual stage transfer functions:

```
H_total(s) = H_sensor(s) · H_bridge(s) · H_amplifier(s) · H_filter(s)
```

Each stage contributes:
- Gain (or attenuation)
- Phase shift
- Bandwidth limitation
- Noise

The overall bandwidth is approximately:

```
1/BW_total² ≈ 1/BW_1² + 1/BW_2² + 1/BW_3² + ...
```

The stage with the lowest bandwidth dominates. In thermal measurement systems, the sensor itself is usually the bandwidth-limiting element.

---

## Signal-to-Noise Ratio (SNR)

SNR is the ratio of signal power to noise power:

```
SNR = 20 · log₁₀(V_signal / V_noise)    [dB]
```

To resolve a signal:

```
V_signal > V_noise
```

In practice, for reliable measurement with margin:

```
SNR > 40 dB    (signal 100× larger than noise)
```

The minimum detectable signal (MDS) is set by the noise floor:

```
V_noise = √(4 k_B T R BW)    [Johnson-Nyquist noise]
```

Where:
- `k_B` = Boltzmann constant (1.38 × 10⁻²³ J/K)
- `T` = temperature (K)
- `R` = source resistance (Ω)
- `BW` = bandwidth (Hz)

This means that wider bandwidth → more noise → reduced SNR. Filtering to the minimum required bandwidth is essential in precision measurement.

---

## Summary Table of Static Characteristics

| Characteristic | Definition | Typical Specification Format |
|---|---|---|
| Accuracy | Closeness to true value | ±°C, ±% FS |
| Precision | Repeatability | σ (standard deviation) |
| Sensitivity | dOutput/dInput | Ω/°C, μV/°C |
| Resolution | Minimum detectable change | °C, mV |
| Linearity | Deviation from best-fit line | ±% FS |
| Hysteresis | Direction-dependent error | ±% FS |
| Drift | Time-dependent output change | ppm/°C, °C/year |
| Range | Operating input limits | °C min to °C max |
| Span | Full-scale range width | °C (= max - min) |

---

## Conclusion

Measurement theory provides the language for describing, specifying, and comparing sensors and measurement systems. Without this vocabulary and the underlying mathematics, it is impossible to:
- Select the right sensor for an application
- Design an appropriate signal conditioning chain
- Quantify system performance or error budgets
- Diagnose measurement problems

Every following section in this project references concepts defined here. The time invested in understanding these fundamentals pays compounding returns throughout the rest of the project.
