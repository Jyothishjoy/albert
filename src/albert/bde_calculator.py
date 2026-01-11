import os
from albert.energy_extractor import extract_scf_energy_from_log, extract_E_ZPE_from_log 
from albert.file_names import Complex, Frag_1_Opt, Complex_pop, Frag_1_pop, Frag_1_Cat_pop, Frag_1_Ani_pop, Frag_2_pop

# Define a constant for the conversion factor
ENERGY_CONVERSION_FACTOR = 627.503

def calculate_frozen_scfbde_from_directory(subdir):
    complex_path = os.path.join(subdir, Complex_pop)
    frag1_path = os.path.join(subdir, Frag_1_pop)
    frag2_path = os.path.join(subdir, Frag_2_pop)
    
    if os.path.exists(complex_path) and os.path.exists(frag1_path) and os.path.exists(frag2_path):
        try:
            complex_energy = extract_scf_energy_from_log(complex_path)
            frag1_energy = extract_scf_energy_from_log(frag1_path)
            frag2_energy = extract_scf_energy_from_log(frag2_path)

            if complex_energy is not None and frag1_energy is not None and frag2_energy is not None:
                bde = (frag1_energy + frag2_energy - complex_energy) * ENERGY_CONVERSION_FACTOR
                return bde
            else:
                return None
        except Exception as e:
            return f"Error: {e}"
    else:
        return None

def calculate_relaxed_scfbde_from_directory(subdir):
    complex_path = os.path.join(subdir, Complex)
    frag1_opt_path = os.path.join(subdir, Frag_1_Opt)

    if os.path.exists(complex_path) and os.path.exists(frag1_opt_path):
        try:
            complex_energy = extract_scf_energy_from_log(complex_path)
            frag1_energy = extract_scf_energy_from_log(frag1_opt_path)
            frag2_energy = -39.7493929978 

            if complex_energy is not None and frag1_energy is not None and frag2_energy is not None:
                bde = (frag1_energy + frag2_energy - complex_energy) * ENERGY_CONVERSION_FACTOR
                return bde
            else:
                return None
        except Exception as e:
            return f"Error: {e}"
    else:
        return None



def calculate_relaxred_ZPEbde_from_directory(subdir):
    complex_path = os.path.join(subdir, Complex)
    frag1_opt_path = os.path.join(subdir, Frag_1_Opt)

    if os.path.exists(complex_path) and os.path.exists(frag1_opt_path):
        try:
            complex_energy = extract_E_ZPE_from_log(complex_path)
            frag1_energy = extract_E_ZPE_from_log(frag1_opt_path)
            frag2_energy = -39.719949  

            if complex_energy is not None and frag1_energy is not None and frag2_energy is not None:
                bde = (frag1_energy + frag2_energy - complex_energy) * ENERGY_CONVERSION_FACTOR
                return bde
            else:
                return None
        except Exception as e:
            return f"Error: {e}"
    else:
        return None
   
def calculate_frag_relax_energy(subdir):
    frag1_path = os.path.join(subdir, Frag_1_pop)
    frag1_opt_path = os.path.join(subdir, Frag_1_Opt)

    if os.path.exists(frag1_path) and os.path.exists(frag1_opt_path):
        try:
            frag1_energy = extract_scf_energy_from_log(frag1_path)
            frag1_opt_energy = extract_scf_energy_from_log(frag1_opt_path)

            if frag1_energy is not None and frag1_opt_energy is not None:
                frag_rlx_energy = (frag1_opt_energy - frag1_energy) * ENERGY_CONVERSION_FACTOR
                return frag_rlx_energy
            else:
                return None
        except Exception as e:
            return f"Error: {e}"
    else:
        return None

