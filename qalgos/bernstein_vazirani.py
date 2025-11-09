# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 21:27:20 2025

@author: Shravan
"""

"""
bernstein_vazirani.py — Bernstein-Vazirani Algorithm Implementation

Compatible with:
- oracles.py
- backends.py

Builds Bernstein-Vazirani circuit with:
  • Bernstein-Vazirani oracle function
  • Optional as_circuit mode (for qc.compose)
"""

from qiskit import QuantumCircuit
from qalgos.oracles import bv_oracle
from IPython.display import display

# ---------------------------------------------------------------------
# Circuit Build Function
# ---------------------------------------------------------------------
def bernstein_vazirani_circuit(secret_string: str, as_circuit: bool = False):
    """
    Construct the full Bernstein–Vazirani algorithm circuit.

    Parameters
    ----------
    secret_string : str
        Secret bitstring used by the oracle.
    as_circuit : bool, optional
        If True, build using a QuantumCircuit oracle.
        If False, build using a callable oracle function.

    Returns
    -------
    QuantumCircuit
        Full Bernstein–Vazirani circuit with measurements.
    """
    n = len(secret_string)

    # Initialize circuit with n input qubits + 1 ancilla, and n classical bits
    qc = QuantumCircuit(n + 1, n)

    # Initialize ancilla qubit in |1>
    qc.x(n)
    
    # Apply Hadamard to all qubits
    qc.h(range(n + 1))
    
    # Apply Barrier
    qc.barrier()

    # Get the oracle (either circuit or callable)
    oracle = bv_oracle(secret_string, as_circuit=as_circuit)

    # Compose oracle depending on type
    if as_circuit:
        qc.compose(oracle, inplace=True)
    else:
        oracle(qc)  # call the function form directly
    
    # Apply Barrier
    qc.barrier()

    # Apply final Hadamard gates to input qubits
    qc.h(range(n))

    # Measure input qubits
    qc.measure(range(n), range(n))
    try:
        display(qc.draw('mpl'))
    except Exception:
        print(qc.draw())
    return qc
