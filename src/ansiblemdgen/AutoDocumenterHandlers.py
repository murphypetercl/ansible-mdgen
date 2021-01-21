#!/usr/bin/env python3

from ansiblemdgen.Config import SingleConfig
import sys
import yaml
import os
from os import walk
from ansiblemdgen.Utils import SingleLog,FileUtils
from mdutils.mdutils import MdUtils

class TasksWriter:

    config = None
    tasks_dir = None

    def __init__(self):
        self.config = SingleConfig()
        self.log = SingleLog()

        self.tasks_dir = self.config.get_base_dir()+"/tasks"
        self.log.info("Tasks directory: "+self.tasks_dir)

    def render(self):

        self.makeDocsTasksDir()

        if (self.config.tasks != None and self.config.tasks['combinations'] != None):
            self.iterateOnCombinations(self.config.get_base_dir(), self.config.tasks['combinations'])
        else:
            self.iterateOnFilesAndDirectories(self.tasks_dir)


    def makeDocsTasksDir(self):
        output_tasks_directory = self.config.get_output_tasks_dir()
        self.log.debug("(makeDocsTasksDir) Output Directory: "+output_tasks_directory)
        if not os.path.exists(output_tasks_directory):
            os.makedirs(output_tasks_directory)

    def iterateOnFilesAndDirectories(self, tasks_dir):
        for (dirpath, dirnames, filenames) in walk(tasks_dir):

            for filename in filenames:
                if filename.endswith('.yml'):
                    self.createMDFile(dirpath, filename)

            for dirname in dirnames:
                self.iterateOnFilesAndDirectories(dirpath+"/"+dirname)

    def createMDFile(self, dirpath, filename):

        self.log.info("(createMDFile) Create MD File")
        self.log.debug("(createMDFile) dirpath: "+dirpath)
        self.log.debug("(createMDFile) filename: "+filename)
        
        docspath = dirpath.replace(self.tasks_dir,self.config.get_output_tasks_dir())
        self.log.debug("(createMDFile) docspath: "+docspath)

        if not os.path.exists(docspath):
            os.makedirs(docspath)

        mdFile = MdUtils(file_name=docspath+"/"+filename.replace('.yml',''))
        mdFile.new_header(level=1, title=filename) 
        self.addTasks(dirpath+"/"+filename, mdFile)

        mdFile.create_md_file()
        self.log.info("(createMDFile) Create MD File Complete")

    
    def addTasks(self, filename, mdFile):
        self.log.debug("(addTasks) Filename: "+filename)
        with open(filename, 'r') as stream:
            try:
                tasks = yaml.safe_load(stream)
                if tasks != None:
                    for task in tasks:
                        mdFile.new_paragraph('* '+task["name"])
            except yaml.YAMLError as exc:
                print(exc)

    def iterateOnCombinations(self, rolepath, combinations):
        for combination in combinations:
            self.createMDCombinationFile(combination['filename'], combination['files_to_combine'])

    def createMDCombinationFile(self, comboFilename, filenamesToCombine):

        comboFilenameAbs = self.config.get_output_tasks_dir()+"/"+comboFilename      
        comboFileDirectory = comboFilenameAbs[0:int(comboFilenameAbs.rfind('/'))]

        if not os.path.exists(comboFileDirectory):
            os.makedirs(comboFileDirectory)

        mdFile = MdUtils(file_name=comboFilenameAbs)

        mdFile.new_header(level=1, title='Tasks: '+comboFilename[comboFilename.rfind('/')+1:])
        mdFile.new_line("---")
        for filename in filenamesToCombine:
            mdFile.new_line("")
            mdFile.new_header(level=2, title=filename['name']) 

            self.addTasks(self.tasks_dir+"/"+filename['name'], mdFile)

        mdFile.create_md_file()