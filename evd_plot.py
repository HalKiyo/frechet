"""Shared helpers for the stationary extreme value fitting scripts.

frechet_pdf.py and gumbel_pdf.py used to duplicate the data loading and
plotting code. Both now import it from here so the figures stay identical.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

INPUT_PATH = "../dat/arakawa_max_y120.bin"
N_VALUES = 240  # 120 years times 2 columns (year, outflow)
N_PDF_POINTS = 240


def load_amax(input_path=INPUT_PATH, count=N_VALUES):
    """Read the annual maximum binary file as a DataFrame with year and outflow."""
    data = np.fromfile(input_path, dtype=np.float32, count=count)
    # 2 columns (year, outflow)
    data = data.reshape(-1, 2)
    return pd.DataFrame(data, columns=["year", "outflow"])


def plot_fit(amax, pdf_func, fit_name, dist_name):
    """Draw the scatter of annual maxima next to the fitted PDF and show it.

    pdf_func maps an array of outflow values to density values.
    fit_name appears in the left panel title as "Annual Max Outflow (<fit_name> fit)".
    dist_name is used for the PDF label, x label and right panel title.
    """
    # PDF calculation
    y_min = amax["outflow"].min() - 500
    y_max = amax["outflow"].max() + 10
    y_vals = np.linspace(y_min, y_max, N_PDF_POINTS)
    pdf_vals = pdf_func(y_vals)

    fig, (ax1, ax2) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]}, figsize=(12, 6))

    # Left: year vs outflow scatter plot
    ax1.scatter(amax["year"], amax["outflow"], color='blue', alpha=0.7, label="Observed Outflow")
    ax1.axhline(0, color='black', linestyle='--')
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Outflow (m3/s)")
    ax1.set_title(f"Annual Max Outflow ({fit_name} fit)")
    ax1.set_ylim(y_min, y_max)

    # Right: PDF vs outflow
    ax2.plot(pdf_vals, y_vals, color='darkgreen', lw=2, label=f"{dist_name} PDF")
    ax2.axhline(0, color='black', linestyle='--')
    ax2.set_xlabel(f"{dist_name} Density")
    ax2.set_yticks([])
    ax2.set_title(f"{dist_name} PDF")
    ax2.set_xlim(0, np.nanmax(pdf_vals) * 1.1)
    ax2.set_ylim(y_min, y_max)

    plt.tight_layout()
    plt.show()
