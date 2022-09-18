
import sys

def mkdoc_heading(heading, level=1):
    heading_level = "#" * level + " " + heading + "\n"
    print(f"""
{heading_level}""")


def wrap_code(code, lang="python"):
    print(f"""```{lang}
{code}
    ```""")


with open("XYZ_GAMAT_SUMMARY.md","w") as sys.stdout:
    for angle in range(0, 380, 20):
        mkdoc_heading(f"Torsion Angle at {angle}$\degree$", level= 3)

        mkdoc_heading(f"./CODE/C2H4Cl2_{angle}_degrees.gzmat", level = 4)
        with open(f"./CODE/C2H4Cl2_{angle}_degrees.gzmat", "r")  as gzmat:
            wrap_code(gzmat.read(), lang="gzmat")

        mkdoc_heading(f"./CODE/C2H4Cl2_{angle}_degrees.xyz", level=4)
        with open(f"./CODE/C2H4Cl2_{angle}_degrees.xyz", "r") as xyz:
            wrap_code(xyz.read(), lang="xyz")
