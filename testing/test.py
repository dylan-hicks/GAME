import unittest
import subprocess
import os
import time
class TestGAME(unittest.TestCase):
  file_names = []
  def setUp(self):
    #System commands to compile test files
    #subprocess.Popen("cd source; compile *.game; mv *.py ../target", shell=True)
    #Create list of file names
    TestGAME.file_names = os.listdir("./source")

  def test_target_compilation(self):
    num_failed = 0
    print("====================================================")
    print("\nTesting for Correctness of Target Compiled Files:\n\n")
    for file_name in TestGAME.file_names:
      #create diff file between target/file_name and correct/file_name
      subprocess.Popen("diff ./target/{}.py ./correct/{}.py > ./target/{}.py.diff".format(file_name, file_name, file_name), shell=True)
      #prevent diff checking before file is created
      time.sleep(0.01)
      #if diff is 0 bytes, target compiled file is correct
      if os.stat("./target/{}.py.diff".format(file_name)).st_size == 0:
        #clean up target file and diff file
        subprocess.Popen("cd target; rm {}.py; rm {}.py.diff".format(file_name, file_name), shell=True)
      else:
        #print error message and leave diff and target files
        num_failed += 1
        print("{}: {} Test Case failed.\n\n".format(num_failed, file_name))
    print("{} Target Compile Test Case(s) Failed\n".format(num_failed))
    print("====================================================")


if __name__ == '__main__':
  unittest.main()
