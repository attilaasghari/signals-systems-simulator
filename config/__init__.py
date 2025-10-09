"""
Configuration constants for the Signals and Systems Simulator
"""
import os

# Application metadata
APP_NAME = "Signals and Systems Simulator"
APP_VERSION = "1.0.0"
AUTHOR = "Attila Asghari"

# Default parameters
DEFAULT_SAMPLING_RATE = 1000  # Hz
DEFAULT_DURATION = 2.0        # seconds
DEFAULT_FUNDAMENTAL_FREQ = 1  # Hz

# Signal types
SIGNAL_TYPES = [
    "Sine Wave",
    "Cosine Wave",
    "Square Wave",
    "Triangle Wave",
    "Sawtooth Wave",
    "Exponential Decay",
    "Unit Step",
    "Impulse",
    "Gaussian Pulse",
    "Custom Function"
]

# System types
SYSTEM_TYPES = [
    "Low-pass Filter",
    "High-pass Filter",
    "Band-pass Filter",
    "Moving Average",
    "Differentiator",
    "Integrator",
    "Custom System"
]

# Plot styles
PLOT_STYLES = {
    'time_domain': {'color': 'blue', 'linewidth': 1.5},
    'freq_domain': {'color': 'red', 'linewidth': 1.5},
    'magnitude': {'color': 'green', 'linewidth': 1.5},
    'phase': {'color': 'purple', 'linewidth': 1.5}
}