# Elevatorfuck interpreter
# Original code : https://github.com/pocmo/Python-Brainfuck/blob/master/brainfuck.py
# Modified by DoggyDogWhirl

code="""code goes here"""

import getch 
code="".join([i for i in code if i in "<>^v-.,[]~"])

temp_bracestack, bracemap = [], {}
for position, command in enumerate(code):
  if command == "[": temp_bracestack.append(position)
  if command == "]":
    assert len(temp_bracestack)!=0,"Brackets do not match"
    start = temp_bracestack.pop()
    bracemap[start] = position
    bracemap[position] = start
assert len(temp_bracestack)==0,"Brackets do not match"

cells, celldirs, codeptr, cellptr = [0], [0], 0, 0
while codeptr < len(code):
  command = code[codeptr]
  if command == ">": cellptr += 1
  if cellptr == len(cells): cells.append(0); celldirs.append(0)
  if command == "<": cellptr = 0 if cellptr <= 0 else cellptr - 1
  if command == "^": celldirs[cellptr] = 1
  if command == "v": celldirs[cellptr] = -1
  if command == "-": celldirs[cellptr] = 0
  if command == "[" and cells[cellptr] == 0: codeptr = bracemap[codeptr]
  if command == "]" and cells[cellptr] != 0: codeptr = bracemap[codeptr]
  if command == ".": print(chr(cells[cellptr]),end="")
  if command == ",": cells[cellptr] = ord(getch.getch())
  for i in range(len(cells)):
    cells[i]+=celldirs[i]
    if cells[i] == 256: cells[i] = 0
    if cells[i] == -1: cells[i] = 255
  codeptr += 1
