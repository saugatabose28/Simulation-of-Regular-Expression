#!/usr/bin/env python


import sys
from languages import *
from dfa import *

from functools import reduce

#def fst(p):
  #  return p[0]

#def snd(p):
 #   return p[1]

def fn_dom(F):
    return {k for k in F.keys()}

#def fn_range(F):
 #   return {v for v in F.values()}

def mk_nfa(Q, Sigma, Delta, q0, F):
    assert(Sigma != {})
    assert("" not in Sigma)  # We don't allow epsilon in any alphabet (except for a GNFA)
    assert(q0 in Q)
    assert(set(F) <= Q)
    assert(fn_dom(Delta) <= product(Q, Sigma | {""}))
    
    for x in list(Delta.values()):
        assert(set(x) <= Q)
    
    return({"Q":Q, "Sigma":Sigma, "Delta":Delta, "q0":q0, "F":F})

def mktot_nfa(N):
    add_delta = { (q,c) : set({}) for q in N["Q"] for c in (N["Sigma"] | {""}) if (q,c) not in N["Delta"] }
    #
    add_delta.update(N["Delta"])
    #
    return {"Q": N["Q"], "Sigma": N["Sigma"], "q0": N["q0"], "F": N["F"], "Delta": add_delta}

def prnfa(N):
        
        Nt = mktot_nfa(N)
        print("")
        print("Q:", Nt["Q"])
        print("Sigma:", Nt["Sigma"])
        print("q0:", Nt["q0"])
        print("F:", Nt["F"])
        print("Delta:")
        print("\t\t".join(map(str, Nt["Q"])))
        print("-------------------------------------------------------------------------------------------------------------------")
        for c in (Nt["Sigma"] | {""}):
            nxt_qs = [Nt["Delta"][(q, c)] for q in Nt["Q"]]
            print("\t".join(map(str, nxt_qs)) + "\t\t\t" + c)
            print("")

def step_nfa(N, q, c):
    
    assert(c in (N["Sigma"] | {""}))
    assert(q in N["Q"])
    if (q,c) in N["Delta"].keys():
        return N["Delta"][(q,c)]
    else:
        return set({})

def ech(Allsofar, Previous, N):
    
    if (Allsofar == Previous):
        return Allsofar
    else:
        all_state_sets_one_eps_away = list(map(lambda q: step_nfa(N, q, ""), Allsofar))
        all_states_one_eps_away = reduce(lambda x, y: set(x) | set(y), all_state_sets_one_eps_away + [ set({}) ] )
        return ech(set(all_states_one_eps_away) | set(Allsofar), Allsofar, N)
    
def eclosure(Q, N):
    return ech(Q, set({}), N)

def ec_step_nfa(Q, c, N):
    
    Eclosure = eclosure(Q, N)
    
    all_state_sets_one_c_away = list(map(lambda s: step_nfa(N, s, c), Eclosure))

    all_states_one_c_away = reduce(lambda x, y: set(x) | set(y), all_state_sets_one_c_away + [ set({}) ] )
    
    Eclosure_again = eclosure(all_states_one_c_away, N)
    
    return Eclosure_again

def nfa2dfa(N):
    if (N["Sigma"] == set({})):
        print("Can't convert NFA with empty Sigma to a DFA")
        assert(False)
    EC = eclosure({N["q0"]}, N)
    # Qsofar is set to [EC] because we have discovered the 'in's to EC; the outs will
    # be added while returning
    return n2d([EC], [EC], dict({}), N)

def mkSSnam(S):
    if S==set({}):
        return "EMPTYSET"
    else:
        S1 = list(S)
        S1.sort()
        return "".join(map(lambda x: "{" if x=="[" else "}" if x=="]" else x, str(S1))) # to please "dot"

def n2d(FrontQ, Qsofar, Delta, N):
    AllMoves = [ ((Q, c), ec_step_nfa(Q, c, N)) for Q in FrontQ for c in N["Sigma"] ]
    NewMoves = list(filter(lambda QcQ: QcQ[1] not in Qsofar, AllMoves)) 
    
    if NewMoves == []:
        
        AllMovesDelta = dict([ ( (mkSSnam(Qfrom), c), mkSSnam(Qto) ) for ((Qfrom, c), Qto) in AllMoves ])
        Delta.update(AllMovesDelta)
        
        DFA_Q = { mkSSnam(Q) for Q in Qsofar }
        DFA_Sigma = N["Sigma"]
        DFA_Delta = Delta
        DFA_q0 = mkSSnam(eclosure({N["q0"]}, N))
        DFA_F = set(map(lambda Q: mkSSnam(Q), filter(lambda Q: (N["F"] & Q) != set({}), Qsofar)))
      
        return mk_dfa(DFA_Q, DFA_Sigma, DFA_Delta, DFA_q0, DFA_F)
    else:
        newFrontQ = list(map(lambda QcQ: QcQ[1], NewMoves)) 
        newQsofar = Qsofar + newFrontQ
        NewMovesDelta = dict([ ( (mkSSnam(Qfrom), c), mkSSnam(Qto) ) for ((Qfrom, c), Qto) in AllMoves ]) 
        
        Delta.update(NewMovesDelta)
        return n2d(newFrontQ, newQsofar, Delta, N)

    
def mk_gnfa_N(N):
  
    GNFA_delta = { ("Real_I","") : {N["q0"]} }
    
    GNFA_delta.update(N["Delta"])
    
    for f in N["F"]:
        if (f,"") in N["Delta"]:
            GNFA_delta.update( { (f, ""): (N["Delta"][(f, "")] | set({ "Real_F" })) } )
        else:
            GNFA_delta.update( { (f, ""): { "Real_F" } } )
    #
    return { "Q" : (N["Q"] | {"Real_I"} | {"Real_F"}),
             "Sigma" : N["Sigma"],
             "Delta" : GNFA_delta,
             "q0" : "Real_I",
             "F" : {"Real_F"} }

