import sys

DDRcode="""code goes here"""
DDRcode=DDRcode.split("\n")
if not all(arrow in DDRcode[0] for arrow in "<v^>"):
 raise SyntaxError('Code does not start with "<v^>"')
DDRcode=DDRcode[1:] #removing initial <v^>

ncode=[0]*len(DDRcode)
for i in range(len(DDRcode)): #convert lines to numbers
  if "<" in DDRcode[i]: #note: only detects if each symbol
    ncode[i]+=8         #is in each line, thus lines do not
  if "v" in DDRcode[i]: #need to exactly match commands,
    ncode[i]+=4         #and allows comments
  if "^" in DDRcode[i]:
    ncode[i]+=2
  if ">" in DDRcode[i]:
    ncode[i]+=1

print("DDR Interpreter")
print("Input uses one character at a time, and")
print(" asks again when each character has been used\n")

cp=0
tape=[0]
tp=0
brackets=[]
function=[]
fp=0
var=0

def run_DDR(code,cp,tape,tp,func,fp,brcts,var):
  while cp < len(code):
    if code[cp] == 0: #noop
      pass
    elif code[cp] == 1: # >
      tp+=1
      if tp==len(tape):
        tape+=[0]
    elif code[cp] == 8: # <
      tp-=1
      assert tp>=0, "Attempted to access negative index"
    elif code[cp] == 2: # +
      tape[tp]+=1
      tape[tp]%=256
    elif code[cp] == 4: # -
      tape[tp]-=1
      tape[tp]%=256
    elif code[cp] == 6: # .
      print(chr(tape[tp]), end="")
    elif code[cp] == 12: # ,
      tape[tp]=ord(sys.stdin.read(1))
    elif code[cp] == 10: # [
      if tape[tp]==0:
        while code[cp] != 3:
          if code[cp] == 9:
            cp+=2
          cp+=1
          assert cp < len(code), 'Could not find matching "  v>"'
      else:
        brcts+=[cp-1]
    elif code[cp] == 5: # ]
      cp=brcts[-1]
      del brcts[-1]
    elif code[cp] == 3: # . (num)
      print(tape[tp], end="")
    elif code[cp] == 14: # var=
      var=tape[tp]
    elif code[cp] == 7: # =var
      tape[tp]=var
    elif code[cp] == 9: # "  "
      tape[tp]=code[cp+1]*16+code[cp+2]
      cp+=2
    elif code[cp] == 11: # def func():
      cp+=1
      func=[]
      while code[cp] != 13:
        func+=[code[cp]]
        if code[cp] == 9:
            cp+=2
        cp+=1
        assert cp < len(code), "Could not find function end"
      print(func)
    elif code[cp] == 13: # call func()
      nfunc=[]
      nfp=0
      run_DDR(func,fp,tape,tp,nfunc,nfp,brcts,var)
    elif code[cp] == 15: # halt
      break
    cp+=1

run_DDR(ncode,cp,tape,tp,function,fp,brackets,var)
