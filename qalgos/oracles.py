# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 21:34:51 2025

@author: Shravan
"""

"""
oracles.py — Oracle implementations for quantum algorithms

Supports both usage styles:
  • In-place mode: oracle(qc) adds gates directly to an existing circuit.
  • Circuit mode:  oracle(..., as_circuit=True) returns a QuantumCircuit
    that can be composed or drawn directly.

Implements oracles for:
  Deutsch–Jozsa (constant and balanced, randomized variants)
  Bernstein-Vazirani
Usage examples
--------------
Deutsch–Jozsa:
# 1 In-place mode
oracle_fn = dj_constant_oracle_random(3)
qc = QuantumCircuit(4)
oracle_fn(qc)
qc.draw('mpl')

# 2️Circuit mode
oracle_circ = dj_constant_oracle_random(3, as_circuit=True)
qc = QuantumCircuit(4)
qc.compose(oracle_circ, inplace=True)
qc.draw('mpl')

Bernstein-Vazirani:
# 1 In-place mode
oracle_fn = bv_oracle("1011")
qc = QuantumCircuit(5)
oracle_fn(qc)
qc.draw('mpl')

# 2️Circuit mode
oracle_circ = bv_oracle("1011", as_circuit=True)
qc = QuantumCircuit(5)
qc.compose(oracle_circ, inplace=True)
qc.draw('mpl')
"""

import random
from typing import Callable
from qiskit import QuantumCircuit

# ---------------------------------------------------------------------
#  Deutsch–Jozsa Oracles (ancilla-style, last qubit is target)
# ---------------------------------------------------------------------

# === CONSTANT ORACLES =================================================

def dj_constant_oracle_impl_do_nothing(n: int) -> Callable[[QuantumCircuit], None]:
    """Implements f(x) = 0 for all x (no operation)."""
    def oracle_fn(qc: QuantumCircuit):
        pass
    return oracle_fn


def dj_constant_oracle_impl_flip_target(n: int) -> Callable[[QuantumCircuit], None]:
    """Implements f(x) = 1 for all x (flips target regardless of input)."""
    def oracle_fn(qc: QuantumCircuit):
        qc.x(n)
    return oracle_fn


def dj_constant_oracle_random(n: int, value: int = None, as_circuit: bool = False):
    """
    Return a randomized constant oracle.

    Parameters
    ----------
    n : int
        Number of input qubits (excluding ancilla).
    value : int, optional
        Force the oracle to implement f(x)=0 or f(x)=1. If None, random.
    as_circuit : bool
        If True, returns a QuantumCircuit for composition.
        If False, returns a callable for in-place application.
    """
   

    # Choose between two constant oracles randomly
    if value is None: 
        value = random.choice([0, 1]) # based on the value chooses between two constant oracles
    implementations = [
        dj_constant_oracle_impl_do_nothing(n),
        dj_constant_oracle_impl_flip_target(n)
    ]

    chosen_implementation = implementations[value]

    if as_circuit:
        qc = QuantumCircuit(n + 1)
        chosen_implementation(qc)
        return qc  #Returns the oracle as circuit can be used with qc.compose
    else:
        return chosen_implementation #Returns the oracle as function cannot be used with qc.compose


# === BALANCED ORACLES =================================================

def dj_balanced_oracle_parity(n: int) -> Callable[[QuantumCircuit], None]:
    """Balanced oracle 1 — flips target if parity of first (n-1) bits == 1."""
    def oracle_fn(qc: QuantumCircuit):
        target = n
        for i in range(0,n):
            qc.cx(i, target)
    return oracle_fn


def dj_balanced_oracle_parity_reverse(n: int) -> Callable[[QuantumCircuit], None]:
    """Balanced oracle 2 — parity flip + X on target to invert output."""
    def oracle_fn(qc: QuantumCircuit):
        target = n
        for i in range(0,n):
            qc.cx(i, target)
        qc.x(target)
    return oracle_fn


def dj_balanced_oracle_random(n: int, value: int = None, as_circuit: bool = False):
    """
    Return a randomized balanced oracle.

    Parameters
    ----------
    n : int
        Number of input qubits (excluding ancilla).
    as_circuit : bool
        If True, returns a QuantumCircuit for composition.
        If False, returns a callable for in-place application.
    """
    # Choose between two constant oracles randomly
    if value is None: 
        value = random.choice([0, 1])# based on the value chooses between two balanced oracles
    implementations = [
        dj_balanced_oracle_parity(n),
        dj_balanced_oracle_parity_reverse(n)
    ]
    chosen_implementation = implementations[value]
    if as_circuit:
        qc = QuantumCircuit(n + 1)
        chosen_implementation(qc)
        return qc #Returns the oracle as circuit can be used with qc.compose
    else:
        return chosen_implementation #Returns the oracle as function cannot be used with qc.compose


def bv_oracle(secret_string: str, as_circuit: bool = False):
    """
    Construct the Bernstein–Vazirani oracle for a given secret string.

    Parameters
    ----------
    secret_string : str
        Binary string (e.g. "1011") representing the hidden bit string `s`.
    as_circuit : bool, optional
        If True, returns a QuantumCircuit object; else returns callable oracle.

    Returns
    -------
    QuantumCircuit or function
        Oracle circuit or callable that applies oracle to a given qc.
    """
    n = len(secret_string)
    qc_oracle = QuantumCircuit(n + 1)

    # Apply X gates to input qubits where secret bit = 1
    for i, bit in enumerate(reversed(secret_string)):
        if bit == "1":
            qc_oracle.cx(i, n)

    if as_circuit:
        return qc_oracle
    else:
        def oracle_fn(qc: QuantumCircuit):
            qc.compose(qc_oracle, inplace=True)
        return oracle_fn

__all__ = [
    "dj_constant_oracle_impl_do_nothing",
    "dj_constant_oracle_impl_flip_target",
    "dj_constant_oracle_random",
    "dj_balanced_oracle_parity",
    "dj_balanced_oracle_parity_reverse",
    "dj_balanced_oracle_random",
    "bv_oracle"
]