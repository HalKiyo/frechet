import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gumbel_r

# --- Data loading ---
input_path = "../dat/arakawa_max_y120.bin"
data = np.fromfile(input_path, dtype=np.float32, count=240)

# Reshape into 2 columns: year, outflow
data = data.reshape(-1, 2)
amax = pd.DataFrame(data, columns=["year", "outflow"])

# --- Fitting Gumbel distribution ---
# gumbel_r.fit returns loc (mu) and scale (beta)
loc_hat, scale_hat = gumbel_r.fit(amax["outflow"])
print(f"Fitted Gumbel parameters: loc = {loc_hat:.2f}, scale = {scale_hat:.2f}")

# --- PDF calculation ---
y_min = amax["outflow"].min() - 500
y_max = amax["outflow"].max() + 10
y_vals = np.linspace(y_min, y_max, 240)
pdf_vals = gumbel_r.pdf(y_vals, loc=loc_hat, scale=scale_hat)

# --- Visualization ---
fig, (ax1, ax2) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]}, figsize=(12, 6))

# Left: year vs outflow scatter plot
ax1.scatter(amax["year"], amax["outflow"], color='blue', alpha=0.7, label="Observed Outflow")
ax1.axhline(0, color='black', linestyle='--')
ax1.set_xlabel("Year")
ax1.set_ylabel("Outflow (m3/s)")
ax1.set_title("Annual Max Outflow (Gumbel fit)")
ax1.set_ylim(y_min, y_max)

# Right: Gumbel PDF vs outflow
ax2.plot(pdf_vals, y_vals, color='darkgreen', lw=2, label="Gumbel PDF")
ax2.axhline(0, color='black', linestyle='--')
ax2.set_xlabel("Gumbel Density")
ax2.set_yticks([])
ax2.set_title("Gumbel PDF")
ax2.set_xlim(0, np.nanmax(pdf_vals) * 1.1)
ax2.set_ylim(y_min, y_max)

plt.tight_layout()
plt.show()

# --- Q100 calculation ---
q100 = gumbel_r.ppf(0.99, loc=loc_hat, scale=scale_hat)
print(f"Q100 (Gumbel, 99% quantile): {q100:.2f} m3/s")
