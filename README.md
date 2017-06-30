# Simulation-of-Regular-Expression
The following Operations are being performed:
	1. RE to NFA
	2. NFA to DFA
	3. DFA to minimum DFA
	4. NFA to GNFA

Regular Expression to NFA:
	1. Run reToNfa.py
	2. Input infix string. (example: (a+b)*.(b+c))
	3. Here, OR='+', CONCAT='.',STAR='*'
	4. You will be shown the fllowing outputs:
		. The transition paths
		. Initial State
		. No. of States
		. Alphabets

NFA2DFA, DFA2minimumDFA,NFA2GNFA:
	1. Run main.py
	2. We are using static input here.The transtion table is already given as input

Reference for "NFA2DFA, DFA2minimumDFA,NFA2GNFA":

1. "Modeling and Reasoning about Computation:Theory and Applications of Automata, Languages, Undecidability,BDD, SAT, and SMT Methods through Declarative Programming" by Ganesh Gopalakrishnan and Tyler Sorensen,September 17, 2013
2.Introduction to the Theory of Computation, [Sipser, 2006],Second Edition
