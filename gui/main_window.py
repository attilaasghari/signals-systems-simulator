"""
Main application window
"""
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, 
                             QVBoxLayout, QWidget, QSplitter, QFrame)
from PyQt5.QtCore import Qt
from .signal_panel import SignalPanel
from .system_panel import SystemPanel
from .plot_panel import PlotPanel

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signals and Systems Simulator")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # Create left panel container (Signal + System stacked vertically)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(5)
        
        self.signal_panel = SignalPanel()
        self.system_panel = SystemPanel()
        
        left_layout.addWidget(self.signal_panel)
        left_layout.addWidget(self.system_panel)
        left_layout.addStretch()  # Push panels to top
        
        # Create plot panel
        self.plot_panel = PlotPanel()
        
        # Create horizontal splitter: left (controls) | right (plots)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(self.plot_panel)
        
        # Set initial sizes: 30% for controls, 70% for plots
        splitter.setSizes([350, 850])
        
        main_layout.addWidget(splitter)
        
        # Connect signals
        self.signal_panel.signal_generated.connect(self.plot_panel.update_input_signal)
        self.system_panel.system_updated.connect(self.plot_panel.update_system_response)
        self.system_panel.system_updated.connect(self.plot_panel.update_frequency_response)
        self.system_panel.system_updated.connect(self.plot_panel.update_pole_zero_plot)
        
        # Initial plot setup
        self.plot_panel.setup_plots()