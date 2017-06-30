#!/usr/bin/env python

import re
import string
import sys

state=0
nfa_stack=[]
epsilon_matrix=[]
d={}
Q=0
 
postfix = []
temp = []
operator = -10
operand = -20
leftparentheses = -30
rightparentheses = -40
empty = -50

def main():
    global nfa_stack
    global epsilon_matrix
    global state
    global d,Q
    
    t=[]
    k=0    
        
    #print("Input Regular Expresion in Postfix Form: ")
    #ip=raw_input()
    #x=list(ip)
    
    inputExpression()
    print postfix
    
    for i in postfix:
        if i<>'+' and i<>'.' and i<>'*':
            t.append(i)
            k+=1
    t=list(set(t))
    t.append('e')
    print "The Alphabets are: "
    print t
    
    #for i in range(len(t)):
    #    epsilon_matrix.insert(i,[])
    #print epsilon_matrix    
    #for i in range(0,1000):
    #    epsilon_matrix.insert(i,[])
    #print epsilon_matrix
    
    for i in t:
        d[i]=[]
    #for k in d:
    #    print (k,d[k])
    
    r=""
    for i in postfix:
        #print "nfa_stack: "
        #print nfa_stack
        if i<>'+' and i<>'.' and i<>'*':
            #print "previous state: "+(str)(state)
            s=state
            e=state+1
                 
            r=(str)(s)+i+str(e)
            state=state+2
            #print "next state: "+(str)(state)
            nfa_stack.append(r)            
            #print nfa_stack
            #print r
            #if i in d:
            #    d[i].append([e])
            
        elif i=='+':
            if(nfa_stack!=[]):
                a=nfa_stack.pop()
            else:
                print "Stack Underflow"
                break
            if(nfa_stack!=[]):
                b=nfa_stack.pop()      
            else:
                print "Stack Underflow"
                break
            or_(a,b)
            #print"Stack after or is:",
            #print nfa_stack
        elif(i=='.'):
            if(nfa_stack!=[]):
                a=nfa_stack.pop()
            else:
                print "Stack Underflow"
                break
            if(nfa_stack!=[]):
                b=nfa_stack.pop()      
            else:
                print "Stack Underflow"
                break
            concat_(a,b)
            #print"Stack after concatenation is:",
            #print nfa_stack
            #print "state after .: "+(str)(state)
        elif(i=='*'):
            if(nfa_stack!=[]):
                a=nfa_stack.pop()
            else:
                print "Stack Underflow"
                break
            star_(a)
            #print"Stack after klene star is:",
            #print nfa_stack
            #print "state after *: "+(str)(state)
        else:
            print "Wrong Input"  
    print("\n")
    print "Resulting paths: "  
    print nfa_stack
    print "Total States: "
    for i in nfa_stack:
        for j in i:
            k=j
    k1=convertString2List(k)
    k2=extractInegersIntoALst(k1)
    
    Q=max(k2)
    print "%d"%(Q)
    print "The states are: "
    for i in range(0,Q+1):
        print i,
    print "\n"
   
    print "Initial State is: "
    for i in nfa_stack:
        a=lstOfStrngToLstOfChars(i)
    b=extractInegersIntoALst(a)
    print (b[0])
    print "NFA to DFA: Resulting Transitions are:  "
    nfa2dfa()
    
def precedence(s):
    if s is '(':
        return 0
    elif s is '+':
        return 1
    elif s is '*' or '.':
        return 2
    else:
        return 99
                 
def typeof(s):
    if s is '(':
        return leftparentheses
    elif s is ')':
        return rightparentheses
    elif s is '+' or s is '.' or s is '*':
        return operator
    elif s is ' ':
        return empty   
    else :
        return operand
    
def inputExpression():
    infix = raw_input("Enter the infix notation : ")
    for i in infix :
        type = typeof(i)
        if type is leftparentheses :
            temp.append(i)
        elif type is rightparentheses :
            next = temp.pop()
            while next is not '(':
                postfix.append(next)
                next = temp.pop()
        elif type is operand:
            postfix.append(i)
        elif type is operator:
            p = precedence(i)
            while len(temp) is not 0 and p <= precedence(temp[-1]) :
                postfix.append(temp.pop())
            temp.append(i)
        elif type is empty:
            continue
                     
    while len(temp) > 0 :
        postfix.append(temp.pop())
         
    #print "It's postfix notation is ",''.join(postfix)
def nfa2dfa():
    #global d
    #global Q
    #epsilon_closure()
    print Q
    for k in d:
        for i in range(1,(Q+2)):
            d[k].append(-1)
    print d
    return
    
    
