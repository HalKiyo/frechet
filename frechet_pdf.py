from scipy.stats import genextreme

from evd_plot import load_amax, plot_fit

amax = load_amax()

# Fitting Frechet distribution(genextreme)
c_hat, loc_hat, scale_hat = genextreme.fit(amax["outflow"])
print(f"Fitted parameters: c = {c_hat:.4f} (if frechet then c < 0), loc = {loc_hat:.2f}, scale = {scale_hat:.2f}")

# frechet PDF and visualization
plot_fit(amax, lambda y: genextreme.pdf(y, c_hat, loc=loc_hat, scale=scale_hat),
         fit_name="frechet", dist_name="Frechet")

# Q100 calculation
q100 = genextreme.ppf(0.99, c_hat, loc=loc_hat, scale=scale_hat)
print(f"Q100 (Frechet, 99% quantile): {q100:.2f} m3/s")
