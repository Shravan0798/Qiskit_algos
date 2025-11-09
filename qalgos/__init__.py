# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 15:28:31 2025

@author: Shravan
"""

"""qalgos package: public API"""

from .deutsch_jozsa import deutsch_jozsa_circuit
from .bernstein_vazirani import bernstein_vazirani_circuit
from .oracles import *
from .oracles import __all__ as oracles_all
from .backends import choose_backend, run_circuit

__all__ = [
    "deutsch_jozsa_circuit",
    "bernstein_vazirani_circuit",
    "choose_backend",
    "run_circuit",
    *oracles_all
]