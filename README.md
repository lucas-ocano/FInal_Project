# Black-Scholes Interactive Pricer

This project provides a simple **interactive GUI** for Black-Scholes option pricing using Streamlit.

## Features

- Interactive sliders for:
  - Spot price (S)
  - Strike price (K)
  - Time to maturity (T)
  - Risk-free rate (r)
  - Volatility (σ)
- Real-time Call and Put prices
- Key Greeks (Delta, Gamma, Vega, Theta, Rho)
- Dynamic chart showing how option values change with underlying spot price

## Run locally

1. Create and activate a virtual environment (recommended)
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Launch the app:

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal (usually `http://localhost:8501`).

## Notes

- This implementation is for educational/demo purposes.
- The model assumes European options and constant volatility/rates.
