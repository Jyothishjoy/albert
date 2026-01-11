def extract_scf_energy_from_log(log_file_path):
    """Extract the final SCF energy from a log file."""
    scf_energy = None
    with open(log_file_path, 'r') as file:
        for line in file:
            if 'SCF Done' in line:
                scf_energy = float(line.split('=')[-1].split()[0])
    return scf_energy

def extract_E_ZPE_from_log(log_file_path):
    """Extract electronic and zero-point energy from a log file."""
    E_ZPE = None
    with open(log_file_path, 'r') as file:
        for line in file:
            if 'Sum of electronic and zero-point Energies=' in line:
                E_ZPE = float(line.split('=')[-1])
    return E_ZPE
    
def extract_H_from_log(log_file_path):
    """Extract enthalpy energy from a log file."""
    H = None
    with open(log_file_path, 'r') as file:
        for line in file:
            if 'Sum of electronic and thermal Enthalpies=' in line:
                H = float(line.split('=')[-1])
    return H
    
def extract_G_from_log(log_file_path):
    """Extract free energy from a log file."""
    G = None
    with open(log_file_path, 'r') as file:
        for line in file:
            if 'Sum of electronic and thermal Free Energies=' in line:
                G = float(line.split('=')[-1])
    return G
    
    