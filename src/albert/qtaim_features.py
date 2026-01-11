import os
import re 
from albert.file_names import qtaim_file

def extract_qtaim_data(subdir):
    # Initialize variables to None
    Electron_Density = None
    Lagrangian_KE = None
    Hamiltonian_KE = None
    PE_Density = None
    Energy_density = None
    Laplacian = None
    ELF = None
    LOL = None
    Local_info_entropy = None
    RDG = None
    Sign_lambda2_rho = None
    SF = None
    ALIE = None
    ESP_nuclear = None
    ESP_electrons = None
    Total_ESP = None
    Ellipticity = None
    eta_index = None

    try:
        # Construct file path
        qtaim_file_path = os.path.join(subdir, qtaim_file)

        if not os.path.exists(qtaim_file_path):
            raise FileNotFoundError(f"File not found: {qtaim_file_path}")

        with open(qtaim_file_path, 'r') as file:
            content = file.read()

        start_marker = " ----------------   CP     3,     Type (3,-1)   ----------------"
        end_marker = " eta index:"

        start_index = content.rfind(start_marker)
        end_index = content.find(end_marker, start_index)

        if start_index != -1 and end_index != -1:
            end_index = content.find("\n", end_index)
            section = content[start_index:] if end_index == -1 else content[start_index:end_index]

            for line in section.split('\n'):
                try:
                    if "Density of all electrons:" in line:
                        Electron_Density = float(line.split(":")[-1].strip())
                    elif "Lagrangian kinetic energy G(r):" in line:
                        Lagrangian_KE = float(line.split(":")[-1].strip())
                    elif "Hamiltonian kinetic energy K(r):" in line:
                        Hamiltonian_KE = float(line.split(":")[-1].strip())
                    elif "Potential energy density V(r):" in line:
                        PE_Density = float(line.split(":")[-1].strip())
                    elif "Energy density E(r) or H(r):" in line:
                        Energy_density = float(line.split(":")[-1].strip())
                    elif "Laplacian of electron density:" in line:
                        Laplacian = float(line.split(":")[-1].strip())
                    elif "Electron localization function (ELF):" in line:
                        ELF = float(line.split(":")[-1].strip())
                    elif "Localized orbital locator (LOL):" in line:
                        LOL = float(line.split(":")[-1].strip())
                    elif "Local information entropy:" in line:
                        Local_info_entropy = float(line.split(":")[-1].strip())
                    elif "Reduced density gradient (RDG):" in line:
                        RDG = float(line.split(":")[-1].strip())
                    elif "Sign(lambda2)*rho:" in line:
                        Sign_lambda2_rho = float(line.split(":")[-1].strip())
                    elif "Source function," in line:
                        SF = float(line.split(":")[-1].strip())
                    elif "Average local ionization energy (ALIE):" in line:
                        ALIE = float(line.split(":")[-1].strip())
                    elif "ESP from nuclear charges:" in line:
                        ESP_nuclear = float(line.split(":")[-1].strip())
                    elif "ESP from electrons:" in line:
                        ESP_electrons = float(line.split(":")[-1].strip())
                    elif "Total ESP:" in line:
                        Total_ESP = float(line.split(":")[-1].split()[0].strip())
                    elif "Ellipticity of electron density:" in line:
                        Ellipticity = float(line.split(":")[-1].strip())
                    elif "eta index:" in line:
                        eta_index = float(line.split(":")[-1].strip())
                except ValueError as e:
                    print(f"Warning: Could not convert value in line '{line.strip()}'. Error: {e}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return (
        Electron_Density, Lagrangian_KE, Hamiltonian_KE, PE_Density, 
        Energy_density, Laplacian, ELF, LOL, Local_info_entropy, RDG, 
        Sign_lambda2_rho, SF, ALIE, ESP_nuclear, ESP_electrons, 
        Total_ESP, Ellipticity, eta_index
    )