def or_(v1,v2):
    
    global state
    s=state
    e=s+1
    state=e+1
    
    if isinstance(v1,list)==True and isinstance(v2,list)==True: #v1=['0a1'] v2=['2b3'],list of string to list of chars
        max1_=0
        min1_=0
        t1=[]
        t2=[]
        r1=[]
        r=""
        
        #print "1. List representation of v1 & v2 is: ",
        a=lstOfStrngToLstOfChars(v2)
        b=lstOfStrngToLstOfChars(v1)
        #print (a,b)
        
        t1=extractInegersIntoALst(a)
        t2=extractInegersIntoALst(b)
        #print t1
        
        start1=t1[0]
        end1=t1[len(t1)-1]
        start2=t2[0]
        end2=t2[len(t2)-1]
        #print "start of 1st list is: %d and end of 1st list is: %d"%(start1,end1)
        #print "start of 2nd list is: %d and end of 2nd list is: %d"%(start2,end2)
        
        r=(str)(s)+'e'+(str)(start1)
        r1.append(r)
        r1.extend(v2)
        t=(str)(end1)+'e'+(str)(e)
        r1.append(t)
        u=(str)(s)+'e'+(str)(start2)
        r1.append(u)
        r1.extend(v1)
        v=(str)(end2)+'e'+(str)(e)
        r1.append(v)
        
        nfa_stack.append(r1)
    elif isinstance(v1,str)==True and isinstance(v2,str)==True: #v1='0a1' v2='2b3',string to list of characters
        max1_=0
        min1_=0
        t1=[]
        t2=[]
        r1=[]
        r=""
        
        a=convertString2List(v2)
        b=convertString2List(v1)
        #print "2. List representation of v1 & v2 is: ",
        #print (a,b)
        
        t1=extractInegersIntoALst(a)
        t2=extractInegersIntoALst(b)
  
        start1=t1[0]
        end1=t1[len(t1)-1]
        start2=t2[0]
        end2=t2[len(t2)-1]
        #print "start of 1st list is: %d and end of 1st list is: %d"%(start1,end1)
        #print "start of 2nd list is: %d and end of 2nd list is: %d"%(start2,end2)
        
        r=(str)(s)+'e'+(str)(start1)
        r1.append(r)
        r1.append(v2)
        t=(str)(end1)+'e'+(str)(e)
        r1.append(t)
        u=(str)(s)+'e'+(str)(start2)
        r1.append(u)
        r1.append(v1)
        v=(str)(end2)+'e'+(str)(e)
        r1.append(v)
        
        nfa_stack.append(r1)
    elif isinstance(v1,str)==True and isinstance(v2,list)==True: #v1='0a1' v2=['2b3']
        max1_=0
        min1_=0
        t1=[]
        t2=[]
        r1=[]
        r=""
        
        a=convertString2List(v1)
        b=lstOfStrngToLstOfChars(v2)
        #print "3. List representation of v1 & v2 is: ",
        #print "v1: %s v2: %s" %(a,b)
        
        t1=extractInegersIntoALst(a)
        t2=extractInegersIntoALst(b)
        
        start1=t1[0]
        end1=t1[len(t1)-1]
        start2=t2[0]
        end2=t2[len(t2)-1]
        #print "start of 1st list is: %d and end of 1st list is: %d"%(start1,end1)
        #print "start of 2nd list is: %d and end of 2nd list is: %d"%(start2,end2)
      
        r=(str)(s)+'e'+(str)(start1)
        r1.append(r)
        
        r1.extend(v2)
        
        t=(str)(end1)+'e'+(str)(e)
        r1.append(t)
        
        u=(str)(s)+'e'+(str)(start2)
        r1.append(u)
       
        r1.append(v1)
        
        v=(str)(end2)+'e'+(str)(e)
        r1.append(v)
      
        nfa_stack.append(r1)
    elif isinstance(v1,list)==True and isinstance(v2,str)==True: #v1='0a1' v2=['2b3']
        max1_=0
        min1_=0
        t1=[]
        t2=[]
        r1=[]
        r=""
        
        a=convertString2List(v2)
        b=lstOfStrngToLstOfChars(v1)
        #print "4. List representation of v1 & v2 is: ",
        #print "v1: %s v2: %s" %(a,b)
        
        t1=extractInegersIntoALst(a)
        t2=extractInegersIntoALst(b)
        
        start1=t1[0]
        end1=t1[len(t1)-1]
        start2=t2[0]
        end2=t2[len(t2)-1]
        #print "start of 1st list is: %d and end of 1st list is: %d"%(start1,end1)
        #print "start of 2nd list is: %d and end of 2nd list is: %d"%(start2,end2)
        
        r=(str)(s)+'e'+(str)(start1)
        r1.append(r)
        r1.append(v2)
        t=(str)(end1)+'e'+(str)(e)
        r1.append(t)
        u=(str)(s)+'e'+(str)(start2)
        r1.append(u)
        r1.extend(v1)
        v=(str)(end2)+'e'+(str)(e)
        r1.append(v)
                          
        nfa_stack.append(r1)    
    
    return
