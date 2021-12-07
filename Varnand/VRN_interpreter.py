import sys

code="""code goes here"""

vardict=dict(zip("abcdefghijklmnopqrstuvwxyz",[0]*26))
pnt=-1

def vareval(n): # evals int, hex string digit, var
    if isinstance(n,int):       return n
    if n in "0123456789ABCDEF": return int(n,16)
    if n in vardict:            return vardict[n]

def nand(x,y): # !
    x=vareval(x)
    y=vareval(y)
    return 255-(x&y)

def redefine(strvar,newnum): # =
    assert strvar in "abcdefghijklmnopqrstuvwxyz","Attempted to redefine non-variable"
    newnum=vareval(newnum)
    vardict[strvar]=newnum
    return newnum

def rotate(num,rot): # %
    num=vareval(num)
    t=2**(8-rot%8)
    return (num%t)*int(256/t)+num//t

def oprint(num): # O
    num=vareval(num)
    print(num,end="")
    return num

def pprint(num): # P
    num=vareval(num)
    print(chr(num),end="")
    return num

def func():
    global pnt
    pnt+=1
    
    if   code[pnt]=="!":  return nand(func(),func())
    elif code[pnt]=="=":  return redefine(func(),func())
    elif code[pnt]=="%":  return rotate(func(),func())
    elif code[pnt]=="O":  return oprint(func())
    elif code[pnt]=="P":  return pprint(func())
    elif code[pnt]=="I":  return ord(sys.stdin.read(1))
    
    elif code[pnt] in "0123456789ABCDEF":           return int(code[pnt],16)
    elif code[pnt] in "abcdefghijklmnopqrstuvwxyz": return code[pnt]
    
    else:
        if pnt<len(code)-1:
            return func()   # comments

while pnt < len(code)-1:
  func()
