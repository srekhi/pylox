import sys 
from scanner import Scanner
from parser import Parser 
from ast_printer import AstPrinter

hadError = False 

def run_file(file_path):
  f = open(file_path)
  run(f.read())
  if hadError:
    sys.exit(65)

def run_prompt():
  global hadError
  while True:
    run(input('>>> '))
    hadError = False;
    # print('HAD ERROR IS RESET')

def run(source):
  scanner = Scanner(source)
  tokens = scanner.scan_tokens()
  parser = Parser(tokens)
  statements = parser.parse()
  
  hadError = len(scanner.errors) + len(parser.errors)
  print("HAD ERROR VALUE IS %s" % hadError)
  if (hadError): 
    return 

  interpreter.interpret(statements)

  # print(AstPrinter().print(expression))

hadRuntimeError = False 
def runtimeError(err):
  global hadRuntimeError
  print(err)
  hadRuntimeError = True 

def error(line, message):
  report(line, '', message)

def report(line, where, message):
  print ("[line %s] Error %s: %s" % (line, where, message))
  import pdb; pdb.set_trace()
  global hadError
  hadError = True

def main(arguments):
  if len(arguments) > 1:
    print("Too many arguments. Format should be: pyLox 'fileName.py'")
    sys.exit(64)
  elif len(arguments) == 1:
    run_file(arguments[0])
  else:
    run_prompt()

if __name__ == '__main__':
  main(sys.argv[1:])
