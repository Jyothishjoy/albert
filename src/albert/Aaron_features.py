import os
import numpy as np
from AaronTools.finders import BondedElements
from AaronTools.finders import BondedTo, WithinRadiusFromAtom, NotAny
from AaronTools.internal_coordinates import Bond
from AaronTools.geometry import Geometry
from AaronTools.component import Component
from AaronTools.fileIO import FileReader, read_types
from albert.file_names import Complex_xyz, Frag_1_xyz

def get_lig_atom_indicies(subdir):
    xyz_file_path = os.path.join(subdir, Frag_1_xyz)
    
    Atom1 = None
    Atom2 = None
    Atom3 = None
    Avg_D = None
    LML_Angle = None

    geom = Geometry(xyz_file_path, refresh_connected=True, refresh_ranks=False)
    metal = geom.find("Pd")[0]
    candidates = geom.find(WithinRadiusFromAtom(metal, 4.0), NotAny(metal))

    coords = geom.coordinates(candidates)

    distances = np.linalg.norm(coords - metal.coords, axis=1)
    d1, d2, d3 = np.partition(distances, 2)[:3]
    
    # Extract the elemental symbol of the atoms connected to the metal
    atom1 = candidates[np.where(distances == d1)[0][0]]
    Atom1 = atom1.element
    atom2 = candidates[np.where(distances == d2)[0][0]]
    Atom2 = atom2.element
    atom3 = candidates[np.where(distances == d3)[0][0]]
    Atom3 = atom3.element
    
    # Extract the average bond length of M-L bonds
    d1 = metal.dist(atom1)
    d2 = metal.dist(atom2)
    d3 = metal.dist(atom3)
    Avg_D = np.mean([d1, d2, d3])

    # Extract Largest Angle between the L-M-L connection
    angle1 = metal.angle(atom1, atom2)
    angle2 = metal.angle(atom2, atom3)
    angle3 = metal.angle(atom1, atom3)
    largest_angle = np.rad2deg(np.max([angle1, angle2, angle3]))
    LML_Angle = largest_angle
    
    return Atom1, Atom2, Atom3, Avg_D, LML_Angle
    
def get_sterimol(subdir):
    xyz_file_path = os.path.join(subdir, Complex_xyz)
    
    B1 = None
    B2 = None
    B3 = None
    B4 = None
    B5 = None
    L = None

    geom = Geometry(xyz_file_path, refresh_connected=True, refresh_ranks=False)
    metal = geom.find("Pd")[0]

    candidates = geom.find(WithinRadiusFromAtom(metal, 4.0), NotAny(metal))

    coords = geom.coordinates(candidates)

    distances = np.linalg.norm(coords - metal.coords, axis=1)
    d1, d2, d3, d4 = np.partition(distances, 3)[:4]
    
    # Extract the elemental symbol of the atoms connected to the metal
    atom1 = candidates[np.where(distances == d1)[0][0]]
    atom2 = candidates[np.where(distances == d2)[0][0]]
    atom3 = candidates[np.where(distances == d3)[0][0]]
    atom4 = candidates[np.where(distances == d4)[0][0]]

    methyl = geom.find("C", BondedElements("H", "H", "H", match_exact=False), [atom1, atom2, atom3, atom4])[0]
    not_methyl = geom.find([atom1, atom2, atom3, atom4], NotAny(methyl))
    L_axis = methyl.bond(metal)
    ligand_atoms = set([])
    for atom in not_methyl:
        ligand_atoms.update(geom.get_fragment(atom, stop=metal))

    sterimol = geom.sterimol(L_axis=L_axis, start_atom=metal, targets=NotAny(metal), radii="umn")
    B1 = sterimol['B1']
    B2 = sterimol['B2']
    B3 = sterimol['B3']
    B4 = sterimol['B4']
    B5 = sterimol['B5']
    L = sterimol['L']

    return B1, B2, B3, B4, B5, L
    

def get_buried_volume(subdir):
    xyz_file_path = os.path.join(subdir, Frag_1_xyz)
    
    Buried_Volume_3 = None
    Buried_Volume_4 = None
    Buried_Volume_5 = None
    Buried_Volume_6 = None

    infile = FileReader(xyz_file_path)
    geom = Geometry(infile, refresh_connected=True, refresh_ranks=False)
    metal = geom.find("Pd")

    Buried_Volume_3 = geom.percent_buried_volume(metal, radius=3.0, radii='umn')
    Buried_Volume_4 = geom.percent_buried_volume(metal, radius=4.0, radii='umn')
    Buried_Volume_5 = geom.percent_buried_volume(metal, radius=5.0, radii='umn')
    Buried_Volume_6 = geom.percent_buried_volume(metal, radius=6.0, radii='umn')

    return Buried_Volume_3, Buried_Volume_4, Buried_Volume_5, Buried_Volume_6

   
def get_cone_angle(subdir):
    xyz_file_path = os.path.join(subdir, Frag_1_xyz)
    
    Cone_Angle = None

    infile = FileReader(xyz_file_path)
    geom = Geometry(infile, refresh_connected=True, refresh_ranks=False)
    metal = geom.find("Pd")[0]

    ligand_atoms = geom.find(NotAny(metal))

    comp = Component(ligand_atoms)
    key_atoms = comp.find(BondedTo(metal)) # or something else to determine the coordinating atoms
    for k in key_atoms:
        k.tags.add("key")
    Cone_Angle = comp.cone_angle(center=metal, method='exact', radii='umn')

    return Cone_Angle
   
   
def get_ligand_solid_angle(subdir):
    xyz_file_path = os.path.join(subdir, Frag_1_xyz)
    
    Solid_Angle = None

    infile = FileReader(xyz_file_path)
    geom = Geometry(infile, refresh_connected=True, refresh_ranks=False)
    metal = geom.find("Pd")[0]

    ligand_atoms = geom.find(NotAny(metal))

    comp = Component(ligand_atoms)
    Solid_Angle = comp.solid_angle(center=metal, radii='umn', grid=5810, return_solid_cone=True)  # Return solid_cone angle in degrees insted of steradians
              
    return Solid_Angle
    
    
