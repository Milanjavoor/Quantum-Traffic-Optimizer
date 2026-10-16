# Quantum Traffic Optimizer

A Quantum Computing–Based Traffic Signal Optimization System Using Qiskit, Flask, HTML, and CSS

## Overview

The **Quantum Traffic Optimizer** is a web-based simulation project that explores how quantum computing techniques can be applied to traffic signal scheduling at a four-way intersection.

Traditional traffic signals often operate using fixed timings, which may not adapt well to changing traffic conditions. This project introduces a quantum circuit-based approach that uses traffic density inputs to generate candidate signal schedules and evaluate their suitability using a traffic allocation objective.

Users enter the number of waiting vehicles in the North, South, East, and West directions. The Flask backend validates these inputs, calculates the relative traffic demand, constructs a four-qubit quantum circuit, and executes it using Qiskit Aer. The measured outcomes represent candidate signal schedules, which can then be evaluated to select a suitable green-light allocation.

The project combines quantum circuit simulation, classical optimization logic, and a web-based user interface into one practical learning application.

**Project type:** Quantum Computing, Quantum Optimization, Web Development  
**Primary language:** Python  
**Quantum framework:** Qiskit  
**Simulation engine:** Qiskit Aer  
**Web framework:** Flask

---

## Problem Statement

Traffic congestion is a major challenge in urban transportation systems. Fixed-time traffic signals allocate a predetermined amount of green-light time to each direction, regardless of the current traffic demand.

This can result in:

- Longer waiting times for vehicles in congested directions.
- Inefficient utilization of available green-light time.
- Unnecessary delays when traffic is unevenly distributed.
- Limited flexibility in adapting signal timings to changing traffic conditions.

The Quantum Traffic Optimizer explores an alternative approach in which traffic density influences the generation and evaluation of possible signal schedules.

The objective is to demonstrate how quantum circuit sampling can be integrated with classical traffic optimization logic to explore different signal timing allocations.

## Project Objectives

1. Accept traffic density inputs for all four directions of an intersection.
2. Validate user inputs to prevent invalid traffic values.
3. Calculate the relative demand of the North–South and East–West phases.
4. Construct a four-qubit quantum circuit whose measurement probabilities depend on traffic demand.
5. Simulate the circuit using Qiskit Aer.
6. Convert measurement outcomes into candidate green-light allocations.
7. Evaluate candidate schedules using a traffic-related objective function.
8. Display the resulting schedule through a web interface built with Flask, HTML, and CSS.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic and traffic calculations |
| Qiskit | Construction and manipulation of quantum circuits |
| Qiskit Aer | Local simulation of quantum circuit execution |
| Flask | Backend routing, request handling, and HTML rendering |
| HTML5 | Structure of the web interface |
| CSS3 | Styling and layout of the interface |
| Jinja2 | Rendering dynamic values inside HTML templates |
| NumPy / Python mathematics | Mathematical calculations, where applicable |

The core quantum and traffic calculations are implemented in Python, while Flask connects those calculations to the frontend.

## System Architecture

The application follows a simple request-processing architecture.

```text
                 USER
                   |
                   v
          HTML / CSS Interface
                   |
                   v
             Flask Backend
                   |
                   v
          Input Validation
                   |
                   v
          Traffic Demand Model
                   |
                   v
         Quantum Circuit Builder
                   |
                   v
            Qiskit Aer
          Quantum Simulation
                   |
                   v
         Measurement Outcomes
                   |
                   v
        Candidate Schedule Mapping
                   |
                   v
        Classical Schedule Scoring
                   |
                   v
          Best Candidate Schedule
                   |
                   v
           Results on Webpage
```

### Architecture Components

**1. Frontend**

The frontend provides input fields for traffic densities in the four directions. Users submit the values through an HTML form, and the resulting signal allocation can be displayed on the webpage.

**2. Flask Backend**

Flask receives form submissions, validates the inputs, executes the traffic optimization workflow, and passes results to the HTML template using Jinja2.

