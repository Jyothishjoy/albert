import os
import numpy as np
from morfeus import SASA, Dispersion, LocalForce, read_xyz, read_geometry
from AaronTools.finders import BondedElements
from AaronTools.finders import BondedTo
from AaronTools.internal_coordinates import Bond
from AaronTools.geometry import Geometry
from AaronTools.fileIO import FileReader
from albert.file_names import Complex_xyz, Frag_1_xyz, fchk_file

def get_sasa(subdir):
    xyz_file_path = os.path.join(subdir, Complex_xyz)
    
    sasa_area = None
    sasa_volume = None

    elements, coordinates = read_xyz(xyz_file_path)
    sasa = SASA(elements, coordinates)
    sasa_area = sasa.area
    sasa_volume = sasa.volume
    
    return sasa_area, sasa_volume
 
 
def get_dispersion_int(subdir):
    xyz_file_path = os.path.join(subdir, Complex_xyz)
    
    surface_area = None
    surface_volume = None
    P_int = None
    P_int_Pd = None

    infile = FileReader(xyz_file_path)
    geom = Geometry(infile, refresh_connected=True, refresh_ranks=False)
    metal = geom.find("Pd")[0]
    metal_id = geom.atoms.index(metal) + 1

    elements, coordinates = read_geometry(xyz_file_path)
    disp = Dispersion(elements, coordinates)
    surface_area = disp.area
    surface_volume = disp.volume
    P_int = disp.p_int
    P_int_Pd = disp.atom_p_int[metal_id]
             
    return surface_area, surface_volume, P_int, P_int_Pd


def get_local_force_constant(subdir):
    fchk_file_path = os.path.join(subdir, fchk_file)
    
    local_FC = None
    local_Freq = None

    infile = FileReader(fchk_file_path)
    geom = Geometry(infile, refresh_connected=True, refresh_ranks=False)
    
    metal = geom.find("Pd")[0]
    methyl_C = geom.find(BondedElements("Pd", "H", "H", "H"), "C")[0]
    metal_id = geom.atoms.index(metal) + 1
    methyl_C_id = geom.atoms.index(methyl_C) + 1

    lf = LocalForce()
    lf.load_file(fchk_file_path, "gaussian", "fchk")
    lf.compute_compliance()
    lf.compute_frequencies()
    local_FC = lf.get_local_force_constant([metal_id, methyl_C_id])
    local_Freq = lf.get_local_frequency([metal_id, methyl_C_id])

    return local_FC, local_Freq
