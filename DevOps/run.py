import subprocess
import sys

#def compile():
#  #sys.argv[1] should be target source .game file
#  subprocess.Popen("./gamec {} > error.txt".format(sys.argv[1]), shell=True)

#def print_errors():
#  with open("./error.txt") as file:
#    print file.read()

if __name__ == '__main__':
  if len(sys.argv) != 0:
    print "\nTo run your .game.py file, please use the following command:\n\npython run.py [.game.py file]\n\nPlease note that you can only run one .game.py file at a time.\n"
  else:
    subprocess.Popen("python {}.py".format(sys.argv[1]), shell=True)
  #if os.stat("./error.txt").st_size == 0
  #  run()
  #else
   # print_errors()
