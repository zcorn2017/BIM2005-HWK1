# This the main program to process the molecule.

from openbabel import openbabel
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set the constant used to convert kCal/mol to kJ/mol
KCAL2KJ_CONSTANT = 4.184

# The C2H4Cl2 molecule with the torsion angle at 0 degree
gzmat_code = """
#

C2H4Cl2

0 1
C
C 1 1.54
H 1 1.0 2 109.5
H 1 1.0 2 109.5 3 120.0
Cl 1 1.67 2 109.5 4 120.0
H 2 1.0 1 109.5 5 -120.0
H 2 1.0 1 109.5 5 120.0
Cl 2 1.67 1 109.5 5 0.0
"""

# Store the code of the 18 modified molecules as a list
code_list = []

for n in range(0, 19):
    # Count the reference number of the atoms to determine which atom to manipulate
    atom_counter = 0

    # .xyz code after conversion
    code_aft_cnv = ""
    for line in gzmat_code.split("\n"):
        words = line.split()

        # if the line is empty, do not make modifications
        if len(words) == 0:
            pass

        # if the title is met, rename the title to mark it with the torsion angle
        elif line.startswith("C2H4Cl2"):
            words.append(str(20 * n))
            words.append("degrees")
            code_aft_cnv = code_aft_cnv + "-".join(words) + "\n"
            continue

        elif words[0].isalpha() and len(words[0]) in [1, 2]:
            atom_counter = atom_counter + 1

            if atom_counter in [6, 7, 8]:

                words[-1] = str(float(words[-1]) + 20 * n)
                if float(words[-1]) >= 360:
                    words[-1] = str(float(words[-1]) - 360)

        code_aft_cnv = code_aft_cnv + " ".join(words) + "\n"
    code_list.append(code_aft_cnv)

# Write the code to the .gzmat format
for code, angle in zip(code_list, range(0, 380, 20)):
    with open(f"./CODE/C2H4Cl2_{angle}_degrees.gzmat", "w") as gzmat_file:
        gzmat_file.write(code)

# Set the input format to gzmat and the output format to xyz
OB_converter = openbabel.OBConversion()
OB_converter.SetInAndOutFormats("gzmat", "xyz")

MMFF94_abs_energy_in_Kcal_list = []
GAFF_abs_energy_in_KJ_list = []

# Convert the .gzmat files to .xyz file via OpenBabel
for angle in range(0, 380, 20):
    mol_C2H4Cl2 = openbabel.OBMol()

    # Use MMFF94 and GAFF to calculate the absolute energy
    OB_converter.ReadFile(mol_C2H4Cl2, f"./CODE/C2H4Cl2_{angle}_degrees.gzmat")

    MMFF94_forcefield = openbabel.OBForceField.FindForceField("MMFF94")
    GAFF_forcefield = openbabel.OBForceField.FindForceField("GAFF")

    # Redirect the log output to std::cout
    MMFF94_forcefield.SetLogToStdOut()
    GAFF_forcefield.SetLogToStdOut()

    # Set the priority of log to high
    MMFF94_forcefield.SetLogLevel(openbabel.OBFF_LOGLVL_HIGH)
    GAFF_forcefield.SetLogLevel(openbabel.OBFF_LOGLVL_HIGH)

    # Specify the molecule we calculate the energy of
    MMFF94_forcefield.Setup(mol_C2H4Cl2)
    GAFF_forcefield.Setup(mol_C2H4Cl2)

    # Energy of C_2H_4Cl_2 with Torsion Angle at `angle` Degrees Starts
    # by MMFF94
    MMFF94_abs_energy_in_Kcal = MMFF94_forcefield.Energy()
    # by GAFF
    GAFF_abs_energy_in_KJ = GAFF_forcefield.Energy()

    MMFF94_abs_energy_in_Kcal_list.append(MMFF94_abs_energy_in_Kcal)
    GAFF_abs_energy_in_KJ_list.append(GAFF_abs_energy_in_KJ)

    OB_converter.WriteFile(mol_C2H4Cl2, f"./CODE/C2H4Cl2_{angle}_degrees.xyz")

# Construct a table containing the information required by the question
ref_MMFF94_energy_in_Kcal = min(MMFF94_abs_energy_in_Kcal_list)
ref_GAFF_energy_in_KJ = min(GAFF_abs_energy_in_KJ_list)

