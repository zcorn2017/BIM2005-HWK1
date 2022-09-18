# This script aims to facilitate the gerneration of the documentation
# which is not part of the main program.
# For the homework solution,
# pls refer to torsion_angle.py

import sys

# Add heading to the Markdown file
def mkdoc_heading(heading, level=1):
    heading_level = "#" * level + " " + heading + "\n"
    print(f"""
{heading_level}""")

# Wrap the code to make it be recognised by the Markdown parser
def wrap_code(code, lang="python"):
    print(f"""```{lang}
{code}
    ```""")

# Redirect the output to the file writing object.
with open("XYZ_GAMAT_SUMMARY.md","w") as sys.stdout:
    for angle in range(0, 380, 20):
        mkdoc_heading(f"Torsion Angle at {angle}$\degree$", level= 4)

        print(f"\n- ./CODE/C2H4Cl2_{angle}_degrees.gzmat\n")
        with open(f"./CODE/C2H4Cl2_{angle}_degrees.gzmat", "r")  as gzmat:
            wrap_code(gzmat.read(), lang="gzmat")

        print(f"\n- ./CODE/C2H4Cl2_{angle}_degrees.xyz\n")
        with open(f"./CODE/C2H4Cl2_{angle}_degrees.xyz", "r") as xyz:
            wrap_code(xyz.read(), lang="xyz")
