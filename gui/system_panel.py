"""
System analysis panel
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QComboBox, 
                             QDoubleSpinBox, QPushButton, QFormLayout, QLineEdit)
from PyQt5.QtCore import pyqtSignal
from core import SystemAnalyzer
from config import SYSTEM_TYPES, DEFAULT_SAMPLING_RATE

class SystemPanel(QWidget):
    """Panel for system analysis parameters"""
    system_updated = pyqtSignal(list, list)  # b, a coefficients
    
    def __init__(self):
        super().__init__()
        self.analyzer = SystemAnalyzer(DEFAULT_SAMPLING_RATE)
        self.init_ui()
        self.update_system()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # System type selection
        system_group = QGroupBox("System Type")
        system_layout = QVBoxLayout()
        self.system_type_combo = QComboBox()
        self.system_type_combo.addItems(SYSTEM_TYPES)
        self.system_type_combo.currentTextChanged.connect(self.on_system_type_changed)
        system_layout.addWidget(self.system_type_combo)
        system_group.setLayout(system_layout)
        layout.addWidget(system_group)
        
        # Parameters group
        self.params_group = QGroupBox("Parameters")
        self.params_layout = QFormLayout()
        self.params_widgets = {}
        self.setup_default_params()
        self.params_group.setLayout(self.params_layout)
        layout.addWidget(self.params_group)
        
        # Update button
        self.update_btn = QPushButton("Update System")
        self.update_btn.clicked.connect(self.update_system)
        layout.addWidget(self.update_btn)
        
        layout.addStretch()
        self.setLayout(layout)
        
    def setup_default_params(self):
        """Set up default parameters based on system type"""
        # Clear existing widgets
        for i in reversed(range(self.params_layout.count())):
            self.params_layout.itemAt(i).widget().setParent(None)
        self.params_widgets.clear()
        
        system_type = self.system_type_combo.currentText()
        
        if "Filter" in system_type:
            self.add_param("Cutoff Frequency (Hz)", 10.0, 0.1, 500.0)
            self.add_param("Order", 4, 1, 20, decimals=0)
            
        if system_type == "Band-pass Filter":
            self.add_param("Low Cutoff (Hz)", 5.0, 0.1, 500.0)
            self.add_param("High Cutoff (Hz)", 15.0, 0.1, 500.0)
            
        if system_type == "Moving Average":
            self.add_param("Window Size", 5, 1, 100, decimals=0)
            
        if system_type == "Custom System":
            self.add_custom_system_params()
            
    def add_param(self, name: str, default: float, min_val: float, max_val: float, decimals: int = 2):
        """Add a parameter spin box"""
        spin = QDoubleSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(default)
        spin.setDecimals(decimals)
        spin.valueChanged.connect(self.update_system)
        self.params_layout.addRow(name + ":", spin)
        self.params_widgets[name] = spin
        
    def add_custom_system_params(self):
        """Add custom system coefficient inputs"""
        # In a real implementation, you might use QLineEdit for array input
        # For simplicity, we'll use a placeholder
        from PyQt5.QtWidgets import QLabel
        label = QLabel("Use [1, 0.5] format for coefficients")
        self.params_layout.addRow("", label)
        
        num_edit = QLineEdit("[1]")
        num_edit.textChanged.connect(self.update_system)
        self.params_layout.addRow("Numerator:", num_edit)
        self.params_widgets["Numerator"] = num_edit
        
        den_edit = QLineEdit("[1, -0.5]")
        den_edit.textChanged.connect(self.update_system)
        self.params_layout.addRow("Denominator:", den_edit)
        self.params_widgets["Denominator"] = den_edit
        
    def on_system_type_changed(self):
        """Handle system type change"""
        self.setup_default_params()
        self.update_system()
        
    def update_system(self):
        """Create and emit system"""
        try:
            system_type = self.system_type_combo.currentText()
            kwargs = {}
            
            for name, widget in self.params_widgets.items():
                if isinstance(widget, QDoubleSpinBox):
                    kwargs[self._param_name_to_kwarg(name)] = widget.value()
                elif hasattr(widget, 'text'):
                    kwargs[self._param_name_to_kwarg(name)] = widget.text()
                    
            b, a = self.analyzer.create_system(system_type, **kwargs)
            self.system_updated.emit(b.tolist(), a.tolist())
        except Exception as e:
            # In a real app, show error message to user
            print(f"Error creating system: {e}")
            
    def _param_name_to_kwarg(self, name: str) -> str:
        """Convert parameter name to keyword argument"""
        mapping = {
            "Cutoff Frequency (Hz)": "cutoff",
            "Order": "order",
            "Low Cutoff (Hz)": "lowcut",
            "High Cutoff (Hz)": "highcut",
            "Window Size": "window_size",
            "Numerator": "numerator",
            "Denominator": "denominator"
        }
        return mapping.get(name, name.lower().replace(" ", "_").replace("(", "").replace(")", ""))