# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 22:14:44 2025

@author: Shravan
"""

"""
deutsch_jozsa.py — Deutsch–Jozsa Algorithm Implementation

Compatible with:
- oracles.py
- backends.py

Builds Deutsch–Jozsa circuits with:
  • Random constant or balanced oracles
  • Optional as_circuit mode (for qc.compose)
"""
from qiskit import QuantumCircuit
from IPython.display import display


#
from qalgos.oracles import (
    dj_constant_oracle_random,
    dj_balanced_oracle_random
)



# ---------------------------------------------------------------------
# Circuit Build Function
# ---------------------------------------------------------------------
def deutsch_jozsa_circuit(n: int, oracle_type: str = "balanced", as_circuit: bool = False):
    """
    Build the Deutsch–Jozsa circuit.

    Parameters
    ----------
    n : int
        Number of input qubits (excluding ancilla).
    oracle_type : str
        "constant" or "balanced".
    as_circuit : bool
        If True, build using a QuantumCircuit oracle.
        If False, build using a callable oracle function.

    Returns
    -------
    QuantumCircuit
        Full Deutsch–Jozsa circuit with measurements.
    """
    qc = QuantumCircuit(n + 1, n)

    # Initialize ancilla to |1>
    qc.x(n)

    # Apply Hadamard to all qubits
    qc.h(range(n + 1))
    # Apply Barrier
    qc.barrier()

    # -----------------------------------------------------------------
    # Oracle selection from oracles module (use all 3 arguments)
    # -----------------------------------------------------------------
    if oracle_type.lower() == "constant":
        oracle = dj_constant_oracle_random(n,None,as_circuit)
        oracle_label = "CONSTANT"
    elif oracle_type.lower() == "balanced":
        oracle = dj_balanced_oracle_random(n,None,as_circuit)
        oracle_label = "BALANCED"
    else:
        raise ValueError("oracle_type must be 'constant' or 'balanced'")

    # Apply oracle
    if as_circuit:
        qc.compose(oracle, inplace=True)
    else:
        oracle(qc)
    # Apply Barrier
    qc.barrier()
    # Apply Hadamard on input qubits
    qc.h(range(n+1))
    # Apply Barrier
    qc.barrier()
    # Measure input qubits
    qc.measure(range(n), range(n))

    print(f"\nOracle selected: {oracle_label}")
    try:
        display(qc.draw('mpl'))
    except Exception:
        print(qc.draw())
    return qc


    

    
    
        


