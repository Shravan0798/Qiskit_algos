# Qiskit Algos — Quantum Algorithm Implementations

A modular Python package that implements popular **quantum computing algorithms** such as **Deutsch-Jozsa** and **Bernstein-Vazirani**, built using [Qiskit](https://qiskit.org/).  
It provides reusable circuit builders, oracle generators, and backend utilities to easily run circuits on both simulators and IBM Quantum QPUs.

---

## Features

1) Modular algorithm design (Deutsch-Jozsa, Bernstein-Vazirani, and more coming soon)
2) Unified `run_circuit()` interface for simulators and real QPUs
3) Oracle builder utilities
4) Automatic histogram plotting of results

---

## Project Structure

```
Qiskit_algos/
│
├── qalgos/
│ ├── init.py
│ ├── deutsch_jozsa.py
│ ├── bernstein_vazirani.py
│ ├── oracles.py
│ ├── backends.py
│
├── setup.py
├── pyproject.toml
├── MANIFEST.in
├── LICENSE
└── README.md
```

---

## Installation

### Option 1 — Local Installation (Recommended for Development)

```bash
git clone https://github.com/Shravan0798/Qiskit_algos.git
cd Qiskit_algos
pip install -e .

### Option 2 - Build & Install from Distribution

python setup.py sdist bdist_wheel
pip install dist/qalgos-0.1.0-py3-none-any.whl
```
---

## Example

```python
from qalgos.deutsch_jozsa import deutsch_jozsa_circuit
from qalgos.bernstein_vazirani import bernstein_vazirani_circuit
from qalgos.backends import run_circuit

# Deutsch-Jozsa example
dj_circuit = deutsch_jozsa_circuit(5, "balanced", True)
run_circuit(dj_circuit, shots=1024)

# Bernstein-Vazirani example
bv_circuit = bernstein_vazirani_circuit("10101", True)
run_circuit(bv_circuit, shots=1024)

```