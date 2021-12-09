# Twobrainsfuck interpreter
# Original code : https://github.com/pocmo/Python-Brainfuck/blob/master/brainfuck.py
# Modified by DoggyDogWhirl

code="""code goes here"""

import getch 
code="".join([i for i in code if i in "+-<>[].,#=v^{}:;"])

temp_bracestack, bracemap = [], {}
for position, command in enumerate(code):
  if command in "[{": temp_bracestack.append((position, command))
  if command in "]}":
    assert len(temp_bracestack)!=0,"Brackets do not match"
    start, matchingcommand = temp_bracestack.pop()
    assert (command == "]" and matchingcommand == "[") or (command == "}" and 
matchingcommand == "{"), "Matched two different types of bracket"
    bracemap[start] = position
    bracemap[position] = start
assert len(temp_bracestack)==0,"Brackets do not match"

cells, cells2, codeptr, cellptr, cellptr2 = [0], [0], 0, 0, 0
while codeptr < len(code):
  command = code[codeptr]
  if command == "+": cells[cellptr] += cellptr2
  if command == "-": cells[cellptr] -= cellptr2
  if command == ">": cellptr += 1
  if cellptr == len(cells): cells.append(0)
  if command == "<": cellptr = 0 if cellptr <= 0 else cellptr - 1
  if command == "[" and cells[cellptr] == 0: codeptr = bracemap[codeptr]
  if command == "]" and cells[cellptr] != 0: codeptr = bracemap[codeptr]
  if command == ".": print(chr(cells[cellptr]),end="")
  if command == ",": cells[cellptr] = ord(getch.getch())

  if command == "#": cells2[cellptr2] += cellptr
  if command == "=": cells2[cellptr2] -= cellptr
  if command == "^": cellptr2 += 1
  if cellptr2 == len(cells2): cells2.append(0)
  if command == "v": cellptr2 = 0 if cellptr2 <= 0 else cellptr2 - 1
  if command == "{" and cells2[cellptr2] == 0: codeptr = bracemap[codeptr]
  if command == "}" and cells2[cellptr2] != 0: codeptr = bracemap[codeptr]
  if command == "!": print(chr(cells2[cellptr2]),end="")
  if command == "?": cells2[cellptr2] = ord(getch.getch())

  cells[cellptr] %= 256
  cells2[cellptr2] %= 256
  codeptr += 1
