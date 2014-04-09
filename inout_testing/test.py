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
    for file_name in TestGAME.file_names:
      #run target/python file and pipe output into .txt file in output directory
      subprocess.Popen("cd target; python ./target/{}.py > ../output/{}.txt;".format(file_name, file_name), shell=True)
      time.sleep(0.01)
      #create diff in diffs directory
      subprocess.Popen("diff ./output/{}.txt ./correct/{}.txt > ./diffs/{}.txt.diff".format(file_name, file_name, file_name), shell=True)
      time.sleep(0.01)
      #if diff is not 0, print diff and then print expected vs. actual
      if os.stat("./diffs/{}.txt.diff".format(file_name)).st_size == 0:
        print("{} Test Case passed.\n\n".format(file_name))
      else:
        num_failed +=1
        print("{} Test Case failed.\n\n".format(file_name))
        #print diff
        print("Diff:\n\n")
        with open("./diffs/{}.txt.diff".format(file_name)) as file:
          print file.read()
        #print expected
        print("Expected Output for {}.py\n\n".format(file_name))
        with open("./correct/{}/txt".format(file_name)) as file:
          print file.read()
        #print actual
        print("Actual Output for {}.py\n\n".format(file_name))
        with open("./output/{}/txt".format(file_name)) as file:
          print file.read()


    print("{} Target Compile Test Case(s) Failed\n".format(num_failed))
    print("====================================================")

if __name__ == '__main__':
  unittest.main()
