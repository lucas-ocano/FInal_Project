"""Core Black-Scholes pricing and Greeks helpers."""

from __future__ import annotations

from dataclasses import dataclass
from math import erf, exp, log, pi, sqrt


@dataclass(frozen=True)
class OptionInputs:
    spot: float
    strike: float
    time_to_maturity: float
    rate: float
    volatility: float


def _std_norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))


def _std_norm_pdf(x: float) -> float:
    return (1.0 / sqrt(2.0 * pi)) * exp(-0.5 * x * x)


def d1(inputs: OptionInputs) -> float:
    numerator = log(inputs.spot / inputs.strike) + (
        inputs.rate + 0.5 * inputs.volatility**2
    ) * inputs.time_to_maturity
    denominator = inputs.volatility * sqrt(inputs.time_to_maturity)
    return numerator / denominator


def d2(inputs: OptionInputs) -> float:
    return d1(inputs) - inputs.volatility * sqrt(inputs.time_to_maturity)


def call_price(inputs: OptionInputs) -> float:
    d1_value = d1(inputs)
    d2_value = d2(inputs)
    discounted_strike = inputs.strike * exp(-inputs.rate * inputs.time_to_maturity)
    return inputs.spot * _std_norm_cdf(d1_value) - discounted_strike * _std_norm_cdf(d2_value)


def put_price(inputs: OptionInputs) -> float:
    d1_value = d1(inputs)
    d2_value = d2(inputs)
    discounted_strike = inputs.strike * exp(-inputs.rate * inputs.time_to_maturity)
    return discounted_strike * _std_norm_cdf(-d2_value) - inputs.spot * _std_norm_cdf(-d1_value)


def greeks(inputs: OptionInputs) -> dict[str, float]:
    d1_value = d1(inputs)
    d2_value = d2(inputs)
    discount = exp(-inputs.rate * inputs.time_to_maturity)

    call_delta = _std_norm_cdf(d1_value)
    put_delta = call_delta - 1.0
    gamma = _std_norm_pdf(d1_value) / (
        inputs.spot * inputs.volatility * sqrt(inputs.time_to_maturity)
    )
    vega = inputs.spot * _std_norm_pdf(d1_value) * sqrt(inputs.time_to_maturity) / 100

    call_theta = (
        -inputs.spot * _std_norm_pdf(d1_value) * inputs.volatility / (2 * sqrt(inputs.time_to_maturity))
        - inputs.rate * inputs.strike * discount * _std_norm_cdf(d2_value)
    ) / 365
    put_theta = (
        -inputs.spot * _std_norm_pdf(d1_value) * inputs.volatility / (2 * sqrt(inputs.time_to_maturity))
        + inputs.rate * inputs.strike * discount * _std_norm_cdf(-d2_value)
    ) / 365

    call_rho = inputs.strike * inputs.time_to_maturity * discount * _std_norm_cdf(d2_value) / 100
    put_rho = -inputs.strike * inputs.time_to_maturity * discount * _std_norm_cdf(-d2_value) / 100

    return {
        "call_delta": call_delta,
        "put_delta": put_delta,
        "gamma": gamma,
        "vega": vega,
        "call_theta": call_theta,
        "put_theta": put_theta,
        "call_rho": call_rho,
        "put_rho": put_rho,
    }


def validate_inputs(inputs: OptionInputs) -> list[str]:
    errors: list[str] = []
    if inputs.spot <= 0:
        errors.append("Spot price must be greater than 0.")
    if inputs.strike <= 0:
        errors.append("Strike price must be greater than 0.")
    if inputs.time_to_maturity <= 0:
        errors.append("Time to maturity must be greater than 0.")
    if inputs.volatility <= 0:
        errors.append("Volatility must be greater than 0.")
    return errors
