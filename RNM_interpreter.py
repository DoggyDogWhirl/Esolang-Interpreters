code="""code goes here"""
import sys

code=code.split()
vardict={}
for i in range(len(code)):
  for sym in "+-*/%^=IOCG":
    if sym in code[i]:
      code[i]=code[i].split(sym)
      if sym in "+-*/%^=":
        assert len(code[i]) == 2, "Expressions may have only one operation"
      if sym in "IOCG":
        assert code[i][0] == "", i+" does not use an initial variable"
        del code[i][0]
      code[i].insert(0,sym)
  try:
    for num in [1,2]:
      s=1
      if code[i][num][0]=="_":
        s=-1
        code[i][num]=code[i][num][1:]
      code[i][num]=s*eval(code[i][num])
      vardict[code[i][num]]=code[i][num]
  except IndexError:
    pass

cp=0
while cp<len(code):
  if code[cp][0] == "+": vardict[code[cp][1]]  += vardict[code[cp][2]]
  if code[cp][0] == "-": vardict[code[cp][1]]  -= vardict[code[cp][2]]
  if code[cp][0] == "*": vardict[code[cp][1]]  *= vardict[code[cp][2]]
  if code[cp][0] == "/": vardict[code[cp][1]]  /= vardict[code[cp][2]]
  if code[cp][0] == "%": vardict[code[cp][1]]  %= vardict[code[cp][2]]
  if code[cp][0] == "^": vardict[code[cp][1]] **= vardict[code[cp][2]]
  if code[cp][0] == "=": vardict[code[cp][1]]   = vardict[code[cp][2]]
    
  if code[cp][0] == "I": vardict[code[cp][1]] = ord(sys.stdin.read(1))
  if code[cp][0] == "O": print(        vardict[code[cp][1]]  ,end="")
  if code[cp][0] == "C": print(chr(int(vardict[code[cp][1]])),end="")
  if code[cp][0] == "G":
    if int(vardict[code[cp][1]]) > 0: cp = int(vardict[code[cp][1]]//1-2)
  cp+=1
