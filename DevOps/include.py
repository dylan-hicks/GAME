import sys
import re
import os

included = []

#Returns what a file should look like after processing all include statements and swapping these out with the appropriate library code
def include(file_name, directory):
  file = open(file_name, "r+")
  contents = file.readlines()
  #Screen for include statements
  i = 0
  for line in contents:
    regMatch = re.match(r'[\s]*include[\s]*["][\s]*([a-zA-Z_-]*/)?([a-zA-Z_-]*)(.game)?[\s]*["][\s]*', line, flags=0)
    if regMatch: #include statement match
      #construct relative library file path name
      prefix = regMatch.group(1)
      if prefix == None:
        prefix = ""
      unique = "./{}{}{}.game".format(directory, prefix, regMatch.group(2)).lower()
      if unique not in included:
        #check for existence of library file
        if os.path.isfile(unique):
          #add library name to included array
          included.append(unique)
          #recursively call include on library file to get prepared content
          to_append = include(unique, regMatch.group(1))
          #add file contents of prepared library file to our contents and remove include line
          contents[i] = ""
          contents [i:i] = to_append
          #contents = contents + to_append
        else:
          print "{} does not exist\n".format(unique)
          sys.exit(1)
      else:
        contents.remove(line)
    i = i + 1;
  file.close()
  return contents

if __name__ == '__main__':
  name = sys.argv[1]
  #create new temp file with .temp file extension
  file = open("{}.temp".format(sys.argv[1]), 'w')
  for line in include(name, ""):
    file.write("%s" % line)
