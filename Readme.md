# FLAM R&D Assignment

## Parametric Curve Parameter Estimation

---

# Final Result

The unknown parameters recovered from the provided `xy_data.csv` dataset are:

- **Theta (θ) = 30 degrees**
- **M = 0.03**
- **X = 55**

The numerical optimization successfully recovered these parameter values from the provided dataset.

The uniformly sampled curve evaluation produced a combined L1 distance of:

$$
\boxed{0.1502428596}
$$

---

## Overview

This project presents a numerical approach for estimating the unknown parameters of a parametric curve using the provided `xy_data.csv` dataset.

The objective is to estimate the following variables:

- $\theta$ (theta)
- $M$
- $X$

The solution uses coordinate transformation, numerical optimization, L1 loss minimization, parameter validation, curve generation, and residual analysis.

The provided dataset contains **1500 coordinate points**.

---

# 1. Problem Statement

The given parametric curve is:

$$
x=t\cos(\theta)-e^{M|t|}\sin(0.3t)\sin(\theta)+X
$$

$$
y=42+t\sin(\theta)+e^{M|t|}\sin(0.3t)\cos(\theta)
$$

The unknown parameters are:

$$
\theta,\quad M,\quad X
$$

The parameter constraints are:

| Parameter | Range |
|---|---|
| $\theta$ | $0^\circ < \theta < 50^\circ$ |
| $M$ | $-0.05 < M < 0.05$ |
| $X$ | $0 < X < 100$ |
| $t$ | $6 < t < 60$ |

The `xy_data.csv` dataset contains 1500 points generated from the parametric curve.

---

# 2. Mathematical Simplification

The parameter range specifies:

$$
6<t<60
$$

Since $t$ is always positive:

$$
|t|=t
$$

Therefore, the parametric equations can be simplified to:

$$
x=t\cos(\theta)-e^{Mt}\sin(0.3t)\sin(\theta)+X
$$

$$
y=42+t\sin(\theta)+e^{Mt}\sin(0.3t)\cos(\theta)
$$

This simplified form is used during the numerical estimation process.

---

# 3. Parameter Recovery Approach

The curve can be analyzed using two perpendicular coordinate directions.

The primary direction is:

$$
(\cos(\theta),\sin(\theta))
$$

The perpendicular direction is:

$$
(-\sin(\theta),\cos(\theta))
$$

For a candidate value of $\theta$ and $X$, the parameter $t$ can be estimated by projecting each point onto the primary direction:

$$
t=(x-X)\cos(\theta)+(y-42)\sin(\theta)
$$

The perpendicular component is:

$$
w=-(x-X)\sin(\theta)+(y-42)\cos(\theta)
$$

For the correct parameter values:

$$
w=e^{Mt}\sin(0.3t)
$$

This transformation allows the optimization process to estimate only the three unknown parameters instead of independently searching for a value of $t$ for every data point.

---

# 4. Numerical Optimization

The parameters were estimated using bounded global numerical optimization.

The search boundaries were:

```text
Theta: 0° to 50°
M: -0.05 to 0.05
X: 0 to 100
```

For every candidate set of parameters:

1. The coordinates are transformed.
2. The parameter $t$ is recovered.
3. The perpendicular component is calculated.
4. A predicted perpendicular component is generated.
5. The L1 error is calculated.
6. The optimization algorithm searches for parameters that minimize the error.

---

# 5. L1 Loss Calculation

For every data point, the recovered value of $t$ is:

$$
t=(x-X)\cos(\theta)+(y-42)\sin(\theta)
$$

The observed perpendicular component is:

$$
w=-(x-X)\sin(\theta)+(y-42)\cos(\theta)
$$

The predicted component is:

$$
w_{\text{pred}}=e^{Mt}\sin(0.3t)
$$

The mean L1 loss is calculated as:

$$
L_1=
\frac{1}{N}
\sum_{i=1}^{N}
\left|w_i-w_{\text{pred},i}\right|
$$

where $N$ represents the total number of data points.

The objective of the optimization process is to minimize this error.

---

# 6. Optimization Results

The numerical optimization produced the following results:

| Parameter | Optimized Value |
|---|---:|
| $\theta$ (radians) | 0.5235983044 |
| $\theta$ (degrees) | 29.999973 |
| $M$ | 0.0299999971 |
| $X$ | 54.9999983399 |

The final optimization L1 loss was:

$$
L_1=0.0000025586
$$

The recovered range of the parameter $t$ was:

$$
6.049405 \leq t \leq 59.995171
$$

This is consistent with the specified constraint:

