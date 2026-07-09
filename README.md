# Fisiologia 🧠❤️🫁

**Human physiology can be cool** – Teaching materials and interactive simulations for understanding human physiological systems.

This repository contains a comprehensive web application built with **Shiny for Python** that provides interactive educational simulations and visualizations of key physiological concepts, including action potentials, cardiac function, respiratory mechanics, running biomechanics, and gait analysis.

---

## 🎯 Features

### 📊 Interactive Pages

#### **Action Potential**
Explore how different tissue types generate electrical signals:
- **Static Comparison**: Visualize action potentials across cardiac muscle, neurons, and skeletal muscle with customizable time windows
- **Interactive Animation**: Generate and animate neuronal action potentials at different stimulus levels
  - Sub-threshold stimulation (-60 mV)
  - Above-threshold stimulation (-40 mV, +10 mV)
  - Real-time threshold visualization

**Key Physiological Details:**
- **Cardiac**: Long plateau phase (200-300ms) preventing tetanic contractions
- **Neuronal**: Rapid signals (1-2ms) enabling high-frequency firing
- **Skeletal**: Intermediate duration (2-5ms) for muscle fiber propagation

#### **Heart Rate (ECG Simulation)**
Simulate and analyze cardiac electrical activity:
- Customizable heart rate (30-230 bpm)
- Heart Rate Variability (HRV) via SDNN parameter (0-100 ms)
- Adjustable time windows for signal analysis
- Real-time statistics including RMSSD calculations

**Advanced Model**: Uses autocorrelated noise to realistically model HRV:
$$RMSSD \approx \sqrt{2 \cdot SDNN^2 \cdot (1 - r_1)}$$
where r = 0.80 (based on literature)

#### **Ventilation (Respiration Simulator)**
Model respiratory mechanics:
- Adjustable respiratory frequency (0-70 bpm)
- Customizable tidal volume (0-3 L)
- Flexible time windows (10-60 seconds)
- Real-time minute ventilation calculations

#### **Running Simulation**
Interactive biomechanics and metabolism simulator:
- Explore relationships between running parameters and physiological responses
- Access custom-built web app: [TreadmillRunSimulator](https://danilobondi.github.io/TreadmillRunSimulator)

#### **Gait Analysis**
Analyze human walking mechanics:
- Process IMU sensor data (tri-axial accelerometer + gyroscope)
- Integrated analysis from Microgate GyrkoPro or any compatible sensor
- Generate comprehensive PDF reports
- Access the tool: [GaitAnalysis](https://danilobondi.github.io/GaitAnalysis)

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Required Packages
- **shiny**: Web framework for interactive Python applications
- **numpy**: Numerical computations and signal processing
- **plotly**: Interactive data visualization

### Run the Application

```bash
shiny run app.py
```

The application will be available at `http://localhost:8000`

---

## 📁 Project Structure

```
Fisiologia/
├── app.py                    # Main Shiny application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── LICENSE                   # AGPL-3.0 License
├── .gitignore               # Git ignore rules
├── AI.png                   # Credits visualization
├── Leonardo.png             # Historical reference image
├── Health care.lottie       # Animated healthcare icon
├── Marathon.lottie          # Running animation
├── Walking robot.lottie     # Gait animation
├── lung.lottie              # Respiratory system animation
└── working brain.lottie     # Brain activity animation
```

---

## 🛠️ Technology Stack

- **Backend**: Python with Shiny for Python framework
- **Data Visualization**: Plotly (interactive charts)
- **Numerical Computing**: NumPy (signal generation and processing)
- **Animations**: Lottie animations for visual engagement
- **Styling**: Custom CSS with responsive design
- **Math Rendering**: MathJax for LaTeX equations

---

## 📚 Educational Content

### Physiological Simulations

1. **Electrophysiology**: Generation and propagation of action potentials
2. **Cardiology**: ECG signal interpretation and HRV analysis
3. **Respiratory Physiology**: Breathing mechanics and ventilation modeling
4. **Biomechanics**: Running mechanics and gait analysis
5. **Signal Processing**: Real-time signal generation and analysis

### Use Cases

- University physiology courses
- Medical education and training
- Research in exercise physiology
- Biomechanics analysis
- Interactive learning materials

---

## 🤝 Credits

- [GitHub](https://github.com) – Version control and hosting
- [Shiny for Python](https://shiny.posit.co/py/) – Web framework
- [Google Gemini](https://gemini.google.com) – AI assistance
- [OpenAI ChatGPT](https://chatgpt.com) – AI assistance
- [LottieFiles](https://lottiefiles.com) – Animations
- [Plotly](https://plotly.com/) – Interactive visualizations

---

## 📝 License

This project is licensed under the **GNU Affero General Public License v3.0** (AGPL-3.0).

See [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Danilo Bondi**

Developed and curated with the assistance of AI technologies to create engaging educational tools for human physiology.

---

## 🌟 Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/DaniloBondi/Fisiologia.git
   cd Fisiologia
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   shiny run app.py
   ```

4. **Open in browser**:
   Navigate to `http://localhost:8000` and explore the interactive simulations!

---

## 💡 Tips for Learning

- **Start with Action Potential**: Understand the basic principles of electrical signaling
- **Explore Variability**: Use the HRV controls to understand heart rate variability concepts
- **Experiment with Parameters**: Modify respiratory rate and tidal volume to see their effects on minute ventilation
- **Compare Tissues**: Switch between different tissue types to observe physiological differences
- **Analyze Animations**: Use play/pause controls to study detailed action potential dynamics

---

## 🔬 For Researchers

This application can be extended for research purposes:
- Custom signal processing algorithms
- Integration with real sensor data
- Statistical analysis tools
- Data export capabilities
- Multi-subject comparative analysis

---

## 📧 Contact & Support

For questions, suggestions, or contributions, please reach out through GitHub Issues or contact the author directly.

---

**Happy learning! Explore the fascinating world of human physiology.** 🧬
