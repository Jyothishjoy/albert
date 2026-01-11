import os
import numpy as np
from AaronTools.fileIO import FileReader
from AaronTools.geometry import Geometry
from AaronTools.finders import BondedElements
from AaronTools.internal_coordinates import Bond
from albert.energy_extractor import extract_scf_energy_from_log
from albert.file_names import Complex, Complex_pop, Frag_1_pop, Frag_1_Cat_pop, Frag_1_Ani_pop, Frag_2_pop


def extract_bndlgth_freq_frc_const(subdir):
    log_file_path = os.path.join(subdir, Complex)
    infile = FileReader(log_file_path, just_geom=False)
    charge = infile['charge']
    geom = Geometry(infile, refresh_connected=True, refresh_ranks=False)
    metal = geom.find("Pd")[0]
    methyl = geom.find(BondedElements("Pd", "H", "H", "H"), "C")[0]
    bond = Bond(geom.atoms.index(metal), geom.atoms.index(methyl))
    distance = methyl.dist(metal)
    s_vec = bond.s_vector(geom.coords)
    freq = infile["frequency"]
    
    max_overlap = None
    best_stretch = None
    for mode in freq.data:
        overlap = abs(np.dot(s_vec, np.reshape(mode.vector, -1)))
        if max_overlap is None or overlap > max_overlap:
            max_overlap = overlap
            best_stretch = mode

    vib_freq = best_stretch.frequency
    force_const = best_stretch.forcek

    return charge, distance, vib_freq, force_const
    
def extract_Radical_Attch_Energy(subdir):

    frag1_path = os.path.join(subdir, Frag_1_pop)
    frag1_cat_path = os.path.join(subdir, Frag_1_Cat_pop)

    if os.path.exists(frag1_path) and os.path.exists(frag1_cat_path):
        energy_frag1 = extract_scf_energy_from_log(frag1_path)
        energy_frag1_cat = extract_scf_energy_from_log(frag1_cat_path)

        if energy_frag1 is not None and energy_frag1_cat is not None:
            rad_attch_energy = (energy_frag1_cat - energy_frag1)
            return rad_attch_energy

    return None
    
def somo_lumo_spin_Mulliken_dipole(subdir):
    log_file_path = os.path.join(subdir, Frag_1_pop)
    if os.path.isfile(log_file_path):
        try:
            with open(log_file_path, 'r') as f:
                file_contents = f.read()

            lines = file_contents.split('\n')
            last_alpha_line = None
            somo = None
            lumo = None
            somo_lumo = None

            for line in lines:
                if "Alpha  occ. eigenvalues" in line:
                    last_alpha_line = line
                    continue

                if last_alpha_line and "Beta virt. eigenvalues" in line:
                    lumo = float(line.split()[4])
                    somo = float(last_alpha_line.split()[-1])
                    somo_lumo = lumo - somo
                    break

            start_marker = "Mulliken charges and spin densities:"
            end_marker = "Sum of Mulliken charges ="
            start_index = file_contents.rfind(start_marker)
            end_index = file_contents.find(end_marker, start_index)
            Pd_spin_density = None
            Pd_Mull_charge = None
            spin_deloc_index = None

            if start_index != -1 and end_index != -1:
                section = file_contents[start_index:end_index]

                pd_line = None
                for line in section.split('\n'):
                    if 'Pd' in line:
                        pd_line = line
                        break

                if pd_line:
                    items = pd_line.split()
                    Pd_spin_density = float(items[-1])
                    spin_deloc_index = 1 - Pd_spin_density
                    Pd_Mull_charge = float(items[2])

            dipole_start_marker = "Dipole moment (field-independent basis, Debye):"
            dipole_end_marker = "Quadrupole moment (field-independent basis, Debye-Ang):"

            dipole_start_index = file_contents.rfind(dipole_start_marker)
            dipole_end_index = file_contents.find(dipole_end_marker, start_index)

            if dipole_start_index != -1 and dipole_end_index != -1:
                section = file_contents[dipole_start_index:dipole_end_index]

                dipole_line = None
                for line in section.split('\n'):
                    if 'Tot=' in line:
                        dipole_line = line
                        break
                if dipole_line:
                    items = dipole_line.split()
                    dipole = float(items[-1])
                else:
                    dipole = None
            else:
                dipole = None

            return somo, lumo, somo_lumo, Pd_spin_density, spin_deloc_index, Pd_Mull_charge, dipole
        
        except Exception as e:
            print(f"Error processing file {log_file_path}: {e}")
            return None, None, None, None, None, None, None

    else:
        print(f"File {log_file_path} not found.")
        return None, None, None, None, None, None, None
        

