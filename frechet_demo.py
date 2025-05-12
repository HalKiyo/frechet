import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.special import gamma

# --- Fréchet Distribution (maximum type) Functions ---
class FrechetMax:
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma
    
    def pdf(self, x):
        """ Probability Density Function (PDF) """
        z = (x - self.mu) / self.sigma
        z = np.maximum(z, 1e-10)  # avoid negative or zero
        return (1 / self.sigma) * (z ** -2) * np.exp(-z ** -1)
    
    def rvs(self, size):
        """ Random Variate Sampling """
        u = np.random.uniform(0, 1, size)
        return self.mu + self.sigma * (u ** -1 - 1)

# --- Step 1: Load Binary Data ---
input_path = "../dat/arakawa_max_y120.bin"
data = np.fromfile(input_path, dtype=np.float32, count=240)

# --- Step 2: Reshape to DataFrame ---
data = data.reshape(-1, 2)
amax = pd.DataFrame(data, columns=["year", "outflow"])

# --- Step 3: Dummy Parameters (mu, sigma) ---
# In practice, these should come from a fitting process
mu_hat = np.exp(5.0)       # Dummy example (replace with fitting result)
sigma_hat = np.exp(2.0)    # Dummy example (replace with fitting result)

# Fréchet instance
frechet = FrechetMax(mu_hat, sigma_hat)

# --- Step 4: Random Sampling ---
n = 3000 * 120
np.random.seed(123)
x = frechet.rvs(n)

# --- Assign Random Years ---
years = np.random.randint(1980, 2100, size=n)

# --- Step 5: DataFrame for Results ---
df = pd.DataFrame({
    "year": years,
    "outflow": x
})

# --- Step 6: Scatter Plot ---
plt.figure(figsize=(10, 6))
plt.scatter(df['year'], df['outflow'], s=5, alpha=0.5, color='royalblue')
plt.axhline(df['outflow'].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
plt.xlabel("Year")
plt.ylabel("Simulated Outflow (m³/s)")
plt.title("Simulated Annual Max Outflows (Fréchet Distribution)")
plt.legend()
plt.show()

# --- Step 7: Histogram and Theoretical PDF ---
plt.figure(figsize=(10, 6))
counts, bins, _ = plt.hist(x, bins=50, color='skyblue', edgecolor='white', density=True)

# Overlay Fréchet PDF
x_vals = np.linspace(bins[0], bins[-1], 1000)
plt.plot(x_vals, frechet.pdf(x_vals), color='red', linewidth=2, label='Fréchet PDF')

plt.title(f"Random Samples from Fréchet Distribution\n(mu = {mu_hat:.2f}, sigma = {sigma_hat:.2f})")
plt.xlabel("Value")
plt.ylabel("Density")
plt.legend()
plt.show()