MMFF94_abs_energy_in_Kcal_vec = np.array(MMFF94_abs_energy_in_Kcal_list)
GAFF_abs_energy_in_KJ_vec = np.array(GAFF_abs_energy_in_KJ_list)

MMFF94_abs_energy_in_KJ_vec = KCAL2KJ_CONSTANT * MMFF94_abs_energy_in_Kcal_vec
GAFF_abs_energy_in_Kcal_vec = GAFF_abs_energy_in_KJ_vec / KCAL2KJ_CONSTANT

MMFF94_rel_energy_in_Kcal_vec = MMFF94_abs_energy_in_Kcal_vec - ref_MMFF94_energy_in_Kcal
GAFF_rel_energy_in_KJ_vec = GAFF_abs_energy_in_KJ_vec - ref_GAFF_energy_in_KJ

MMFF94_rel_energy_in_KJ_vec = MMFF94_abs_energy_in_KJ_vec - KCAL2KJ_CONSTANT * ref_MMFF94_energy_in_Kcal
GAFF_rel_energy_in_Kcal_vec = GAFF_abs_energy_in_Kcal_vec - ref_GAFF_energy_in_KJ / KCAL2KJ_CONSTANT

data_in_Kcal_dict = {
    "Absolute Energy (kcal/mol) by MMFF94" : MMFF94_abs_energy_in_Kcal_vec.tolist(),
    "Absolute Energy (kcal/mol) by GAFF" : GAFF_abs_energy_in_Kcal_vec.tolist(),
    "Relative Energy (kcal/mol) by MMFF94" : MMFF94_rel_energy_in_Kcal_vec.tolist(),
    "Relative Energy (kcal/mol) by GAFF" : GAFF_rel_energy_in_Kcal_vec.tolist()
}
data_in_KJ_dict = {
    "Absolute Energy (kJ/mol) by MMFF94" : MMFF94_abs_energy_in_KJ_vec.tolist(),
    "Absolute Energy (kJ/mol) by GAFF" : GAFF_abs_energy_in_KJ_vec.tolist(),
    "Relative Energy (kJ/mol) by MMFF94" : MMFF94_rel_energy_in_KJ_vec.tolist(),
    "Relative Energy (kJ/mol) by GAFF" : GAFF_rel_energy_in_KJ_vec.tolist()
}

data_in_Kcal_df = pd.DataFrame(data_in_Kcal_dict,index=[angle for angle in range(0, 380, 20)])
data_in_KJ_df = pd.DataFrame(data_in_KJ_dict,index=[angle for angle in range(0, 380, 20)])

data_in_Kcal_df.to_csv("./DATA/data_in_Kcal.csv")
data_in_KJ_df.to_csv("./DATA/data_in_KJ.csv")

data_dict = {
    "Absolute Energy (kcal/mol) by MMFF94": np.round(MMFF94_abs_energy_in_Kcal_vec.tolist(), 3),
    "Absolute Energy (kcal/mol) by GAFF": np.round(GAFF_abs_energy_in_Kcal_vec.tolist(), 3),
    "Relative Energy (kcal/mol) by MMFF94": np.round(MMFF94_rel_energy_in_Kcal_vec.tolist(), 3),
    "Relative Energy (kcal/mol) by GAFF": np.round(GAFF_rel_energy_in_Kcal_vec.tolist(), 3),
    "Absolute Energy (kJ/mol) by MMFF94": np.round(MMFF94_abs_energy_in_KJ_vec.tolist(), 3),
    "Absolute Energy (kJ/mol) by GAFF": np.round(GAFF_abs_energy_in_KJ_vec.tolist(), 3),
    "Relative Energy (kJ/mol) by MMFF94": np.round(MMFF94_rel_energy_in_KJ_vec.tolist(), 3),
    "Relative Energy (kJ/mol) by GAFF": np.round(GAFF_rel_energy_in_KJ_vec.tolist(), 3)
}

data_df = pd.DataFrame(data_dict, index=[angle for angle in range(0, 380, 20)])
data_df.index.name = "Angle (degree)"
data_df.to_csv("./DATA/data.csv")

# Plot the lineplot of relative energy in kcal/mol with respect to angle in degrees
lineplot_df = data_df.loc[:,["Relative Energy (kcal/mol) by MMFF94","Relative Energy (kcal/mol) by GAFF"]]
sns.lineplot(data=lineplot_df)

plt.savefig("rel_energy.png")
