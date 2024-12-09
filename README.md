# Quantum Key Distribution

This project is a Quantum Key Distribution (QKD) Simulator that demonstrates secure communication protocols based on the principles of quantum mechanics. The application provides simulations for two well-known QKD protocols: the BB84 Protocol and the E91 Protocol. It includes a visually appealing landing page built with HTML and an interactive simulator powered by Streamlit.
![image](https://github.com/user-attachments/assets/c0ab161a-f195-4518-8bf0-ec84543f6e35)



---

## Features

1. **Landing Page:**
   - Built with HTML.
   - Responsive design with gradient backgrounds and interactive hover effects.
   - Provides an introduction to quantum cryptography and the protocols simulated.

2. **QKD Simulation:**
   - **BB84 Protocol:**
     - Simulates the generation and transmission of quantum keys.
     - Detects eavesdropping based on mismatched bases.
     - Displays shared keys, matched bases, and error rates.
   - **E91 Protocol:**
     - Uses quantum entanglement for secure key distribution.
     - Detects eavesdropping through violations of quantum correlations.
   - Customizable parameters such as the number of qubits and random seed.

3. **Performance Metrics:**
   - Displays execution time, matched bases, shared key length, and channel security status.

4. **User-Friendly Interface:**
   - Interactive Streamlit-based UI.
   - Tabs and visual elements for detailed protocol insights.

---

## Installation and Setup

### Prerequisites
Ensure you have the following installed:
- Python 3.8 or later
- Streamlit
- Tailwind CSS (for local HTML edits, if required)
- FontAwesome (for icons in the landing page)

### Installation

1. Install required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

2. Launch the Streamlit app:
   ```bash
   streamlit run quantum.py
   ```

3. Open the `index.html` page in a browser for the landing page:
   ```bash
   python -m http.server 8000
   ```
   Navigate to `http://localhost:8000` in your browser.

4 . Connect the landing page to the Streamlit app by updating the "Let's Get Started" button link in `index.html` to point to your Streamlit app URL (default: `http://localhost:8501`).

---

## Usage
1. Open the landing page to learn about QKD protocols.
2. Click "Let's Get Started" to navigate to the simulator.
3. Use the sidebar in the simulator to:
   - Select a protocol (BB84 or E91).
   - Adjust the number of qubits and set a random seed for reproducibility.
4. Click "Run Quantum Simulation" to view results.
5. Explore detailed results, including bits, bases, matched bases, and shared keys.

---

## File Structure

```plaintext
quantum-key-distribution-simulator/
├── index.html         # Landing page (HTML/Tailwind CSS)
├── quantum.py         # Streamlit app for QKD simulation
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

---

## Technologies Used

- **Python:** Backend for simulations.
- **Streamlit:** Interactive UI for the simulator.
- **HTML:** Landing page design.
- **NumPy:** Quantum protocol simulations and random number generation.

---



