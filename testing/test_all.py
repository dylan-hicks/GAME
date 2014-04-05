import unittest
import subprocess
import os
class TestGAME(unittest.TestCase):
  file_names = []
  def setUp(self):
    #System commands to compile test files
    #subprocess.Popen("cd source; compile *.game; mv *.py ../target", shell=True)
    #Create list of file names
    TestGame.file_names = os.listdir("./source")

  def test(self):
    for file_name in TestGame.file_names
      #create diff file between target/file_name and correct/file_name
      subprocess.Popen("diff ./target/{}.py ./correct/{}.py > ./target/{}.py.diff".format(file_name, file_name, file_name), shell=True)
      #if diff is 0 bytes, is good
      if os.stat("./target/{}.diff".format(file_name)).st_size == 0
        #clean up target file and diff file
        subprocess.Popen("cd target; rm {}.py; rm {}.py.diff".format(file_name, file_name), shell=True)
      else
        #print error message
        #leave diff and target files

  def tearDown(self):
    subprocess.Popen("rm *.pyc", shell=True)

if __name__ == '__main__':
  unittest.main()
