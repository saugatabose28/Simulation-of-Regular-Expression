#!/usr/bin/env python

#!/usr/local/bin/python3

#A test file for various dfa's and operations
#Not very well organized... See the example.py for an example

from dfa_min import *
from dfa import *
from nfa import *
#from nfa_operations import *
#from reparse import *

def main():    
  
    Q2 = {'S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6'}

    Sigma2 = {'0','1'}
    
    Delta2 = { ('S0', '')  : { 'S1' },
               ('S0', '0') : { 'S0' },
               ('S0', '1') : { 'S0', 'S5' },
               ('S1', '0') : { 'S2' },
               ('S2', '0') : { 'S3' },
               ('S2', '1') : { 'S3' },
               ('S3', '0') : { 'S4' },
               ('S3', '1') : { 'S4' },
               ('S5', '0') : { 'S6' },
               ('S5', '1') : { 'S6' } }
    
    q02 = 'S0'
    
    F2 = {'S4', 'S6'}
    
    print "NFA Representation is: "
    NFA2 = mk_nfa(Q2, Sigma2, Delta2, q02, F2)
    prnfa(NFA2)
    
    print "NFA to DFA Representation is: "
    DNFA2 = nfa2dfa(NFA2)
    prdfa(DNFA2)
    
    print "Minimum DFA Representation is: "
    minDTree3 = minDFA(DNFA2, 'verbose')
    prdfa(minDTree3)
    
    print "GNFA Representation is: "
    G2 = mk_gnfa_N(NFA2)
    prdfa(G2)    

if __name__ == "__main__":
    main()

    