**3. Traffic Demand Calculation**

The application calculates the fraction of traffic belonging to the North–South phase relative to the total traffic at the intersection.

**4. Quantum Circuit Construction**

A four-qubit quantum circuit is created using Hadamard and Z-rotation gates. The rotation angle is derived from the North–South traffic demand share.

**5. Quantum Simulation**

Qiskit Aer executes the circuit repeatedly. The measured bitstrings and their frequencies provide a distribution of candidate outcomes.

**6. Classical Schedule Evaluation**

Each candidate is mapped to a green-light allocation. A traffic objective function evaluates these allocations, and the best-scoring candidate is selected.

**7. Result Rendering**

The selected schedule and associated traffic information are passed back to the frontend for display.

---

## How the Quantum Circuit Works

The project uses a quantum circuit containing four qubits and four classical bits.

Four qubits produce \(2^4=16\) possible measurement outcomes. These outcomes can be represented as four-bit binary strings or integers from 0 to 15.

Examples include:

| Binary outcome | Integer candidate |
|---|---:|
| `0000` | 0 |
| `0001` | 1 |
| `0101` | 5 |
| `1000` | 8 |
| `1111` | 15 |

Each qubit is prepared using the following sequence:

```text
H → RZ(θ) → H → Measurement
```

### Hadamard Gate

The Hadamard gate, represented by `H`, creates a superposition of computational basis states when applied to a qubit initially in the state \(|0\rangle\).

### RZ Rotation Gate

The `RZ(θ)` gate rotates the qubit's phase around the Z axis. When combined with the two Hadamard gates, it controls the final probability of measuring the qubit as 0 or 1.

### Traffic-Dependent Rotation

Let \(p\) represent the proportion of traffic belonging to the North–South phase:

\[
p=\frac{N+S}{N+S+E+W}
\]

where \(N,S,E,W\) denote the traffic counts in the four directions.

When the total traffic is zero, the implementation uses \(p=0.5\) as a neutral fallback.

The rotation angle is calculated as:

\[
\theta=2\arcsin(\sqrt{p})
\]

For the gate sequence used in this project, the probability of measuring a single qubit as 1 is:

\[
P(1)=\sin^2\left(\frac{\theta}{2}\right)=p
\]

Consequently, the North–South traffic share influences the probability distribution of the measured bitstrings.

Because the qubits are prepared independently in this circuit, their outcomes are sampled independently with the same single-qubit probability.

### Quantum Measurement

The circuit is executed using Qiskit Aer with 1,024 measurement shots.

Repeated measurements produce a histogram of possible outcomes. The application can use these counts to examine the generated candidate schedules.

**Important:** Quantum measurement generates candidate schedules; it does not inherently determine which schedule minimizes congestion. The classical scoring function is responsible for evaluating and ranking the candidates.

---

## Traffic Signal Allocation

The model assumes a total signal cycle of 60 seconds divided between two phases:

- North–South phase
- East–West phase

Each phase receives a minimum of 10 seconds.

Therefore, the flexible green time is:

\[
T_{\text{flex}}=60-2(10)=40\text{ seconds}
\]

A candidate \(k\), where \(k\in\{0,1,\ldots,15\}\), is mapped to the North–South green time using:

\[
G_{NS}=10+
\operatorname{round}\left(\frac{k}{15}\times40\right)
\]

The East–West green time is then calculated as:

\[
G_{EW}=60-G_{NS}
\]

Example allocations:

| Candidate | North–South green | East–West green |
|---:|---:|---:|
| 0 | 10 seconds | 50 seconds |
| 4 | 21 seconds | 39 seconds |
| 8 | 31 seconds | 29 seconds |
| 12 | 42 seconds | 18 seconds |
| 15 | 50 seconds | 10 seconds |

The precise allocations follow Python's `round()` behavior.

These allocations are candidate solutions rather than guaranteed optimal signal timings. Their suitability depends on the scoring function, the traffic assumptions, and real-world safety constraints.

---

## Input Validation

