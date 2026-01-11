import os
from albert.file_names import Complex, Complex_pop, Frag_1_pop, Frag_1_Cat_pop, Frag_1_Ani_pop, Frag_2_pop
    
def extract_NBO(subdir):
    log_file_path = os.path.join(subdir, Frag_1_pop)
    with open(log_file_path, 'r') as file:
        content = file.read()

        start_marker = "Summary of Natural Population Analysis:"
        end_marker = " NATURAL BOND ORBITAL ANALYSIS"

        start_index = content.rfind(start_marker)
        end_index = content.find(end_marker, start_index)

        if start_index != -1 and end_index != -1:
            section = content[start_index:end_index]

            pd_line = None
            for line in section.split('\n'):
                if 'Pd' in line:
                    pd_line = line
                    break

            if pd_line:
                items = pd_line.split()
                Pd_natural_charge = float(items[2])
                Pd_natural_population = float(items[-1])
            else:
                Pd_natural_charge = None
                Pd_natural_population = None
        else:
            Pd_natural_charge = None
            Pd_natural_population = None

        return Pd_natural_charge, Pd_natural_population

