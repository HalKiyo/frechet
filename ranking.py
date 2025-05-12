import numpy as np
import matplotlib.pyplot as plt

# step 1 loading dataset
n_years = 120
n_ensemble = 3000
output_file = "../dat/osse_gum_e3000_y120.bin"
bin_data = np.fromfile(output_file, dtype=np.float32, count=n_years*n_ensemble)
sim_matrix = bin_data.reshape((n_years, n_ensemble), order='F') # Fortran sorting
flattened_data = sim_matrix.flatten(0)

# sorting data
data_sorted = np.sort(flattened_data)[::-1] # large >>> small

# step 3 calculate rank for each return period
n = len(data_sorted)
return_periods = [2, 5, 10, 20, 50, 100, 200, 500]

# exceedance probability (p = 1/T)
# p * (n+1) is ranking based on Weibull method ( i / (n+1) = exceedance probability )
ranks = [(1/T) * (n + 1) for T in return_periods]
ranks_int = [int(round(r)) for r in ranks]

# outflow corrresponding to rank
q_values = [data_sorted[r-1] for r in ranks_int] # python starts from 0

# step 4 plotting
plt.figure(figsize=(12, 6))

# rank vs outflow at log scale
plt.plot(range(1, n+1), data_sorted, color='blue', lw=1, label="Sorted Annual Max Flows")
plt.xscale('log')
plt.xlabel("Rank")
plt.ylabel("Flow (m3/s)")
plt.title("Order Statistics of simulated Annual Maximum Flows")

for T, rank, q_val in zip(return_periods, ranks_int, q_values):
    plt.axhline(y=q_val, color='red', linestyle='--', alpha=0.7)
    plt.text(n/10, q_val*1.01, f"Q{T} = {q-val:.2f} m3/s", color = 'red', fontsize=9, va='bottom')

plt.grid(True, which="both", linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()

