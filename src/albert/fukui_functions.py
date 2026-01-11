import os
from albert.energy_extractor import extract_scf_energy_from_log
from albert.file_names import Complex, Complex_pop, Frag_1_pop, Frag_1_Cat_pop, Frag_1_Ani_pop, Frag_2_pop

def extract_NBO_pop(content):
    start_marker = "Summary of Natural Population Analysis:"
    end_marker = " NATURAL BOND ORBITAL ANALYSIS"

    # Find the last occurrence of the start marker
    start_index = content.find(start_marker)
    if start_index == -1:
        print("Start marker not found in the file.")
        return None

    # Find the end marker after the start marker
    end_index = content.find(end_marker, start_index)
    if end_index == -1:
        print("End marker not found in the file.")
        return None

    section = content[start_index:end_index]

    pd_line = None
    for line in section.split('\n'):
        if 'Pd' in line:
            pd_line = line
            break

    if pd_line:
        items = pd_line.split()
        Pd_natural_population = float(items[-1])
    else:
        Pd_natural_population = None

    return Pd_natural_population
    
def extract_Fukui_Fun(subdir):
    if os.path.isdir(subdir):
        frag1_path = os.path.join(subdir, Frag_1_pop)
        frag1_cat_path = os.path.join(subdir, Frag_1_Cat_pop)
        frag1_ani_path = os.path.join(subdir, Frag_1_Ani_pop)

        if os.path.isfile(frag1_path) and os.path.isfile(frag1_cat_path) and os.path.isfile(frag1_ani_path):
            frag1_Pd_pop = extract_NBO_pop(open(frag1_path).read())
            frag1_cat_Pd_pop = extract_NBO_pop(open(frag1_cat_path).read())
            frag1_ani_Pd_pop = extract_NBO_pop(open(frag1_ani_path).read())

            if all((frag1_Pd_pop, frag1_cat_Pd_pop, frag1_ani_Pd_pop)):
                Electrophilicity = frag1_ani_Pd_pop - frag1_Pd_pop
                Nucleophilicity = frag1_Pd_pop - frag1_cat_Pd_pop
                Radical_attack_susceptibility = (frag1_ani_Pd_pop - frag1_cat_Pd_pop)*0.5
            else:
                Electrophilicity = None
                Nucleophilicity = None
                Radical_attack_susceptibility = None

            return Electrophilicity, Nucleophilicity, Radical_attack_susceptibility

    return None, None, None