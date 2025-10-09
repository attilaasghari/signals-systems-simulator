"""
Plot panel for visualizing signals and systems
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from core import SystemAnalyzer, FourierTransform, utils
from config import PLOT_STYLES

class PlotPanel(QWidget):
    """Panel for plotting signals and system responses"""
    
    def __init__(self):
        super().__init__()
        self.analyzer = SystemAnalyzer()
        self.init_ui()
        self.input_signal = None
        self.system_b = None
        self.system_a = None
        
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
    def setup_plots(self):
        """Set up the initial plot structure"""
        # Create figure with subplots
        self.figure = Figure(figsize=(10, 8))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        
        # Create subplots
        self.ax_time = self.figure.add_subplot(2, 2, 1)
        self.ax_freq = self.figure.add_subplot(2, 2, 2)
        self.ax_response = self.figure.add_subplot(2, 2, 3)
        self.ax_pz = self.figure.add_subplot(2, 2, 4)
        
        self.update_plot_titles()
        self.canvas.draw()
        
    def update_plot_titles(self):
        """Update plot titles"""
        self.ax_time.set_title("Time Domain")
        self.ax_freq.set_title("Frequency Domain")
        self.ax_response.set_title("System Response")
        self.ax_pz.set_title("Pole-Zero Plot")
        
    def update_input_signal(self, t: np.ndarray, x: np.ndarray):
        """Update input signal plot"""
        self.input_signal = (t, x)
        self.plot_time_domain()
        self.plot_frequency_domain()
        
    def update_system_response(self, b: list, a: list):
        """Update system response plot"""
        self.system_b = np.array(b)
        self.system_a = np.array(a)
        self.plot_system_response()
        
    def update_frequency_response(self, b: list, a: list):
        """Update frequency response plot"""
        self.system_b = np.array(b)
        self.system_a = np.array(a)
        self.plot_frequency_response()
        
    def update_pole_zero_plot(self, b: list, a: list):
        """Update pole-zero plot"""
        self.system_b = np.array(b)
        self.system_a = np.array(a)
        self.plot_pole_zero()
        
    def plot_time_domain(self):
        """Plot time domain signal"""
        if self.input_signal is None:
            return
            
        self.ax_time.clear()
        t, x = self.input_signal
        self.ax_time.plot(t, x, **PLOT_STYLES['time_domain'])
        self.ax_time.set_xlabel("Time (s)")
        self.ax_time.set_ylabel("Amplitude")
        self.ax_time.grid(True)
        self.canvas.draw()
        
    def plot_frequency_domain(self):
        """Plot frequency domain representation"""
        if self.input_signal is None:
            return
            
        self.ax_freq.clear()
        t, x = self.input_signal
        fs = 1 / (t[1] - t[0]) if len(t) > 1 else 1000
        
        freq, X = FourierTransform.fft(x, fs)
        magnitude = np.abs(X)
        phase = np.angle(X)
        
        # Plot magnitude
        self.ax_freq.plot(freq, magnitude, **PLOT_STYLES['magnitude'])
        self.ax_freq.set_xlabel("Frequency (Hz)")
        self.ax_freq.set_ylabel("Magnitude")
        self.ax_freq.grid(True)
        self.canvas.draw()
        
    def plot_system_response(self):
        """Plot system impulse and step responses"""
        if self.system_b is None or self.system_a is None:
            return
            
        self.ax_response.clear()
        
        # Impulse response
        t_imp, h = self.analyzer.impulse_response(self.system_b, self.system_a)
        self.ax_response.plot(t_imp, h, label="Impulse Response", **PLOT_STYLES['time_domain'])
        
        # Step response
        t_step, s = self.analyzer.step_response(self.system_b, self.system_a)
        self.ax_response.plot(t_step, s, label="Step Response", **PLOT_STYLES['freq_domain'])
        
        self.ax_response.set_xlabel("Time (s)")
        self.ax_response.set_ylabel("Amplitude")
        self.ax_response.legend()
        self.ax_response.grid(True)
        self.canvas.draw()
        
    def plot_frequency_response(self):
        """Plot system frequency response"""
        if self.system_b is None or self.system_a is None:
            return
            
        # This would typically be plotted in the frequency domain subplot
        # For this example, we'll update the existing frequency plot
        w, h = self.analyzer.frequency_response(self.system_b, self.system_a)
        magnitude = np.abs(h)
        phase = np.angle(h)
        
        # We'll just update the magnitude for now
        self.ax_freq.clear()
        self.ax_freq.plot(w, magnitude, **PLOT_STYLES['magnitude'])
        self.ax_freq.set_xlabel("Frequency (Hz)")
        self.ax_freq.set_ylabel("Magnitude")
        self.ax_freq.grid(True)
        self.canvas.draw()
        
    def plot_pole_zero(self):
        """Plot pole-zero diagram"""
        if self.system_b is None or self.system_a is None:
            return
            
        self.ax_pz.clear()
        
        zeros, poles = utils.generate_pole_zero_plot(self.system_b, self.system_a)
        
        # Plot unit circle
        theta = np.linspace(0, 2*np.pi, 100)
        self.ax_pz.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.5)
        
        # Plot poles and zeros
        self.ax_pz.scatter(np.real(zeros), np.imag(zeros), 
                          s=100, marker='o', facecolors='none', 
                          edgecolors='blue', label='Zeros')
        self.ax_pz.scatter(np.real(poles), np.imag(poles), 
                          s=100, marker='x', color='red', label='Poles')
        
        self.ax_pz.set_xlabel("Real")
        self.ax_pz.set_ylabel("Imaginary")
        self.ax_pz.legend()
        self.ax_pz.grid(True)
        self.ax_pz.axis('equal')
        self.canvas.draw()