def star_(v1):
    
    global state
    s=state
    e=s+1
    state=e+1
    if(isinstance(v1,str)==True):
        #print "string v1 in star_ is: %s"%(v1)
        r=""
        r1=[]
              
        r=(str)(s)+'e'+(str)(s-2)
        #print r
        r1.append(r)   
        r1.append(v1)
        u=(str)(e-2)+'e'+(str)(e)
        #print u
        r1.append(u)
        s1=(str)(e)+'e'+(str)(s-2)
        #print s
        r1.append(s1)
        t=(str)(s)+'e'+(str)(e)
        #print t
        r1.append(t)
        
        nfa_stack.append(r1)
    elif(isinstance(v1,list)==True):
        #print "list v1 in star_ is: %s"%(v1)
        
        a=lstOfStrngToLstOfChars(v1)
        #print "a: %s"%(a)
        t1=extractInegersIntoALst(a)
        end=t1[len(t1)-1]
        start=t1[0]
        #print "start of 1st list is: %d and end of 2nd list is: %d"%(start,end)
        r=""
        r1=[]
              
        r=(str)(s)+'e'+(str)(start)
        #print r
        r1.append(r)
        r1.extend(v1)
        u=(str)(end)+'e'+(str)(e)
        #print u
        r1.append(u)
        t=(str)(e)+'e'+(str)(start)
        #print u
        r1.append(t)
        w=(str)(s)+'e'+(str)(e)
        #print u
        r1.append(w)

        #r1.append(v1)
        nfa_stack.append(r1)   
    #print r5    
    return
    
def concat_(v1,v2):
    
    #print "Concat: "
    #print "v1: %s v2: %s " %(v1, v2)
    
    #a=convert2SingleList(v1,v2)
    
    if isinstance(v1,str)==True and isinstance(v2,str)==True: #v1='0a1' v2='2b3',string to list of characters
        max1_=0
        min1_=0
        t1=[]
        t2=[]
        r1=[]
        r=""
        
        a=convertString2List(v2)
        b=convertString2List(v1)
        #print "List representation of v1 & v2 is: ",
        #print (a,b)
        
        t1=extractInegersIntoALst(a)
        t2=extractInegersIntoALst(b)

  
        max1_=max(t1)
        min1_=min(t2)
        #print "max of 1st list is: %d and min of 2nd list is: %d"%(max1_,min1_)
        
        r+=(str)(max1_)+'e'+(str)(min1_)
        r1.append(v2)
        r1.append(r)
        r1.append(v1)
        
        nfa_stack.append(r1)
    elif isinstance(v1,list)==True and isinstance(v2,list)==True: #v1=['0a1'] v2=['2b3'],list of string to list of chars
        max1_=0
        min1_=0
        t1=[]
        t2=[]
        r1=[]
        r=""
        
        #print "List representation of v1 & v2 is: ",
        a=lstOfStrngToLstOfChars(v2)
        b=lstOfStrngToLstOfChars(v1)
        #print (a,b)
        
        t1=extractInegersIntoALst(a)
        t2=extractInegersIntoALst(b)
        #print t1
        
        end=t1[len(t1)-1]
        start=t2[0]
        #print "start of 1st list is: %d and end of 2nd list is: %d"%(start,end)
        
        r+=(str)(end)+'e'+(str)(start)
        
        r1.extend(v2)
        r1.append(r)
        r1.extend(v1)
    
        nfa_stack.append(r1)
    elif isinstance(v1,str)==True and isinstance(v2,list)==True: #v1='0a1' v2=['2b3']
        max1_=0
        min1_=0
        t1=[]
        t2=[]
        r1=[]
        r=""
        
        a=convertString2List(v1)
        b=lstOfStrngToLstOfChars(v2)
        #print "a: %s b: %s" %(a,b)
        
        t1=extractInegersIntoALst(a)
        t2=extractInegersIntoALst(b)
        
        end=t2[len(t2)-1]
        start=t1[0]
        
        #print "start of 1st list is: %d and end of 2nd list is: %d"%(start,end)
        
        r+=(str)(end)+'e'+(str)(start)
        
        v2.append(r)
        v2.append(v1)
                
        nfa_stack.append(v2)
    elif isinstance(v1,list)==True and isinstance(v2,str)==True: #v1=['0a1'] v2='2b3'
        max1_=0
        min1_=0
        t1=[]
        t2=[]
        r1=[]
        r=""
        
        a=convertString2List(v2)
        b=lstOfStrngToLstOfChars(v1)
        #print "a: %s b: %s" %(a,b)
        
        t1=extractInegersIntoALst(a)
        t2=extractInegersIntoALst(b)
        
        end=t1[len(t2)-1]
        start=t2[0]
        
        #print "start of 1st list is: %d and end of 2nd list is: %d"%(start,end)
        
        r+=(str)(end)+'e'+(str)(start)
        
        v1.append(r)
        v1.append(v2)
                
        nfa_stack.append(v1)
        
    return
def extractInegersIntoALst(v):    
    t1=[]
    
    for a1 in v:
            #print a1
            try:
                if(int)(a1)>=0 and (int)(a1)<=1000:
                    t1.append((int)(a1))                    
            except:
                pass
    return t1

def lstOfStrngToLstOfChars(a):
    t=[]
    for b in a:
        t.extend(re.split("([^0-9])",b))
    return t   
def convertString2List(v):
    a=[]
    a.extend(re.split("([^0-9])",v))
    return a    
    
if __name__ == "__main__":
    main()