import os
from albert.energy_extractor import extract_scf_energy_from_log
from albert.file_names import Complex, Complex_pop, Frag_1_pop, Frag_1_Cat_pop, Frag_1_Ani_pop, Frag_2_pop

def extract_conceptual_dft(subdir):  # https://chemtools.org/sci_doc_conceptual.html
    frag1_path = os.path.join(subdir, Frag_1_pop)
    frag1_cat_path = os.path.join(subdir, Frag_1_Cat_pop)
    frag1_ani_path = os.path.join(subdir, Frag_1_Ani_pop)
    
    if os.path.exists(frag1_path) and os.path.exists(frag1_cat_path) and os.path.exists(frag1_ani_path):
        frag1_energy = extract_scf_energy_from_log(frag1_path)
        frag1_cat_energy = extract_scf_energy_from_log(frag1_cat_path)
        frag1_ani_energy = extract_scf_energy_from_log(frag1_ani_path)

        if frag1_energy is not None and frag1_cat_energy is not None and frag1_ani_energy is not None:
            I = (frag1_cat_energy - frag1_energy)  # Ionization Energy
            A = (frag1_energy - frag1_ani_energy)   # Electron Affinity 
            mue = -(I + A) / 2  # Chemical Potential
            eta = I - A         # Chemical Hardness
            S = 1 / (2 * eta)   # Chemical Softness
            omega = mue**2 / (2 * eta)  # Electrophilicity Index
            omega_negative = (3 * I + A)**2 / (16 * (I - A))
            omega_positive = (I + 3 * A)**2 / (16 * (I - A))

            return I, A, mue, eta, S, omega, omega_negative, omega_positive
        else:
            return None, None, None, None, None, None, None, None