The application validates the four traffic density inputs before running the quantum simulation.

The validation logic checks that:

- All four directions have a value.
- Each value can be converted into a number.
- Values are finite and nonnegative.
- No individual direction exceeds 500 vehicles.

Invalid inputs are rejected with an explanatory error message.

These checks improve the reliability of the application and prevent invalid data from entering the traffic calculation workflow.

---

## Installation and Setup

### Prerequisites

Install the following before running the project:

- Python 3.10 or a compatible Python version supported by the selected Qiskit packages.
- pip, the Python package installer.
- A modern web browser.
- A terminal such as PowerShell, Command Prompt, or the VS Code terminal.

Python 3.13 may work with compatible package releases, but confirm that the installed Qiskit and Qiskit Aer versions support your Python version.

### 1. Clone the Repository

Replace the placeholder URL with the actual URL of your GitHub repository.

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

Alternatively, download the repository and extract it locally.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If you use Command Prompt instead:

```bat
venv\Scripts\activate.bat
```

### 3. Install Dependencies

Create a file named `requirements.txt` containing:

```text
Flask
qiskit
qiskit-aer
```

Install the packages:

```bash
python -m pip install -r requirements.txt
```

For a reproducible project, test the application and pin the exact package versions that work in your environment.

### 4. Check the Project Structure

A recommended project structure is:

```text
Quantum-Traffic-Optimizer/
│
├── quanttrafficoptimizer.py
├── requirements.txt
├── README.md
│
├── templates/
│   └── index1.html
│
└── static/
    └── style.css
```

The `templates` directory contains HTML files rendered by Flask. The `static` directory contains CSS and other static assets.

The filenames must match the actual filenames referenced by the Python application.

### 5. Run the Application

From the project root directory, run:

```bash
python quanttrafficoptimizer.py
```

Open the local address printed by Flask in your browser, typically:

```text
http://127.0.0.1:5000/
```

Do not expose Flask's development server directly to the public internet.

---

## Usage

1. Start the Flask application.
2. Open the application in your browser.
3. Enter the number of waiting vehicles for North, South, East, and West.
4. Submit the form.
5. The backend validates the input values.
6. The traffic demand calculation determines the North–South demand share.
7. The quantum circuit is constructed and simulated.
8. The measured outcomes are mapped to candidate signal allocations.
9. The candidates are evaluated using the configured traffic objective.
10. The selected allocation is displayed on the webpage.

The exact output depends on the implementation of the candidate scoring and selection logic.

---

## Example Scenario

Consider the following illustrative traffic inputs:

| Direction | Waiting vehicles |
|---|---:|
| North | 180 |
| South | 120 |
| East | 60 |
| West | 40 |
| **Total** | **400** |

The North–South traffic demand share is:

\[
p=\frac{180+120}{400}=0.75
\]

The corresponding rotation angle is:

\[
\theta=2\arcsin(\sqrt{0.75})=\frac{2\pi}{3}
\]

The circuit therefore assigns a 0.75 probability of measuring 1 on each qubit.

The expected number of 1 bits in a four-bit measurement is:

\[
E[\text{number of 1s}]=4p=3
\]

This makes bitstrings containing more 1s more likely than they would be under a uniform distribution.

However, the candidate-to-green mapping assigns larger candidate numbers more North–South green time. The final schedule must still be evaluated using the application's scoring objective rather than assuming that the most frequently measured bitstring is automatically optimal.

---

## Optimization Strategy

The project separates candidate generation from candidate evaluation.

**Candidate generation:** The quantum circuit produces a probability distribution over 16 candidate schedules, influenced by the North–South traffic share.

**Candidate evaluation:** Classical logic evaluates the available schedules according to a defined traffic objective.

**Candidate selection:** The best-scoring schedule is selected from the candidates considered by the implementation.

A more advanced version could use a mathematically defined waiting-time or queue-based objective function, with explicit constraints for pedestrian crossings, yellow-light intervals, safety clearances, and minimum green times.

