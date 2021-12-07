# Compiles to Brainfuck.
code="".join(i for i in input() if i in "01")
assert len(code) >= 3, "Code cannot refer to any instruction"
print("".join(["<>+-.,[]"[int(code[i:i+3],2)] for i in range(len(code)-2)]))
