# About the project
Scpyce is an SQL based structural engineering solver in Python for 3d systems. Each model built is stored as an SQLite database which is read by the solver which solves the stiffness matrix for the model and saves resuls back in the database. 

_For more information on the project structure, please refer to the [Documentation](https://github.com/nicbencini/scpyce/tree/main/docs)_.

# The solver
The model database is compiled into a global stiffness matrix (Kp), structural stiffness matrix (Ks) and force vector {Fv}. The deflections of the system are obtained by solving the structural stiffness with the force vector to obtain the displacement vector {d}. This solver relies on the numpy linalg library which computes the exact solution, x, of the well-determined i.e. full rank, linear matrix equation ax = b. The resulting vector contains a value for the displacement or rotation for each degree of freedom for each node. All other structural results are then derived from this resultant displacement vector.

Limitations:
Since this solver relies on the numpy library, the global stiffness matrix is constructed as a dense matrix which is very memory intensive for larger matrices. To prevent using too much RAM the solver will throw a runtime error if the global stiffness matrix size exceeds 1 GB.

Sign Convention:
- Positive values represent upward forces
- Negative values represent downward forces
- Clockwise moments are positive moments
- Counter Clockwise moments are negative moments

Units:
- Force: kN
- Moment: KNm
- Distance: m
- Area: m^2
- Density kN/m^3
- Moment of inertia: m^4
- Youngs Modulus: MPa
- Embodied carbon: kgCO2e/m^3
- Coefficient of thermal expansion : 1/c

# Getting started
_For examples on how to use the solver, please refer to the [Examples](https://github.com/nicbencini/scpyce/tree/main/examples)_.

# Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

# License
Distributed under the GPL-3.0 License. See LICENSE.txt for more information.

# Contact
Email: nicbencini@gmail.com
LinkedIn: [Nicolo Bencini](https://www.linkedin.com/in/nicolo-bencini/)
