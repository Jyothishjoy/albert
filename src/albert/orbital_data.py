import os
import numpy as np
from AaronTools.fileIO import FileReader
from AaronTools.geometry import Geometry
from AaronTools.finders import BondedElements
from AaronTools.internal_coordinates import Bond
from albert.file_names import Complex, Complex_pop, Frag_1_pop, Frag_1_Cat_pop, Frag_1_Ani_pop, Frag_2_pop


def extract_complex_orbital_data(subdir):
    log_file_path = os.path.join(subdir, Complex_pop)
    if os.path.isfile(log_file_path):
        infile = FileReader(log_file_path, just_geom=False)
        geom = Geometry(infile, refresh_connected=True, refresh_ranks=False)
        metal = geom.find("Pd")[0]
        methyl_C = geom.find(BondedElements("Pd", "H", "H", "H"), "C")[0]
            
        metal_id = geom.atoms.index(metal) + 1
        carbon_id = geom.atoms.index(methyl_C) + 1
                      
        orbital_energy = extract_Pd_Me_Orbital_Energy(log_file_path, metal_id, carbon_id)
        methyl_C_1s_energy = extract_C_1s_energy(log_file_path, carbon_id)
        if orbital_energy and methyl_C_1s_energy:
            return orbital_energy, methyl_C_1s_energy
    return None, None
    
def extract_Pd_Me_Orbital_Energy(log_file_path, metal_id, carbon_id):
    """
    Extract orbital energy of the Pd-Me bond: 
    There are several MOs with Pd-Me bond chracter,
    hence the line with the maximum value of 'C{carbon_id}-p' 
    from a log file is extracted.
    """
    start_marker = "Atomic contributions to Alpha molecular orbitals:"
    end_marker = " Orbital energies and kinetic energies (alpha):"
    keywords = ["Alpha", "occ", f"Pd{metal_id}-d", f"C{carbon_id}-p"]

    max_value = float('-inf')
    max_line = None

    try:
        with open(log_file_path, 'r') as file:
            lines = file.readlines()
            
            in_section = False
            for line in lines:
                if start_marker in line:
                    in_section = True
                    continue
                if end_marker in line:
                    in_section = False

                if in_section and all(keyword in line for keyword in keywords):
                    parts = line.split()
                    for part in parts:
                        if part.startswith(f"C{carbon_id}-p"):
                            value_str = part.split('=')[-1]
                            try:
                                value = float(value_str)
                                if value > max_value:
                                    max_value = value
                                    max_line = line
                            except ValueError:
                                print(f"Could not convert value to float: {value_str}")

        if max_line:
            # Split the max_line and get the 4th item, then split that and get the last item
            parts = max_line.split()
            if len(parts) >= 4:
                for part in parts:
                    if part.startswith("OE="):
                        orbital_energy = part.split('=')[-1]
            return orbital_energy
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def extract_C_1s_energy(file_path, carbon_id):
    start_marker = "Atomic contributions to Alpha molecular orbitals:"
    end_marker = " Orbital energies and kinetic energies (alpha):"
    keywords_Me_1s_energy = ["Alpha", "occ", f"C{carbon_id}-s"]

    max_value = float('-inf')
    max_line = None
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            in_section = False
            for line in lines:
                if start_marker in line:
                    in_section = True
                    continue
                if end_marker in line:
                    in_section = False

                if in_section and all(keyword in line for keyword in keywords_Me_1s_energy):
                    parts = line.split()
                    if len(parts) >= 4:
                        # Extract value specifically from C{carbon_id}-p
                        for part in parts:
                            if part.startswith(f"C{carbon_id}-s"):
                                value_str = part.split('=')[-1]
                                try:
                                    value = float(value_str)
                                    if value > max_value:
                                        max_value = value
                                        max_line = line
                                except ValueError:
                                    print(f"Could not convert value to float: {value_str}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

    if max_line:
        # Split the max_line and get the 4th item, then split that and get the last item
        parts = max_line.split()
        if len(parts) >= 4:
            for part in parts:
                if part.startswith("OE="):
                    methyl_C_1s_energy = part.split('=')[-1]
        return methyl_C_1s_energy
    return None