import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution


# ============================================================
# FLAM R&D PARAMETRIC CURVE PARAMETER ESTIMATION
# ============================================================

print("=" * 60)
print("FLAM R&D PARAMETRIC CURVE PARAMETER ESTIMATION")
print("=" * 60)


# ============================================================
# LOAD DATA
# ============================================================

data = pd.read_csv("xy_data.csv")

print(f"\nNumber of data points: {len(data)}")
print(f"Columns: {list(data.columns)}")

print("\nFirst 5 rows:")
print(data.head())


# Extract coordinates
x_data = data["x"].values
y_data = data["y"].values


# ============================================================
# PARAMETRIC CURVE FUNCTIONS
# ============================================================

def recover_t(theta, X, x, y):
    """
    Recover parameter t by projecting points onto
    the primary direction of the parametric curve.
    """

    return (
        (x - X) * np.cos(theta)
        + (y - 42) * np.sin(theta)
    )


def calculate_perpendicular_component(theta, X, x, y):
    """
    Calculate the perpendicular component of each point.
    """

    return (
        -(x - X) * np.sin(theta)
        + (y - 42) * np.cos(theta)
    )


def l1_loss(params):
    """
    Calculate the L1 loss for candidate values of:
    theta, M and X.
    """

    theta, M, X = params

    # Recover t values
    t = recover_t(theta, X, x_data, y_data)

    # Observed perpendicular component
    w_actual = calculate_perpendicular_component(
        theta,
        X,
        x_data,
        y_data
    )

    # Predicted perpendicular component
    w_predicted = (
        np.exp(M * np.abs(t))
        * np.sin(0.3 * t)
    )

    # Penalize invalid t values
    penalty = np.sum(
        np.maximum(0, 6 - t)
        + np.maximum(0, t - 60)
    )

    # Mean L1 error
    loss = np.mean(
        np.abs(w_actual - w_predicted)
    )

    return loss + penalty


# ============================================================
# PARAMETER OPTIMIZATION
# ============================================================

print("\nRunning parameter optimization...")
print("Please wait...")


# Parameter bounds
bounds = [
    (np.radians(0.001), np.radians(49.999)),  # Theta
    (-0.05, 0.05),                            # M
    (0, 100)                                  # X
]


# Run global optimization
result = differential_evolution(
    l1_loss,
    bounds,
    strategy="best1bin",
    maxiter=1000,
    popsize=20,
    tol=1e-9,
    polish=True,
    seed=42
)


# Optimized parameters
theta_opt, M_opt, X_opt = result.x

theta_degrees = np.degrees(theta_opt)


# Recover t values
t_recovered = recover_t(
    theta_opt,
    X_opt,
    x_data,
    y_data
)


# ============================================================
# OPTIMIZATION RESULTS
# ============================================================

print("\n" + "=" * 60)
print("OPTIMIZATION RESULTS")
print("=" * 60)

print(f"\nTheta (radians): {theta_opt:.10f}")
print(f"Theta (degrees): {theta_degrees:.6f}")
print(f"M: {M_opt:.10f}")
print(f"X: {X_opt:.10f}")

print(f"\nFinal L1 Loss: {result.fun:.10f}")

print("\nRecovered t range:")
print(f"Minimum t: {np.min(t_recovered):.6f}")
print(f"Maximum t: {np.max(t_recovered):.6f}")


# ============================================================
# ROUNDED PARAMETER VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("VALIDATION USING ROUNDED PARAMETERS")
print("=" * 60)


# Final rounded parameters
theta_final_degrees = 30
theta_final = np.radians(theta_final_degrees)

M_final = 0.03
X_final = 55


# Calculate L1 loss using rounded parameters
rounded_loss = l1_loss(
    [theta_final, M_final, X_final]
)


# Recover t values using rounded parameters
t_final = recover_t(
    theta_final,
    X_final,
    x_data,
    y_data
)


print("\nFinal Parameter Values:")
print(f"Theta: {theta_final_degrees} degrees")
print(f"M: {M_final}")
print(f"X: {X_final}")

print(
    f"\nL1 Loss using rounded parameters: "
    f"{rounded_loss:.10f}"
)

print("\nRecovered t range using rounded parameters:")
print(f"Minimum t: {np.min(t_final):.6f}")
print(f"Maximum t: {np.max(t_final):.6f}")


# ============================================================
# UNIFORMLY SAMPLED CURVE L1 EVALUATION
# ============================================================

print("\n" + "=" * 60)
print("UNIFORMLY SAMPLED CURVE L1 EVALUATION")
print("=" * 60)


# Sort actual data according to recovered t values
sort_index = np.argsort(t_final)

x_actual_sorted = x_data[sort_index]
y_actual_sorted = y_data[sort_index]

t_actual_sorted = t_final[sort_index]


# Create uniformly sampled t values
num_points = len(data)

t_uniform = np.linspace(
    np.min(t_actual_sorted),
    np.max(t_actual_sorted),
    num_points
)


# Generate predicted curve
x_predicted = (
    t_uniform * np.cos(theta_final)
    - np.exp(M_final * np.abs(t_uniform))
    * np.sin(0.3 * t_uniform)
    * np.sin(theta_final)
    + X_final
)


y_predicted = (
    42
    + t_uniform * np.sin(theta_final)
    + np.exp(M_final * np.abs(t_uniform))
    * np.sin(0.3 * t_uniform)
    * np.cos(theta_final)
)


# Interpolate actual values to uniformly sampled t points
x_actual_uniform = np.interp(
    t_uniform,
    t_actual_sorted,
    x_actual_sorted
)

y_actual_uniform = np.interp(
    t_uniform,
    t_actual_sorted,
    y_actual_sorted
)


# Calculate L1 distances
l1_x = np.mean(
    np.abs(x_actual_uniform - x_predicted)
)

l1_y = np.mean(
    np.abs(y_actual_uniform - y_predicted)
)

combined_l1 = (
    l1_x + l1_y
) / 2


print(f"\nNumber of uniformly sampled points: {num_points}")

print("\nL1 Distance Results:")
print(f"L1 distance for X coordinates: {l1_x:.10f}")
print(f"L1 distance for Y coordinates: {l1_y:.10f}")

print(
    f"\nCombined Curve L1 Distance: "
    f"{combined_l1:.10f}"
)


# ============================================================
# CREATE PLOTS DIRECTORY
# ============================================================

os.makedirs("plots", exist_ok=True)


# ============================================================
# PREDICTED CURVE VS ACTUAL DATA
# ============================================================

plt.figure(figsize=(10, 7))


# Actual data
plt.scatter(
    x_data,
    y_data,
    s=15,
    alpha=0.6,
    label="Actual Data"
)


# Predicted curve
plt.plot(
    x_predicted,
    y_predicted,
    linewidth=2.5,
    label="Predicted Curve"
)


plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")

plt.title(
    "Predicted Parametric Curve vs Actual Data"
)

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()


# Save graph
plt.savefig(
    "plots/predicted_vs_actual.png",
    dpi=300
)

plt.close()


print(
    "\nSaved: plots\\predicted_vs_actual.png"
)


# ============================================================
# FINAL ANSWER
# ============================================================

print("\n" + "=" * 60)
print("FINAL ANSWER")
print("=" * 60)

print(
    f"\nTheta (theta) = "
    f"{theta_final_degrees} degrees"
)

print(f"M = {M_final}")

print(f"X = {X_final}")