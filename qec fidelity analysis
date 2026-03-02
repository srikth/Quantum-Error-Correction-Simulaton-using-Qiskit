import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, Aer, execute
from qiskit.providers.aer.noise import NoiseModel, depolarizing_error
from qiskit.quantum_info import Statevector, state_fidelity

# Create single qubit (no protection)
def single_qubit_circuit():
    qc = QuantumCircuit(1)
    qc.x(0)  # logical |1>
    return qc

# Create 3-qubit bit-flip code
def bit_flip_circuit():
    qc = QuantumCircuit(3)

    # Logical state
    qc.x(0)

    # Encode
    qc.cx(0, 1)
    qc.cx(0, 2)

    # Decode + Correct (majority vote)
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.ccx(1, 2, 0)

    return qc

def simulate_with_noise(qc, noise_prob):
    noise_model = NoiseModel()
    error = depolarizing_error(noise_prob, 1)
    noise_model.add_all_qubit_quantum_error(error, ['x', 'cx', 'ccx'])

    simulator = Aer.get_backend("statevector_simulator")
    result = execute(qc, simulator, noise_model=noise_model).result()
    return result.get_statevector()

def run_experiment():

    noise_levels = np.linspace(0.0, 0.2, 10)

    fidelity_unprotected = []
    fidelity_protected = []

    for p in noise_levels:

        # Ideal reference state
        ideal_single = Statevector.from_label('1')
        ideal_protected = Statevector.from_label('111')

        # Simulate
        sv_single = simulate_with_noise(single_qubit_circuit(), p)
        sv_protected = simulate_with_noise(bit_flip_circuit(), p)

        # Compute fidelity
        f1 = state_fidelity(sv_single, ideal_single)
        f2 = state_fidelity(sv_protected, ideal_protected)

        fidelity_unprotected.append(f1)
        fidelity_protected.append(f2)

    # Plot
    plt.figure()
    plt.plot(noise_levels, fidelity_unprotected)
    plt.plot(noise_levels, fidelity_protected)
    plt.xlabel("Noise Probability")
    plt.ylabel("State Fidelity")
    plt.title("Quantum Error Correction Performance")
    plt.show()

if _name_ == "_main_":
    run_experiment()
