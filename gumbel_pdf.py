from scipy.stats import gumbel_r

from evd_plot import load_amax, plot_fit

amax = load_amax()

# --- Fitting Gumbel distribution ---
# gumbel_r.fit returns loc (mu) and scale (beta)
loc_hat, scale_hat = gumbel_r.fit(amax["outflow"])
print(f"Fitted Gumbel parameters: loc = {loc_hat:.2f}, scale = {scale_hat:.2f}")

# --- PDF calculation and visualization ---
plot_fit(amax, lambda y: gumbel_r.pdf(y, loc=loc_hat, scale=scale_hat),
         fit_name="Gumbel", dist_name="Gumbel")

# --- Q100 calculation ---
q100 = gumbel_r.ppf(0.99, loc=loc_hat, scale=scale_hat)
print(f"Q100 (Gumbel, 99% quantile): {q100:.2f} m3/s")
