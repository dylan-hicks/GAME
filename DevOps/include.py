import sys
import re
import os

included = []

#Returns what a file should look like after processing all include statements and swapping these out with the appropriate library code
def include(file_name):
  file = open(file_name, "r+")
  contents = file.readlines()
  #Screen for include statements
  i = 0
  for line in contents:
    regMatch = re.match(r'[\s]*include[\s]*["][\s]*([a-zA-Z_-]*)(.game)?[\s]*["][\s]*', line, flags=0)
    if regMatch: #include statement match
      if regMatch.group(1) not in included:
        #get library file name
        library_file_name = "{}.game".format(regMatch.group(1)).lower()
        #check for existence of library file
        if file_exists(library_file_name):
          #add library name to included array
          included.append(regMatch.group(1))
          #recursively call include on library file to get prepared content
          to_append = include(library_file_name)
          #add file contents of prepared library file to our contents and remove include line
          contents[i] = ""
          contents [i:i] = to_append
          #contents = contents + to_append
        else:
          print "{} does not exist\n".format(library_file_name)
          sys.exit()
      else:
        contents.remove(line)
    i = i + 1;
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
    file.write("%s" % line)
