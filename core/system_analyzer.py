"""
System analysis module for LTI systems
"""
import numpy as np
from scipy import signal as scipy_signal
from typing import Tuple, Optional

class SystemAnalyzer:
    """Analyzes LTI systems and their responses"""
    
    def __init__(self, fs: float = 1000):
        self.fs = fs
        
    def create_system(self, system_type: str, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create system representation (numerator and denominator coefficients)
        
        Parameters:
        -----------
        system_type : str
            Type of system to create
        **kwargs : dict
            System-specific parameters
            
        Returns:
        --------
        b : np.ndarray
            Numerator coefficients
        a : np.ndarray
            Denominator coefficients
        """
        if system_type == "Low-pass Filter":
            cutoff = kwargs.get('cutoff', 10.0)
            order = int(kwargs.get('order', 4))
            nyquist = self.fs / 2
            if cutoff >= nyquist:
                cutoff = nyquist * 0.99  # Avoid Nyquist limit
            normalized_cutoff = cutoff / nyquist
            b, a = scipy_signal.butter(order, normalized_cutoff, btype='low', analog=False)
        elif system_type == "High-pass Filter":
            cutoff = kwargs.get('cutoff', 10.0)
            order = int(kwargs.get('order', 4))
            nyquist = self.fs / 2
            if cutoff <= 0:
                cutoff = 1.0
            if cutoff >= nyquist:
                cutoff = nyquist * 0.99
            normalized_cutoff = cutoff / nyquist
            b, a = scipy_signal.butter(order, normalized_cutoff, btype='high', analog=False)
        elif system_type == "Band-pass Filter":
            lowcut = kwargs.get('lowcut', 5.0)
            highcut = kwargs.get('highcut', 15.0)
            order = int(kwargs.get('order', 4))
            nyquist = self.fs / 2
            # Ensure valid band
            lowcut = max(lowcut, 0.1)
            highcut = min(highcut, nyquist * 0.99)
            if lowcut >= highcut:
                lowcut, highcut = 5.0, 15.0  # fallback
            low = lowcut / nyquist
            high = highcut / nyquist
            b, a = scipy_signal.butter(order, [low, high], btype='band', analog=False)
        elif system_type == "Moving Average":
            window_size = int(kwargs.get('window_size', 5))
            if window_size < 1:
                window_size = 1
            b = np.ones(window_size) / window_size
            a = np.array([1.0])
        elif system_type == "Differentiator":
            # Proper, stable approximation: H(z) = (1 - z^{-1}) / (1 - alpha*z^{-1})
            alpha = float(kwargs.get('alpha', 0.95))
            alpha = np.clip(alpha, 0.0, 0.999)  # Ensure stability
            b = np.array([1.0, -1.0])
            a = np.array([1.0, -alpha])
        elif system_type == "Integrator":
            # Leaky integrator for numerical stability: H(z) = 1 / (1 - beta*z^{-1})
            beta = float(kwargs.get('beta', 0.99))
            beta = np.clip(beta, 0.0, 0.9999)
            b = np.array([1.0])
            a = np.array([1.0, -beta])
        elif system_type == "Custom System":
            b_str = kwargs.get('numerator', '[1]')
            a_str = kwargs.get('denominator', '[1]')
            try:
                # Safe evaluation with restricted namespace
                safe_dict = {"np": np, "__builtins__": {}}
                b = np.array(eval(b_str, safe_dict))
                a = np.array(eval(a_str, safe_dict))
                
                if b.size == 0 or a.size == 0:
                    raise ValueError("Empty coefficient array")
                
                # Remove leading zeros (normalize)
                b_trimmed = np.trim_zeros(b, 'f')
                a_trimmed = np.trim_zeros(a, 'f')
                b = b_trimmed if b_trimmed.size > 0 else np.array([0.0])
                a = a_trimmed if a_trimmed.size > 0 else np.array([1.0])
                
                # Ensure a[0] is not zero
                if abs(a[0]) < 1e-12:
                    raise ValueError("Leading denominator coefficient cannot be zero")
                    
            except Exception as e:
                raise ValueError(f"Invalid system coefficients: {e}")
        else:
            raise ValueError(f"Unknown system type: {system_type}")
            
        return b, a
    
    def impulse_response(self, b: np.ndarray, a: np.ndarray, 
                        t: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Compute impulse response of the system"""
        if t is None:
            t = np.linspace(0, 2.0, int(2.0 * self.fs), endpoint=False)
        
        # Handle static gain (no dynamics)
        if len(a) == 1 and len(b) == 1:
            h = np.zeros_like(t)
            h[0] = b[0] / a[0]
            return t, h

        # For improper systems (len(b) > len(a)), use lfilter directly
        if len(b) > len(a):
            N = len(t)
            impulse = np.zeros(N)
            impulse[0] = 1.0
            h = scipy_signal.lfilter(b, a, impulse)
            return t, h
        else:
            # Proper system: try dimpulse first
            try:
                system = scipy_signal.dlti(b, a, dt=1/self.fs)
                t_out, h = scipy_signal.dimpulse(system, t=t)
                return t_out, np.squeeze(h)
            except Exception:
                # Fallback to lfilter if dimpulse fails
                N = len(t)
                impulse = np.zeros(N)
                impulse[0] = 1.0
                h = scipy_signal.lfilter(b, a, impulse)
                return t, h
    
    def step_response(self, b: np.ndarray, a: np.ndarray, 
                     t: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Compute step response of the system"""
        if t is None:
            t = np.linspace(0, 2.0, int(2.0 * self.fs), endpoint=False)
        
        # Handle static gain
        if len(a) == 1 and len(b) == 1:
            step_val = b[0] / a[0]
            return t, np.full_like(t, step_val)

        # For improper systems, use lfilter with step input
        if len(b) > len(a):
            N = len(t)
            step_input = np.ones(N)
            s = scipy_signal.lfilter(b, a, step_input)
            return t, s
        else:
            try:
                system = scipy_signal.dlti(b, a, dt=1/self.fs)
                t_out, s = scipy_signal.dstep(system, t=t)
                return t_out, np.squeeze(s)
            except Exception:
                # Fallback
                N = len(t)
                step_input = np.ones(N)
                s = scipy_signal.lfilter(b, a, step_input)
                return t, s
    
    def frequency_response(self, b: np.ndarray, a: np.ndarray, 
                          n_points: int = 1024) -> Tuple[np.ndarray, np.ndarray]:
        """Compute frequency response of the system"""
        try:
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                w, h = scipy_signal.freqz(b, a, worN=n_points, fs=self.fs)
            # Replace NaNs/Infs with zeros for plotting
            h = np.nan_to_num(h, nan=0.0, posinf=0.0, neginf=0.0)
            return w, h
        except Exception as e:
            # Fallback: return zeros if freqz fails completely
            w = np.linspace(0, self.fs/2, n_points//2 + 1)
            h = np.zeros_like(w, dtype=complex)
            return w, h
    
    def apply_system(self, b: np.ndarray, a: np.ndarray, 
                    input_signal: np.ndarray) -> np.ndarray:
        """Apply system to input signal"""
        if len(input_signal) == 0:
            return np.array([])
        return scipy_signal.lfilter(b, a, input_signal)