# 📡 Signals and Systems Simulator

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

A comprehensive, interactive educational tool for **computer engineering** and **electronic engineering** students studying **Signals and Systems**. Visualize signals, analyze LTI systems, and explore transforms in both time and frequency domains.

---

## 🌟 Features

### Signal Generation
- **Standard signals**: Sine, cosine, square, triangle, sawtooth waves
- **Special signals**: Unit step, impulse, exponential decay, Gaussian pulse
- **Custom functions**: Define your own mathematical expressions
- **Real-time parameter adjustment**: Instantly see changes in signal properties

### System Analysis
- **Filter types**: Low-pass, high-pass, band-pass (Butterworth)
- **Basic systems**: Moving average, differentiator, integrator
- **Custom systems**: Define transfer functions with numerator/denominator coefficients
- **Stable approximations**: Proper implementations of ideal operations

### Visualization
- **Time domain**: Input signal and system responses
- **Frequency domain**: Magnitude and phase spectra via FFT
- **System responses**: Impulse and step responses
- **Pole-zero plots**: Analyze system stability and characteristics
- **Interactive plots**: Zoom, pan, and export capabilities

### Educational Focus
- Designed specifically for **signals and systems coursework**
- Demonstrates key concepts: sampling, filtering, stability, transforms
- Safe environment for experimentation without mathematical errors
- Immediate visual feedback reinforces theoretical understanding

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation
```bash
# Clone the repository
git clone https://github.com/attilaasghari/signals-systems-simulator.git
cd signals-systems-simulator

# Install dependencies
pip install -r requirements.txt
```

### Run from Source
```bash
python main.py
```

### Build Standalone Executable
```bash
pyinstaller --onefile --windowed --name="SignalsSystemsSimulator" main.py
---

## 📂 Project Structure

```
signals-systems-simulator/
├── main.py                 # Application entry point
├── setup.py                # Build and distribution script
├── requirements.txt        # Dependencies
├── README.md               # This file
├── LICENSE                 # MIT License
│
├── core/                   # Signal processing algorithms
│   ├── signal_generator.py # Signal creation utilities
│   ├── system_analyzer.py  # LTI system analysis
│   ├── transform.py        # Fourier, Laplace, Z-transforms
│   └── utils.py            # Helper functions
│
├── gui/                    # Graphical user interface
│   ├── main_window.py      # Main application window
│   ├── signal_panel.py     # Signal generation controls
│   ├── system_panel.py     # System analysis controls
│   └── plot_panel.py       # Visualization components
│
└── config/                 # Application configuration
    └── __init__.py         # Constants and settings
```

---

## 🎓 Educational Applications

### Classroom Demonstrations
- **Fourier Transform**: Show how time-domain signals correspond to frequency spectra
- **Filter Design**: Visualize the effects of different filter types and orders
- **System Stability**: Use pole-zero plots to demonstrate stability criteria
- **Sampling Theory**: Illustrate aliasing and reconstruction concepts

### Student Self-Study
- **Experiment safely**: Test hypotheses without complex mathematical setup
- **Visual learning**: Reinforce abstract concepts with concrete visualizations
- **Homework verification**: Check analytical solutions against numerical results
- **Project development**: Build custom signal processing chains

### Key Concepts Covered
- Continuous and discrete-time signals
- Linear Time-Invariant (LTI) systems
- Convolution and system responses
- Frequency domain analysis
- Filter design and implementation
- Stability and causality
- Sampling and reconstruction

---

## 🛠️ Technical Details

### Dependencies
- **NumPy**: Numerical computing foundation
- **SciPy**: Signal processing and scientific algorithms
- **Matplotlib**: High-quality 2D plotting
- **PyQt5**: Cross-platform GUI framework

### Design Principles
- **Modular architecture**: Clear separation between core algorithms and GUI
- **Educational accuracy**: Mathematically correct implementations
- **Numerical robustness**: Handles edge cases and improper systems gracefully
- **User-friendly interface**: Intuitive controls with immediate feedback
- **Cross-platform compatibility**: Works on Windows, macOS, and Linux

### Safety Features
- Input validation prevents common student errors
- Stable approximations replace non-realizable ideal systems
- Warning suppression for educational clarity
- Graceful error handling with meaningful messages

---

## 📸 Screenshots

*(Add screenshots of your application here showing:)*
- Signal generation panel with sine wave
- System analysis panel with low-pass filter
- Four-panel visualization (time domain, frequency domain, system response, pole-zero plot)
- Custom function input example

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Improvement
- Add Laplace transform visualization
- Implement convolution demonstrations
- Add sampling and reconstruction examples
- Include noise addition and SNR analysis
- Support export to CSV/PNG for reports
- Add tutorial mode for beginners

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---

## 🙏 Acknowledgments

- Built with [NumPy](https://numpy.org/), [SciPy](https://scipy.org/), [Matplotlib](https://matplotlib.org/), and [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
- Inspired by classic signals and systems textbooks by Oppenheim, Willsky, and Nawab
- Educational design informed by engineering pedagogy best practices

---

## 📧 Contact

For questions, suggestions, or bug reports:
- **Email**: attilaasghari@gmail.com
- **Issue Tracker**: [GitHub Issues](https://github.com/attilaasghari/signals-systems-simulator/issues)

---

*Empowering the next generation of engineers through interactive learning.* 🚀