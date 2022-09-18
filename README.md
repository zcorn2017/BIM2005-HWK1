[TOC]

# BIM2005: Homework I

> In this report, the 'we' term may be preferred by convention rather than by a result of collaboration.

## Overview

- 

## Preparation

- Headers are added to to the .gzmat code as below.

```.gzmat
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
```

## Question 1 & Question 2

### Procedure

Git hub

> Details of implementation could be found 

1. We [added the headers to the code](#Preparation) for it to be recognised by [OpenBabel][]
2. We modify the code in order to change $\tau(Cl^8-C^2-C^1-Cl^{5})$ by $20\times N\degree$.
   - As the reference plane, which is the $2-1-5$ plane, is the same for the last three definitions of atoms, we only need to change the dihedral angles of the last three lines by an increment of $20\degree$.
3. We convert the code via [OpenBabel][] from the .gzmat format to the .xyz. one.
4. During the conversion, we use the python bindings to the OpenBabel C++ library to set up the force field for MMFF94 and GAFF respectively, get the pro
5. We repeat the procedure for $N = 0\dots18$, which means 19 times.



[Avogadro]: https://avogadro.cc
[OpenBabel]:https://openbabel.org
