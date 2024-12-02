import sys
import architect

file = input("Choose a file to run (don't need .arc): ")
with open(f"{file}.arc") as sys.stdin:
  code = sys.stdin.read()

architect.execute_code(code)
