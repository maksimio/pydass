# About
This repository is a module of the [alternatives ranking system](http://mcodm.ru/theory/Podinovski%202019.pdf) based on the methods of V.V. Podinovksiy ([DASS program](http://mcodm.ru/soft/dass/)). 
This system uses a method of sequential preference refinement. 
It consists of gradually eliminating options and increasing the rigor of their evaluation methods.

## Compliance of functions with theoretical calculations
Algorithms for clarifying preferences were implemented using the [manual](http://mcodm.ru/theory/Podinovski%202019.pdf). The table below maps code sections to manual theory for better understanding.

| №  | Preference clarification stage    | Code                                                                                    | V.V. Porinovski textbook (ISBN 978-5-02-040241-6) |
|----|-----------------------------------|-----------------------------------------------------------------------------------------|---------------------------------------------------|
| 1  | Edgeworth-Pareto method           | `def pareto(variants: list[Variant]):`                                                    | §1.2, point 3                                     |
| 2  | Qualitative importance (QI)       | `def quality_domination(variants: list[Variant]...):`                                     | §2.5                                              |
| 3  | QI: criteria importance vector    | `for imp in importances:`                                                                 | formula 2.6                                       |
| 4  | QI: sort importance vector        | `for pos, value in zip(importance.positions, importance_vector):`                         | formula 2.3                                       |
| 5  | QI: B^Omega matrix                | `v.matrix = quality_domination_matrix(v.scores, importance_vector_new, scale.gradeCount)` | formula 2.4 and table 2.2 (last row)              |
| 6  | QI: B^Omega matrix comparison     | `res = v1.matrix - v2.matrix`                                                             | formula 2.5                                       |
| 7  | Count importance (CI)             | `def count_domination(variants: list[Variant]...):`                                       | §3.3 (example)                                    |
| 8  | CI: N-model                       | `n_model.append(coefs[i] * n_model[i])`                                                   | §3.1 (theory), point 2 (begin)                    |
| 9  | CI: long scores from N-model      | `for n, s in zip(n_model, v.scores):`                                                     | §3.1, point 2 (end)                               |
| 10 | CI: Pareto for sorted long scores | `for i in range(len(b.long_scores)):`                                                     | §3.3, point 1 (begin)                             |

# Persons
The main contributor of the project is Maxim A. Lopatin, a student of SPbPU ICSC.

The advisor and minor contributor is Vladimir A. Parkhomenko a seniour lecturer of SPbPU ICSC. 

# Structure
The dass.py file contains the algorithms. 
The main.py file contains the reading of the data and the order in which the algorithms are applied. 
The input directory contains two examples of XML input data from the DASS program.

# Warranty
The contributors give no warranty for the using of the software.

# License
This program is open to use anywhere and is licensed under the MIT license.