The current circuit is a quantum circuit simulation used to explore traffic scheduling. It should not be described as a proven quantum speedup over classical optimization.

---

## Testing and Evaluation

The application can be tested using several traffic scenarios.

| Test case | North | South | East | West |
|---|---:|---:|---:|---:|
| Balanced traffic | 100 | 100 | 100 | 100 |
| North–South heavy | 200 | 150 | 40 | 30 |
| East–West heavy | 30 | 40 | 180 | 170 |
| No traffic | 0 | 0 | 0 | 0 |
| Boundary value | 500 | 0 | 0 | 0 |

For each test, verify that:

- The application accepts valid input.
- Invalid or missing values produce clear errors.
- The quantum circuit executes successfully.
- Measurement counts are returned.
- Candidate allocations remain between 10 and 50 seconds for each phase.
- The total green allocation remains 60 seconds.
- The chosen candidate matches the configured scoring objective.

Because quantum measurements are sampled, the measurement counts can vary between executions. Use a fixed simulator seed when reproducible simulation results are required and supported by the selected execution configuration.

---

## Limitations

This project is an educational prototype and has several important limitations.

1. **Simplified intersection model:** It combines the four directions into two phases and does not model turning movements or conflicting traffic streams.
2. **Static traffic inputs:** It processes submitted vehicle counts rather than continuously collecting live traffic data.
3. **Limited candidate space:** The circuit generates 16 candidate outcomes, so only 16 possible green allocations are represented.
4. **Simplified demand model:** The same probability parameter is used for all four qubits; it does not encode four independent directional densities directly.
5. **Classical scoring requirement:** A quantum circuit does not automatically optimize traffic flow. The objective function determines how candidate schedules are ranked.
6. **No demonstrated quantum advantage:** The implementation uses a classical simulator and does not establish a performance advantage over classical optimization.
7. **Safety requirements:** The prototype is not suitable for controlling real traffic signals without extensive engineering, testing, regulatory compliance, and safety validation.

---

## Future Improvements

Possible extensions include:

- Implement a more realistic queue-based traffic objective function.
- Compare the quantum candidate-generation method against a classical search or optimization baseline.
- Increase the number of candidate schedules using additional qubits.
- Encode separate directional traffic information in a more expressive quantum circuit.
- Add charts showing vehicle density, measurement probabilities, and selected green-light allocations.
- Integrate simulated vehicle arrivals and queue-length updates over multiple cycles.
- Add configurable signal-cycle duration and minimum green-time constraints.
- Explore QAOA or other quantum optimization methods for more complex scheduling problems.
- Investigate real-time traffic data integration using camera-based vehicle detection or traffic sensors.
- Add automated tests, logging, error handling, and deployment configuration.

These improvements would make the project more suitable for systematic benchmarking and future research.

---

## Learning Outcomes

Building this project provides practical experience with:

- Python application development.
- Flask routing and HTML template rendering.
- Frontend and backend integration.
- Quantum circuit construction with Qiskit.
- Hadamard and rotation gates.
- Quantum measurement and probability distributions.
- Quantum circuit simulation using Qiskit Aer.
- Mapping measurement outcomes to classical decisions.
- Candidate evaluation and constrained resource allocation.
- Testing and documenting a complete software project.

---

## Conclusion

The Quantum Traffic Optimizer demonstrates how quantum circuit simulation can be integrated into a web application to explore traffic signal allocation.

By combining traffic demand calculations, four-qubit circuit construction, Qiskit Aer simulation, and classical candidate evaluation, the project provides a practical introduction to the intersection of quantum computing, optimization, and web development.

The current implementation is intended for educational experimentation rather than deployment in real traffic infrastructure. Its primary value is demonstrating a complete workflow in which a quantum circuit generates candidate solutions and classical logic evaluates their usefulness.

## License

This project can be distributed under the MIT License if you choose that license for your repository.

If using the MIT License, add a `LICENSE` file containing the standard MIT License text and replace the copyright holder and year with your own details.
