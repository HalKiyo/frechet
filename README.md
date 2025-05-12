## Data Description

### arakawa_max_y120.bin
- **Description**: Pseudo-observed annual maximum discharge data for the Arakawa River over a 120-year period (1980–2099).
- **Contents**: Records of annual maximum discharge (units: m³/s).
- **Generation Method**:  
  - Based on CMIP6 ACCESS (Australian model) climate simulation outputs.  
  - River discharge simulated using the global river routing model **CaMa-Flood** at a 6-minute spatial resolution (approx. 10 km grid), with daily outputs.  
  - Annual maximum discharges were extracted from these daily simulations.

### osse_gum_e3000_y120.bin
- **Description**: Generated pseudo-observed data by fitting a non-stationary Gumbel distribution to the `arakawa_max_y120.bin` dataset.  
- **Contents**: 3,000 ensemble sets of annual maximum discharge data for the period 1980–2099, resulting in a total of 360,000 samples.
- **Purpose**: Designed for OSSE (Observing System Simulation Experiment) applications, used to evaluate estimation methods for extreme flood quantiles.

## Scripts Description

### ranking.py
- **Function**: Expands the `osse_gum_e3000_y120.bin` dataset and performs order-statistics-based estimation of the 100-year return period discharge (Q100) from all 360,000 samples.
- **Method**: Calculates empirical quantiles using ranking (order statistics) across the full ensemble.

### frechet.py
- **Function**: Fits a Fréchet distribution to the `arakawa_max_y120.bin` dataset and estimates the 100-year return period discharge (Q100).
- **Method**: Utilizes the generalized extreme value distribution (Fréchet type, c < 0) to model annual maxima and compute Q100.

### gumbel.py
- **Function**: Fits a stationary Gumbel distribution to the `arakawa_max_y120.bin` dataset and estimates the 100-year return period discharge (Q100).
- **Method**: Applies the Gumbel (type I extreme value) distribution to annual maxima and computes the Q100 quantile.


