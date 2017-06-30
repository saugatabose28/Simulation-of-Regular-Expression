#!/usr/bin/env python


def fst(p):
     return p[0]

def snd(p):
       return p[1]

def fn_dom(F):
    return {k for k in F.keys()}

def fn_range(F):
    return {v for v in F.values()}

def mk_dfa(Q, Sigma, Delta, q0, F):
    
    assert(Sigma != {})
    
    assert("" not in Sigma)
    
    dom = fn_dom(Delta)
    states_dom = set(map(fst,dom))
    input_dom = set(map(snd,dom))
    state_targ = set(fn_range(Delta))
    
    assert(states_dom == Q)
    assert(input_dom == Sigma)
    
    assert(len(Delta)==len(Q)*len(Sigma))
    
    assert((state_targ <= Q)&(state_targ != {}))
    
    assert(q0 in Q)
    
    assert(set(F) <= Q)
    
    return({"Q":Q, "Sigma":Sigma, "Delta":Delta, "q0":q0, "F":F})

def mkp_dfa(Q, Sigma, Delta, q0, F):

    assert(Sigma != {})
    # Targets must be in Q and non-empty
    # Initial state in Q
    assert(q0 in Q)
    # Final states subset of Q (could be empty, could be Q)
    assert(set(F) <= Q)
    # If all OK, return DFA as a dict
    return({"Q":Q, "Sigma":Sigma, "Delta":Delta, "q0":q0, "F":F})

def mktot(D):

    add_delta = { (q,c) : "BH" for q in D["Q"] for c in D["Sigma"] if (q,c) not in D["Delta"] }
    
    #print("<add_delta")
    print(add_delta)
    #print("add_delta>")
    #
    bh_moves =  { ("BH", c): "BH" for c in D["Sigma"] }
    #
    add_delta.update(bh_moves)
    #
    #print(add_delta)
    #
    add_delta.update(D["Delta"])
    #
    return {"Q": D["Q"] | { "BH" }, "Sigma": D["Sigma"], "q0": D["q0"], "F": D["F"], "Delta": add_delta}

def prdfa(D):
      
        Dt = mktot(D)
        # print(totdfa)
        #print("")
        print("Q:", Dt["Q"])
        print("Sigma:", Dt["Sigma"])
        print("q0:", Dt["q0"])
        print("F:", Dt["F"])
        print("Delta:")
        print("\t".join(map(str,Dt["Q"])))
        print("----------------------------------------------------------------------------------------")
        for c in (Dt["Sigma"]):
            nxt_qs = [Dt["Delta"][(q, c)] for q in Dt["Q"]]
            print("\t".join(map(str, nxt_qs)) + "\t" + c)
            print("")
