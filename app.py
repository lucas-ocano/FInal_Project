"""Interactive Streamlit Black-Scholes pricer."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from black_scholes import OptionInputs, call_price, greeks, put_price, validate_inputs

st.set_page_config(page_title="Black-Scholes Option Pricer", layout="wide")

st.title("📈 Black-Scholes Option Pricer")
st.caption("Interactive option pricing and Greeks visualizer")

with st.sidebar:
    st.header("Model inputs")
    spot = st.slider("Spot price (S)", min_value=1.0, max_value=300.0, value=100.0, step=1.0)
    strike = st.slider("Strike price (K)", min_value=1.0, max_value=300.0, value=100.0, step=1.0)
    time_to_maturity = st.slider(
        "Time to maturity (years)", min_value=0.01, max_value=5.0, value=1.0, step=0.01
    )
    rate_pct = st.slider("Risk-free rate (%)", min_value=-5.0, max_value=20.0, value=5.0, step=0.1)
    vol_pct = st.slider("Volatility (%)", min_value=1.0, max_value=150.0, value=20.0, step=0.5)

inputs = OptionInputs(
    spot=spot,
    strike=strike,
    time_to_maturity=time_to_maturity,
    rate=rate_pct / 100,
    volatility=vol_pct / 100,
)

errors = validate_inputs(inputs)
if errors:
    for err in errors:
        st.error(err)
    st.stop()

call = call_price(inputs)
put = put_price(inputs)
greek_values = greeks(inputs)

c1, c2, c3 = st.columns(3)
c1.metric("Call price", f"${call:,.2f}")
c2.metric("Put price", f"${put:,.2f}")
c3.metric("Put-Call Parity (C - P)", f"{(call - put):,.2f}")

st.subheader("Greeks")
st.dataframe(
    pd.DataFrame(
        {
            "Greek": [
                "Call Delta",
                "Put Delta",
                "Gamma",
                "Vega (per 1% vol)",
                "Call Theta (per day)",
                "Put Theta (per day)",
                "Call Rho (per 1% rate)",
                "Put Rho (per 1% rate)",
            ],
            "Value": [
                greek_values["call_delta"],
                greek_values["put_delta"],
                greek_values["gamma"],
                greek_values["vega"],
                greek_values["call_theta"],
                greek_values["put_theta"],
                greek_values["call_rho"],
                greek_values["put_rho"],
            ],
        }
    ).style.format({"Value": "{:.4f}"}),
    use_container_width=True,
)

st.subheader("How option value changes with spot price")
spot_grid = np.linspace(max(1.0, 0.4 * strike), 1.6 * strike, 120)
call_curve = []
put_curve = []
for s in spot_grid:
    scenario = OptionInputs(
        spot=float(s),
        strike=inputs.strike,
        time_to_maturity=inputs.time_to_maturity,
        rate=inputs.rate,
        volatility=inputs.volatility,
    )
    call_curve.append(call_price(scenario))
    put_curve.append(put_price(scenario))

fig = go.Figure()
fig.add_trace(go.Scatter(x=spot_grid, y=call_curve, mode="lines", name="Call value"))
fig.add_trace(go.Scatter(x=spot_grid, y=put_curve, mode="lines", name="Put value"))
fig.add_vline(x=strike, line_dash="dash", annotation_text="Strike")
fig.update_layout(
    xaxis_title="Spot price",
    yaxis_title="Option value",
    legend_title="Option",
    template="plotly_white",
)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
### Tips for experimentation
- Increase **volatility** to observe both call and put prices rise.
- Move **time to maturity** to see stronger time value.
- Adjust **risk-free rate** and compare call vs put sensitivity.
"""
)
