# FLAM R&D Parametric Curve Parameter Estimation

## Overview

This project estimates the unknown parameters of a parametric curve using the provided `xy_data.csv` dataset containing 1500 points.

The unknown parameters are:

- θ (Theta)
- M
- X

The solution uses mathematical transformation, numerical optimization, L1 loss minimization, and curve validation.

---

## Problem Statement

The given parametric equations are:

$$
x=t\cos(\theta)-e^{M|t|}\sin(0.3t)\sin(\theta)+X
$$

$$
y=42+t\sin(\theta)+e^{M|t|}\sin(0.3t)\cos(\theta)
$$

Parameter constraints:

| Parameter | Range |
|---|---|
| θ | 0° < θ < 50° |
| M | -0.05 < M < 0.05 |
| X | 0 < X < 100 |
| t | 6 < t < 60 |

---

## Approach

Since the given range ensures that `t` is always positive:

$$
|t|=t
$$

The curve was analyzed by transforming the data into components parallel and perpendicular to the direction defined by θ.

For each candidate set of parameters, `t` was recovered and the predicted curve was compared with the given data.

Bounded numerical optimization was used to find the parameter values that minimized the L1 error.

---

## Optimization Results

The optimization produced:

| Parameter | Value |
|---|---:|
| θ | 29.999973° |
| M | 0.0299999971 |
| X | 54.9999983399 |

These values were rounded to:

### Final Parameters

- **θ = 30°**
- **M = 0.03**
- **X = 55**

The recovered parameter range was approximately:

```text
6.05 < t < 60