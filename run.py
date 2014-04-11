import subprocess
import sys

#python run.py [.game file]

def compile():
  #sys.argv[1] should be target source .game file
  subprocess.Popen("./gamec {} > error.txt".format(sys.argv[1]), shell=True)

def print_errors():
  with open("./error.txt") as file:
    print file.read()

def run():
  subprocess.Popen("python {}.py".format(sys.argv[1]), shell=True)

if __name__ == '__main__':
  compile()
  if os.stat("./error.txt").st_size == 0
    run()
  else
    print_errors()
