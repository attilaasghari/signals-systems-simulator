"""
Signal generation panel
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QComboBox, 
                             QDoubleSpinBox, QPushButton, QLabel, QFormLayout, 
                             QLineEdit)
from PyQt5.QtCore import pyqtSignal
import numpy as np
from core import SignalGenerator
from config import SIGNAL_TYPES, DEFAULT_SAMPLING_RATE, DEFAULT_DURATION

class SignalPanel(QWidget):
    """Panel for signal generation parameters"""
    signal_generated = pyqtSignal(np.ndarray, np.ndarray)  # t, x
    
    def __init__(self):
        super().__init__()
        self.generator = SignalGenerator(DEFAULT_SAMPLING_RATE, DEFAULT_DURATION)
        self.init_ui()
        self.update_signal()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Signal type selection
        signal_group = QGroupBox("Signal Type")
        signal_layout = QVBoxLayout()
        self.signal_type_combo = QComboBox()
        self.signal_type_combo.addItems(SIGNAL_TYPES)
        self.signal_type_combo.currentTextChanged.connect(self.on_signal_type_changed)
        signal_layout.addWidget(self.signal_type_combo)
        signal_group.setLayout(signal_layout)
        layout.addWidget(signal_group)
        
        # Parameters group
        self.params_group = QGroupBox("Parameters")
        self.params_layout = QFormLayout()
        self.params_widgets = {}
        self.setup_default_params()
        self.params_group.setLayout(self.params_layout)
        layout.addWidget(self.params_group)
        
        # Generate button
        self.generate_btn = QPushButton("Generate Signal")
        self.generate_btn.clicked.connect(self.update_signal)
        layout.addWidget(self.generate_btn)
        
        # Global parameters
        global_group = QGroupBox("Global Parameters")
        global_layout = QFormLayout()
        
        self.fs_spin = QDoubleSpinBox()
        self.fs_spin.setRange(1, 100000)
        self.fs_spin.setValue(DEFAULT_SAMPLING_RATE)
        self.fs_spin.setSuffix(" Hz")
        self.fs_spin.valueChanged.connect(self.on_global_params_changed)
        global_layout.addRow("Sampling Rate:", self.fs_spin)
        
        self.duration_spin = QDoubleSpinBox()
        self.duration_spin.setRange(0.01, 100)
        self.duration_spin.setValue(DEFAULT_DURATION)
        self.duration_spin.setSuffix(" s")
        self.duration_spin.valueChanged.connect(self.on_global_params_changed)
        global_layout.addRow("Duration:", self.duration_spin)
        
        global_group.setLayout(global_layout)
        layout.addWidget(global_group)
        
        layout.addStretch()
        self.setLayout(layout)
        
    def setup_default_params(self):
        """Set up default parameters based on signal type"""
        # Clear existing widgets
        for i in reversed(range(self.params_layout.count())):
            self.params_layout.itemAt(i).widget().setParent(None)
        self.params_widgets.clear()
        
        signal_type = self.signal_type_combo.currentText()
        
        # Common parameters
        self.add_param("Amplitude", 1.0, 0.0, 100.0)
        self.add_param("DC Offset", 0.0, -100.0, 100.0)
        
        if "Wave" in signal_type or signal_type in ["Exponential Decay", "Gaussian Pulse"]:
            self.add_param("Frequency (Hz)", 1.0, 0.0, 1000.0)
            self.add_param("Phase (rad)", 0.0, -2*np.pi, 2*np.pi)
            
        if signal_type == "Square Wave":
            self.add_param("Duty Cycle", 0.5, 0.0, 1.0)
        elif signal_type == "Triangle Wave":
            self.add_param("Width", 0.5, 0.0, 1.0)
        elif signal_type == "Exponential Decay":
            self.add_param("Decay Rate", 1.0, 0.0, 100.0)
        elif signal_type == "Unit Step":
            self.add_param("Step Time (s)", 0.0, 0.0, DEFAULT_DURATION)
        elif signal_type == "Impulse":
            self.add_param("Impulse Time (s)", 0.0, 0.0, DEFAULT_DURATION)
        elif signal_type == "Gaussian Pulse":
            self.add_param("Center (s)", DEFAULT_DURATION/2, 0.0, DEFAULT_DURATION)
            self.add_param("Std Dev (s)", 0.1, 0.001, DEFAULT_DURATION)
        elif signal_type == "Custom Function":
            self.add_custom_function_param()
            
    def add_param(self, name: str, default: float, min_val: float, max_val: float):
        """Add a parameter spin box"""
        spin = QDoubleSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(default)
        spin.valueChanged.connect(self.update_signal)
        self.params_layout.addRow(name + ":", spin)
        self.params_widgets[name] = spin
        
    def add_custom_function_param(self):
        """Add custom function input"""
        line_edit = QLineEdit("np.sin(2*np.pi*t)")
        line_edit.textChanged.connect(self.update_signal)
        self.params_layout.addRow("Function:", line_edit)
        self.params_widgets["Function"] = line_edit
        
    def on_signal_type_changed(self):
        """Handle signal type change"""
        self.setup_default_params()
        self.update_signal()
        
    def on_global_params_changed(self):
        """Handle global parameter changes"""
        self.generator.set_parameters(
            fs=self.fs_spin.value(),
            duration=self.duration_spin.value()
        )
        self.update_signal()
        
    def update_signal(self):
        """Generate and emit signal"""
        try:
            signal_type = self.signal_type_combo.currentText()
            kwargs = {}
            
            for name, widget in self.params_widgets.items():
                if isinstance(widget, QDoubleSpinBox):
                    kwargs[self._param_name_to_kwarg(name)] = widget.value()
                elif isinstance(widget, QLineEdit):
                    kwargs['function'] = widget.text()
                    
            t, x = self.generator.generate(signal_type, **kwargs)
            self.signal_generated.emit(t, x)
        except Exception as e:
            # In a real app, show error message to user
            print(f"Error generating signal: {e}")
            
    def _param_name_to_kwarg(self, name: str) -> str:
        """Convert parameter name to keyword argument"""
        mapping = {
            "Amplitude": "amplitude",
            "DC Offset": "dc_offset",
            "Frequency (Hz)": "frequency",
            "Phase (rad)": "phase",
            "Duty Cycle": "duty_cycle",
            "Width": "width",
            "Decay Rate": "decay_rate",
            "Step Time (s)": "step_time",
            "Impulse Time (s)": "impulse_time",
            "Center (s)": "center",
            "Std Dev (s)": "std_dev"
        }
        return mapping.get(name, name.lower().replace(" ", "_").replace("(", "").replace(")", ""))