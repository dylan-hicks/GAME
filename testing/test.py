import subprocess
import os
import time

def test():

  print("")

  #System commands to compile test files
  subprocess.Popen("./gamec ./source/*.game && mv ./source/*.game.py ./target;", shell=True)
  time.sleep(1)

  #Create list of file names
  for file_name in os.listdir("./source"):
    if ".game" in file_name: run_case(file_name)
  time.sleep(0.3)

  num_failed = 0
  print("\n====================================================\n")
  for file_name in os.listdir("./source"):
    if ".game" in file_name: num_failed += compare_output(file_name)
  print("{} Test Case(s) Failed\n".format(num_failed))
  print("====================================================\n")

def run_case(file_name):
  #run target/python file and pipe output into .txt file in output directory
  subprocess.Popen("python ./target/{}.py > ./output/{}.txt;".format(file_name, file_name), shell=True)
  time.sleep(0.25)
  #create diff in diffs directory
  subprocess.Popen("diff ./output/{}.txt ./correct/{}.txt > ./diffs/{}.txt.diff".format(file_name, file_name, file_name), shell=True)
  time.sleep(0.1)

def compare_output(file_name):
  #if diff is not 0, print diff and then print expected vs. actual
  if "{}.txt".format(file_name) not in os.listdir("./correct"):
    print("{} Test Case failed.".format(file_name))
    print("No correct output file for {} Test Case exists.\n".format(file_name))
    return 1
  elif os.stat("./diffs/{}.txt.diff".format(file_name)).st_size == 0:
    print("{} Test Case passed.\n".format(file_name))
    return 0
  else:
    print("{} Test Case failed.\n".format(file_name))
    #print diff
    print("Diff:\n")
    with open("./diffs/{}.txt.diff".format(file_name)) as file:
      print file.read()
    #print expected
    print("Expected Output for {}.py:\n".format(file_name))
    with open("./correct/{}.txt".format(file_name)) as file:
      print file.read()
    #print actual
    print("Actual Output for {}.py:\n".format(file_name))
    with open("./output/{}.txt".format(file_name)) as file:
      print file.read()
    return 1

if __name__ == '__main__':
  test()
