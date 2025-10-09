"""
Transform implementations for signals and systems
"""
import numpy as np
from scipy import fft
from typing import Tuple

class FourierTransform:
    """Fourier Transform implementations"""
    
    @staticmethod
    def fft(signal: np.ndarray, fs: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute FFT of a signal
        
        Parameters:
        -----------
        signal : np.ndarray
            Input signal
        fs : float
            Sampling frequency
            
        Returns:
        --------
        freq : np.ndarray
            Frequency vector
        X : np.ndarray
            Complex FFT values
        """
        N = len(signal)
        X = fft.fft(signal)
        freq = fft.fftfreq(N, 1/fs)
        return freq, X
    
    @staticmethod
    def ifft(X: np.ndarray) -> np.ndarray:
        """Compute inverse FFT"""
        return fft.ifft(X).real

class LaplaceTransform:
    """Laplace Transform utilities (symbolic approach)"""
    
    @staticmethod
    def evaluate(s: complex, poles: list, zeros: list, gain: float = 1.0) -> complex:
        """
        Evaluate Laplace transform at a complex frequency s
        
        Parameters:
        -----------
        s : complex
            Complex frequency
        poles : list
            List of poles
        zeros : list
            List of zeros
        gain : float
            System gain
            
        Returns:
        --------
        H : complex
            Transfer function value at s
        """
        numerator = gain
        denominator = 1.0
        
        for zero in zeros:
            numerator *= (s - zero)
            
        for pole in poles:
            denominator *= (s - pole)
            
        return numerator / denominator

class ZTransform:
    """Z-Transform utilities"""
    
    @staticmethod
    def evaluate(z: complex, b: np.ndarray, a: np.ndarray) -> complex:
        """
        Evaluate Z-transform at a complex point z
        
        Parameters:
        -----------
        z : complex
            Complex point on z-plane
        b : np.ndarray
            Numerator coefficients
        a : np.ndarray
            Denominator coefficients
            
        Returns:
        --------
        H : complex
            Transfer function value at z
        """
        # Evaluate polynomial in z^{-1}
        num = np.sum(b * (z ** -np.arange(len(b))))
        den = np.sum(a * (z ** -np.arange(len(a))))
        return num / den