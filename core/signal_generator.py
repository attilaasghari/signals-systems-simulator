"""
Signal generation module for educational purposes
"""
import numpy as np
from scipy import signal as scipy_signal
from typing import Tuple, Optional, Callable

class SignalGenerator:
    """Generates various types of signals for educational demonstrations"""
    
    def __init__(self, fs: float = 1000, duration: float = 2.0):
        """
        Initialize signal generator
        
        Parameters:
        -----------
        fs : float
            Sampling frequency in Hz
        duration : float
            Signal duration in seconds
        """
        self.fs = fs
        self.duration = duration
        self.t = np.linspace(0, duration, int(fs * duration), endpoint=False)
        
    def generate(self, signal_type: str, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate a signal of specified type
        
        Parameters:
        -----------
        signal_type : str
            Type of signal to generate
        **kwargs : dict
            Signal-specific parameters
            
        Returns:
        --------
        t : np.ndarray
            Time vector
        x : np.ndarray
            Generated signal
        """
        # Set default parameters
        amplitude = kwargs.get('amplitude', 1.0)
        frequency = kwargs.get('frequency', 1.0)
        phase = kwargs.get('phase', 0.0)
        dc_offset = kwargs.get('dc_offset', 0.0)
        
        if signal_type == "Sine Wave":
            x = amplitude * np.sin(2 * np.pi * frequency * self.t + phase) + dc_offset
        elif signal_type == "Cosine Wave":
            x = amplitude * np.cos(2 * np.pi * frequency * self.t + phase) + dc_offset
        elif signal_type == "Square Wave":
            duty_cycle = kwargs.get('duty_cycle', 0.5)
            x = amplitude * scipy_signal.square(2 * np.pi * frequency * self.t + phase, duty=duty_cycle) + dc_offset
        elif signal_type == "Triangle Wave":
            width = kwargs.get('width', 0.5)
            x = amplitude * scipy_signal.sawtooth(2 * np.pi * frequency * self.t + phase, width=width) + dc_offset
        elif signal_type == "Sawtooth Wave":
            x = amplitude * scipy_signal.sawtooth(2 * np.pi * frequency * self.t + phase) + dc_offset
        elif signal_type == "Exponential Decay":
            decay_rate = kwargs.get('decay_rate', 1.0)
            x = amplitude * np.exp(-decay_rate * self.t) + dc_offset
        elif signal_type == "Unit Step":
            step_time = kwargs.get('step_time', 0.0)
            x = amplitude * (self.t >= step_time) + dc_offset
        elif signal_type == "Impulse":
            impulse_time = kwargs.get('impulse_time', 0.0)
            x = np.zeros_like(self.t)
            idx = np.argmin(np.abs(self.t - impulse_time))
            x[idx] = amplitude
        elif signal_type == "Gaussian Pulse":
            center = kwargs.get('center', self.duration/2)
            std_dev = kwargs.get('std_dev', 0.1)
            x = amplitude * np.exp(-0.5 * ((self.t - center) / std_dev)**2) + dc_offset
        elif signal_type == "Custom Function":
            func_str = kwargs.get('function', 'np.sin(2*np.pi*t)')
            try:
                # Safe evaluation with limited namespace
                safe_dict = {"np": np, "t": self.t, "__builtins__": {}}
                x = eval(func_str, safe_dict) + dc_offset
            except Exception as e:
                raise ValueError(f"Invalid custom function: {e}")
        else:
            raise ValueError(f"Unknown signal type: {signal_type}")
            
        return self.t.copy(), x
    
    def set_parameters(self, fs: Optional[float] = None, duration: Optional[float] = None):
        """Update generator parameters and regenerate time vector"""
        if fs is not None:
            self.fs = fs
        if duration is not None:
            self.duration = duration
        self.t = np.linspace(0, self.duration, int(self.fs * self.duration), endpoint=False)