Requirements: Python 3, numpy

For Windows: 
Run "SAT.bat -Sn input_file.txt" in command prompt.
For Unix based systems:
Run "sh SAT.sh -Sn input_file.txt" in the terminal.

Heuristics:
S1: Random Heuristic
S2: Deterministic Two-Sided Jeroslow-Wang Heuristic
S3: Probabilistic Two-Sided Jeroslow-Wang Heuristic
S4: Deterministic DLIS Heuristic
S5: Probabilistic DLIS Heuristic

For encoding test cases in DIMACS format and sample from different categories, first run translate_examples.py under tests/ and then run samples_tests.py.