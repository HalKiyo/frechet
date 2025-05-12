import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import genextreme

input_path = "../dat/arakawa_max_y120.bin"
data = np.fromfile(input_path, dtype=np.float32, count=240)

# 2 columns (year, outflow)
data = data.reshape(-1, 2)
amax = pd.DataFrame(data, columns=["year", "outflow"])

# Fitting Frechet distribution(genextreme)
c_hat, loc_hat, scale_hat = genextreme.fit(amax["outflow"])
print(f"Fitted parameters: c = {c_hat:.4f} (if frechet then c < 0), loc = {loc_hat:.2f}, scale = {scale_hat:.2f}")

# 3 frechet PDF calculation
y_min = amax["outflow"].min() - 500
y_max = amax["outflow"].max() + 10
y_vals = np.linspace(y_min, y_max, 240)
pdf_vals = genextreme.pdf(y_vals, c_hat, loc=loc_hat, scale=scale_hat)

# step 4 visualize

fig, (ax1, ax2) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]}, figsize=(12, 6))

# left: year vs outflow
ax1.scatter(amax["year"], amax["outflow"], color='blue', alpha=0.7, label="Observed Outflow")
ax1.axhline(0, color='black', linestyle='--')
ax1.set_xlabel("Year")
ax1.set_ylabel("Outflow (m3/s)")
ax1.set_title("Annual Max Outflow (frechet fit)")
ax1. set_ylim(y_min, y_max)

# right: pdf vs outflow
ax2.plot(pdf_vals, y_vals, color='darkgreen', lw=2, label="Frechet PDF")
ax2.axhline(0, color='black', linestyle='--')
ax2.set_xlabel("Frechet Density")
ax2.set_yticks([])
ax2.set_title("Frechet PDF")
ax2.set_xlim(0, np.nanmax(pdf_vals)*1.1)
ax2.set_ylim(y_min, y_max)

plt.tight_layout()
plt.show()

# step 5 Q100 calculation
q100 = genextreme.ppf(0.99, c_hat, loc=loc_hat, scale=scale_hat)
print(f"Q100 (Frechet, 99% quantile): {q100:.2f} m3/s")