$$
6<t<60
$$

---

# 7. Validation Using Rounded Parameters

The optimized values are extremely close to simple numerical values.

The final rounded parameter values are:

$$
\boxed{\theta=30^\circ}
$$

$$
\boxed{M=0.03}
$$

$$
\boxed{X=55}
$$

The rounded values were evaluated again.

The resulting L1 loss was:

$$
L_1=0.0000150483
$$

The recovered range of $t$ using the rounded parameters was:

$$
6.049404 \leq t \leq 59.995167
$$

The small error confirms that the rounded parameters accurately represent the recovered solution.

---

# 8. Uniformly Sampled Curve Evaluation

The predicted curve was evaluated using 1500 sampled points.

The following coordinate-wise L1 distances were obtained:

| Measurement | L1 Distance |
|---|---:|
| X-coordinate distance | 0.2108307222 |
| Y-coordinate distance | 0.0896549970 |
| **Combined Curve L1 Distance** | **0.1502428596** |

The combined value is calculated from the average of the X-coordinate and Y-coordinate L1 distances.

This evaluation provides an additional numerical comparison between the generated curve and the provided data.

---

# 9. Final Parametric Equation

Using the recovered parameters:

$$
\theta=30^\circ
$$

$$
M=0.03
$$

$$
X=55
$$

the final parametric equations become:

$$
x=55+0.8660254t-0.5e^{0.03t}\sin(0.3t)
$$

$$
y=42+0.5t+0.8660254e^{0.03t}\sin(0.3t)
$$

where:

$$
6<t<60
$$

---

# 10. Generated Visualizations

The program automatically generates multiple plots to visualize and validate the solution.

## Given Data

The original dataset is visualized and saved as:

```text
plots/given_data.png
```

![Given Data](plots/given_data.png)

---

## Predicted Curve vs Actual Data

The predicted curve generated using the recovered parameters is compared with the original data.

The visualization is saved as:

```text
plots/predicted_vs_actual.png
```

![Predicted Curve vs Actual Data](plots/predicted_vs_actual.png)

---

## Residual Analysis

The residual analysis compares the differences between the predicted and actual coordinate values.

The visualization is saved as:

```text
plots/residual_analysis.png
```

![Residual Analysis](plots/residual_analysis.png)

---

# 11. Program Output

The project can be executed using:

```bash
python main.py
```

The program performs the following operations:

1. Loads the provided dataset.
2. Displays information about the 1500 data points.
3. Generates a plot of the original data.
4. Performs numerical parameter optimization.
5. Recovers $\theta$, $M$, and $X$.
6. Validates the rounded parameter values.
7. Evaluates the generated curve.
8. Calculates L1 distances.
9. Creates residual analysis plots.
10. Displays the final recovered parameters.

The final program output is:

```text
Theta (theta) = 30 degrees
M = 0.03
X = 55
```

---

# 12. How to Run the Project

## Step 1: Clone the Repository

```bash
git clone <repository-url>
```

## Step 2: Navigate to the Project Folder

```bash
cd <project-folder-name>
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Run the Program

```bash
python main.py
```

---

# 13. Requirements

The project requires the following Python libraries:

```text
numpy
pandas
matplotlib
scipy
```

These dependencies can be installed using:

```bash
pip install -r requirements.txt
```

---

# 14. Project Structure

```text
flam_curve_parameter_estimation/
│
├── README.md
├── requirements.txt
├── main.py
├── xy_data.csv
│
└── plots/
    ├── given_data.png
    ├── predicted_vs_actual.png
    └── residual_analysis.png
```

---

# 15. Final Answer

The recovered parameters of the parametric curve are:

$$
\boxed{\theta=30^\circ}
$$

$$
\boxed{M=0.03}
$$

$$
\boxed{X=55}
$$

Therefore:

- **Theta (θ) = 30 degrees**
- **M = 0.03**
- **X = 55**

The optimization process achieved an extremely small parameter-recovery loss:

$$
\boxed{0.0000025586}
$$

The uniformly sampled curve comparison produced a combined L1 distance of:

$$
\boxed{0.1502428596}
$$

---

# Conclusion

This project successfully estimates the unknown parameters of the given parametric curve using coordinate transformation and bounded numerical optimization.

The recovered values are:

$$
\boxed{\theta=30^\circ,\quad M=0.03,\quad X=55}
$$

The optimization results demonstrate that these parameters accurately reconstruct the provided parametric dataset.

The repository includes the complete Python implementation, mathematical explanation, numerical results, generated visualizations, and instructions for reproducing the analysis.
