"""
Utility functions for signal processing
"""
import numpy as np
from typing import Tuple

def validate_signal(t: np.ndarray, x: np.ndarray) -> bool:
    """Validate signal arrays"""
    if len(t) != len(x):
        return False
    if not np.all(np.isfinite(x)):
        return False
    if not np.all(np.diff(t) > 0):  # Check if time is strictly increasing
        return False
    return True

def normalize_signal(x: np.ndarray) -> np.ndarray:
    """Normalize signal to [-1, 1] range"""
    max_val = np.max(np.abs(x))
    if max_val == 0:
        return x
    return x / max_val

def calculate_snr(signal: np.ndarray, noise: np.ndarray) -> float:
    """Calculate Signal-to-Noise Ratio in dB"""
    signal_power = np.mean(signal ** 2)
    noise_power = np.mean(noise ** 2)
    if noise_power == 0:
        return np.inf
    return 10 * np.log10(signal_power / noise_power)

def generate_pole_zero_plot(b: np.ndarray, a: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Generate poles and zeros for plotting"""
    zeros = np.roots(b)
    poles = np.roots(a)
    return zeros, poles