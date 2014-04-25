import sys
import re
import os

included = []

def include(file_name):

  file = open(file_name, "r+")
  contents = file.readlines()
  for line in contents:
    regMatch = re.match(r'[\s]*include[\s]*["][\s]*([a-zA-Z_-]*)[\s]*["][\s]*\n', line, flags=0)
    if regMatch:
      if regMatch.group(1) not in included:
        #get library file name
        library_file_name = "{}.game".format(regMatch.group(1))
        #check for existence of library file
        if file_exists(library_file_name):
          #add library name to included array
          included.append(regMatch.group(1))
          #recursively call include on library file to get prepared content
          to_append = include(library_file_name)
          #add file contents of prepared library file to our contents and remove include line
          contents.remove(line)
          contents = contents + to_append
        else:
          print "{} does not exist\n".format(library_file_name)
          sys.exit()
      else:
        contents.remove(line)
  file.close()
  return contents

def file_exists(file_name):
  if file_name in os.listdir("./"):
    return True
  return False

if __name__ == '__main__':
  name = sys.argv[1]
  #create new temp file with .temp file extension
  file = open("{}.temp".format(sys.argv[1]), 'w')

  for line in include(name):

    print line
    print>>file, line
  print "done"

