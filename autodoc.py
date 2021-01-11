# #!/usr/bin/python3 -tt

"""A python program to create documentation for ansible roles
  python autodoc.py <role_path>
"""

import sys
import yaml
import os
from os import walk
from mdutils.mdutils import MdUtils
from mdutils import Html


# rolepath = None

# Define a main() function that prints a little greeting.
def main():
  # Get the role path from the command line
  if len(sys.argv) >= 2:
    rolepath = sys.argv[1]
    roletasks = rolepath+"/tasks"
    print ('Role path = ', roletasks)

    config = getConfig(rolepath)

    makeDocsDir(rolepath)

    if (config != None):
      combinations = getCombinations(config)
      print(combinations)
      iterateOnCombinations(rolepath, combinations)
    else:
      iterateOnFilesAndDirectories(roletasks)
  else:
    print ('No role path specified!')
    return

def makeDocsDir(rolepath):
  docspath = rolepath+"/docs"
  print("docspath",docspath)
  if not os.path.exists(docspath):
    os.makedirs(docspath)

def iterateOnFilesAndDirectories(roletasks):
  for (dirpath, dirnames, filenames) in walk(roletasks):
    print("Dir path", dirpath)
    print("dirnames", dirnames)
    print("filenames", filenames)

    for filename in filenames:
      if filename.endswith('.yml'):
        createMDFile(dirpath, filename)

    for dirname in dirnames:
      iterateOnFilesAndDirectories(dirpath+"/"+dirname)

def createMDFile(dirpath, filename):

  docspath = dirpath.replace('tasks','docs')
  if not os.path.exists(docspath):
    os.makedirs(docspath)

  mdFile = MdUtils(file_name=docspath+"/"+filename.replace('.yml',''),title=filename.replace('.yml',''))
  mdFile.new_header(level=1, title='Tasks') 
  addTasks(dirpath+"/"+filename, mdFile)
  mdFile.create_md_file()
  

def addTasks(filename, mdFile):
  print("Filename: ", filename)
  with open(filename, 'r') as stream:
    try:
        tasks = yaml.safe_load(stream)
        if tasks != None:
          for task in tasks:
            print(task["name"])
            mdFile.new_paragraph(task["name"])
    except yaml.YAMLError as exc:
        print(exc)


def getConfig(rolepath):
  print('GET CONFIG:')
  with open(rolepath+"/mdgen.yml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
        return config
        # print(config)
        # if config != None:
        #   print(config["combine"])
          # for configitem in config:
          #   print(configitem["combine"])
    except yaml.YAMLError as exc:
        print(exc)

def getCombinations(config):
      if config != None:
        return config["combine"]

def iterateOnCombinations(rolepath, combinations):
  for combination in combinations:
    print(combination.items())
    for key, value in combination.items():
      print(key, value)
      createMDCombinationFile(rolepath, key, value)

def createMDCombinationFile(rolepath, comboFilename, filenamesToCombine):

  mdFile = MdUtils(file_name=rolepath+"/docs/"+comboFilename,title=comboFilename)
  mdFile.new_header(level=1, title='Tasks') 
  for filename in filenamesToCombine:
    mdFile.new_line("")
    mdFile.new_header(level=2, title=filename) 
    addTasks(rolepath+"/tasks/"+filename, mdFile)
  
  mdFile.create_md_file()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
