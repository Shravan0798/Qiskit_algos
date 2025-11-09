# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 16:56:29 2025

@author: Shravan
"""

"""
backends.py
A helper module to manage Qiskit backends dynamically.
If IBM account is configured, shows available QPUs.
If not, defaults to AerSimulator.

It has two functions 
choose_backend function to select backend based on saved accounts or Aer Simulator.
run_circuit function which takes in Quantum circuit,shots and optimization_leve\
    as arguments and runs the circuit on selected backends based on choose backend
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from IPython.display import display

# ---------------------------------------------------------------------
# Choose Backend Function
# ---------------------------------------------------------------------

def choose_backend():
    """
    Checks if IBM account is saved and lets user choose between Aer simulator or real QPU.
    Returns the backend object.
    """
    try:
        # Try to load IBM account
        service = QiskitRuntimeService()# assumes account already saved via service.save_account()
        backends = service.backends()
        least_busy = service.least_busy(simulator = False)
        
        
        #If IBM account is saved lists available backends and the least busy backend, else uses Aer Simulator
        if backends:
            print("\nIBM account found.")
            print("Available IBM QPUs:")
            available_backends = []
            for index, backend in enumerate(backends):
                name = backend.name
                if backend.status().status_msg == "active":
                    status = "Online"
                else: 
                    status = backend.status().status_msg
                available_backends.append(backend)
                print(f"{index + 1}. {name} - {status}")
            print(f"\nThe least busy backend is: {least_busy.name}")
            
            # Getting input from user to use a IBM backend from list or to Aer Simulator
            print("\nChoose backend type: ")
            print("1. Use real QPU from IBM Cloud")
            print("2. Use local Aer simulator")
            choice = int(input("Enter your choice (1/2): ").strip())
            if choice == 1:
                index = int(input("Enter QPU number from list above:")) - 1
                if 0 <= index < len(available_backends):
                    backend = available_backends[index]
                    print(f"Using IBM QPU: {backend.name}")
                    return backend
                else:
                    print("Invalid selection for QPU, Falling back to AerSimulator.")
                    return AerSimulator()
            elif choice == 2:
                print("Using AerSimulator")
                return AerSimulator()
            else:
                print("No such choice exists give either 1 or 2 to use QPU or Simulator")
            
        else:
            print("No IBM QPUs available. Using local AerSimulator instead.")
            return AerSimulator()
    except Exception as e:
        # Handle case where account is not saved or unreachable
        print("IBM account not found or connection failed. Using AerSimulator instead.")
        print(f"Error detail: {e}")
        return AerSimulator()


# ---------------------------------------------------------------------
# Circuit Run Function
# ---------------------------------------------------------------------
def run_circuit(qc: QuantumCircuit, shots: int = 2000, optimization_level: int =1):
    """
    Run the Quantum Circuit on a Simulator or Real backend selected from backends module

    Parameters
    ----------
    qc : QuantumCircuit
    shots: int Default value is 2000 can be edited while calling the function
    optimization_level: int Default value is 1 can be edited while calling the function
    
    Returns
    -------
    dict
        Measurement counts run on Aer Simulator or selected QPU
    """
    backend = choose_backend()
    print(f"\nBackend selected: {backend.name}")
    if backend.name == "aer_simulator":
        job = backend.run(qc, shots = shots)
        result = job.result()
        counts = result.get_counts()
        print(f"The job ran on {backend.name}")
        print (f"The counts for {shots} is: {counts}")
        print("Plotting the data into histogram")
        display(plot_histogram(counts))
        return counts
    else:
        sampler = Sampler(mode = backend)
        target =  backend.target
        pm = generate_preset_pass_manager(target = target, optimization_level = optimization_level )
        transpiled_cir = pm.run(qc)
        print(f"\nThe Transpiled circuit for the {backend.name} QPU")
        display(transpiled_cir.draw('mpl'))
        print(f"\nRunning the transpiled circuit on {backend.name} QPU")
        job = sampler.run([transpiled_cir], shots = shots)
        job_id = job.job_id()
        result = job.result()
        print(f"\nSubmitted job to {backend.name} QPU and the job ID is: {job_id}")
        counts = result[0].data.c.get_counts()
        print(f"\nThe job {job_id} ran on {backend.name} and the counts for {shots} is:\n{counts}")
        print("\nPlotting the data into histogram")
        display(plot_histogram(counts))
        return counts    
       

            