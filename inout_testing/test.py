import subprocess
import os
import time

def test():
  #System commands to compile test files
  #subprocess.Popen("cd source; compile ../*.game; mv *.py ../target", shell=True)
  #Create list of file names
  file_names = os.listdir("./source")

  num_failed = 0
  print("====================================================")
  for file_name in file_names:
    num_failed += test_case(file_name)
  print("{} Test Case(s) Failed\n".format(num_failed))
  print("====================================================")

def test_case(file_name):
  run_case(file_name)
  return compare_outputs(file_name)

def run_case(file_name):
  #run target/python file and pipe output into .txt file in output directory
  subprocess.Popen("cd target; python {}.py > ../output/{}.txt;".format(file_name, file_name), shell=True)
  time.sleep(0.1)
  #create diff in diffs directory
  subprocess.Popen("diff ./output/{}.txt ./correct/{}.txt > ./diffs/{}.txt.diff".format(file_name, file_name, file_name), shell=True)
  time.sleep(0.01)

def compare_outputs(file_name):
  #if diff is not 0, print diff and then print expected vs. actual
  if os.stat("./diffs/{}.txt.diff".format(file_name)).st_size == 0:
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
