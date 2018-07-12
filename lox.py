import sys 
from scanner import Scanner

hadError = False 

def run_file(file_path):
  global hadError
  f = open(file_path)
  run(f.read())
  if hadError:
    sys.exit(65)

def run_prompt():
  global hadError
  while True:
    run(input('>>> '))
    hadError = False;

def run(source):
  scanner = Scanner(source)
  tokens = scanner.scan_tokens()
  for token in tokens:
    print(token)

def error(line, message):
  report(line, '', message)

def report(line, where, message):
  print ("[line %s] Error %s: %s" % (line, where, message))
  global hadError
  hadError = False 

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
