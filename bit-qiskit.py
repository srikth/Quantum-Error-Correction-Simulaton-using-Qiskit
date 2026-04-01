from qiskit import QuantumCircuit, Aer, execute
from qiskit.providers.aer.noise import NoiseModel, depolarizing_error
from qiskit.quantum_info import state_fidelity
import numpy as np

# Create 3-qubit bit-flip error correction circuit
def create_bit_flip_circuit():

    qc = QuantumCircuit(3, 3)

    # Step 1: Prepare logical qubit (|1> for demonstration)
    qc.x(0)

    # Step 2: Encode (3-qubit repetition code)
    qc.cx(0, 1)
    qc.cx(0, 2)

    # Step 3: Introduce error manually (bit-flip on qubit 1)
    qc.x(1)

    # Step 4: Error correction (majority voting)
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.ccx(1, 2, 0)

    # Step 5: Measurement
    qc.measure([0, 1, 2], [0, 1, 2])

    return qc


def run_simulation():

    qc = create_bit_flip_circuit()

    # Noise model (depolarizing noise)
    noise_model = NoiseModel()
    error = depolarizing_error(0.01, 1)
    noise_model.add_all_qubit_quantum_error(error, ['x', 'cx'])

    simulator = Aer.get_backend('qasm_simulator')

    result = execute(qc, simulator, noise_model=noise_model, shots=1024).result()
    counts = result.get_counts()

    print("Measurement Results:")
    print(counts)


if _name_ == "_main_":
    run_simulation()
