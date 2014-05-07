import subprocess
import sys

def compile(file_name):
  subprocess.check_call("./gamec {}".format(file_name), shell=True)

if __name__ == '__main__':
  if len(sys.argv) == 0:
    print "\nTo run your .game file, please use the following command:\n\npython run.py [.game file]\n\nPlease note that you can only run one .game file at a time.\n"
  else:
    compile(sys.argv[1])
    subprocess.check_call("python {}.py".format(sys.argv[1]), shell=True)