#!/usr/bin/env python3

from ansiblemdgen.Config import SingleConfig
import sys
import yaml
import os
from os import walk
from ansiblemdgen.Utils import SingleLog,FileUtils
from mdutils.mdutils import MdUtils

from ansiblemdgen.AutoDocumenterBase import WriterBase

class TasksWriter(WriterBase):

    tasks_dir = None
    handlers_dir = None
    flow = {}

    def render(self):

        self.tasks_dir = self.config.get_base_dir()+"/tasks"
        self.log.info("Tasks directory: "+self.tasks_dir)

        self.handlers_dir = self.config.get_base_dir()+"/handlers"
        self.log.info("Tasks directory: "+self.handlers_dir)

        self.makeDocsDir(self.config.get_output_tasks_dir())

        self.createMDFlowFile(self.tasks_dir, self.config.get_output_tasks_dir())

        if (self.config.tasks != None and self.config.tasks['combinations'] != None):
            self.iterateOnCombinations(self.tasks_dir, self.config.tasks['combinations'], self.config.get_output_tasks_dir())
        else:
            self.iterateOnFilesAndDirectories(self.tasks_dir, self.config.get_output_tasks_dir())

        self.makeDocsDir(self.config.get_output_handlers_dir())

        if (self.config.handlers != None and self.config.handlers['combinations'] != None):
            self.iterateOnCombinations(self.handlers_dir, self.config.handlers['combinations'], self.config.get_output_handlers_dir())
        else:
            self.iterateOnFilesAndDirectories(self.handlers_dir,self.config.get_output_handlers_dir())


    def createMDFile(self, dirpath, filename, output_directory):

        self.log.info("(createMDFile) Create MD File")
        self.log.debug("(createMDFile) dirpath: "+dirpath)
        self.log.debug("(createMDFile) filename: "+filename)
        self.log.debug("(createMDFile) output_directory: "+output_directory)
        
        if output_directory == self.config.get_output_tasks_dir():
            docspath = dirpath.replace(self.tasks_dir,output_directory)
        else:
            docspath = dirpath.replace(self.handlers_dir,output_directory)
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
                        try:
                            if 'block' in task.keys():
                                if 'name' in task.keys():
                                    mdFile.new_paragraph('* Block: '+task["name"])
                                else:
                                    mdFile.new_paragraph('* Block: ')

                                for btask in task["block"]:
                                    if 'name' in btask.keys():
                                        mdFile.new_paragraph('    * '+btask["name"])
                            elif 'name' in task.keys():
                                mdFile.new_paragraph('* '+task["name"])
                            else:
                                mdFile.new_paragraph('* No description available for this task - here is the definition:')
                                mdFile.new_line("```")
                                mdFile.new_paragraph(yaml.safe_dump(task,  default_flow_style=False))
                                mdFile.new_line("```")
                        except Exception:
                            print(task)
                            pass

            except yaml.YAMLError as exc:
                print(exc)

    def createMDCombinationFile(self, comboFilename, directory, output_directory, filenamesToCombine):

        self.log.info("(createMDCombinationFile) Create MD Combination File")
        self.log.debug("(createMDCombinationFile) comboFilename: "+comboFilename)
        self.log.debug("(createMDCombinationFile) directory: "+directory)
        self.log.debug("(createMDCombinationFile) output_directory: "+output_directory)

        comboFilenameAbs = output_directory+"/"+comboFilename      
        comboFileDirectory = comboFilenameAbs[0:int(comboFilenameAbs.rfind('/'))]

        if not os.path.exists(comboFileDirectory):
            os.makedirs(comboFileDirectory)

        mdFile = MdUtils(file_name=comboFilenameAbs)

        mdFile.new_header(level=1, title='Tasks: '+comboFilename[comboFilename.rfind('/')+1:])
        mdFile.new_line("---")
        for filename in filenamesToCombine:
            mdFile.new_line("")
            mdFile.new_header(level=2, title=filename['name']) 

            self.addTasks(directory+"/"+filename['name'], mdFile)

        mdFile.create_md_file()
    
    def createMDFlowFile(self, directory, output_directory):

        mdFile = MdUtils(file_name=output_directory+"/flow")
        mdFile.new_header(level=1, title='Flow') 

        self.getFlowData(directory)

        mdFile.new_line("```mermaid")
        mdFile.new_line("graph LR")

        for connection in self.flow:
            if self.flow[connection] != []:
                for connectTo in self.flow[connection]:
                    to = connectTo['include']
                    mdFile.new_line(connection+"("+connection+") --> "+to+"("+to+")")

        mdFile.new_line("```")

        mdFile.create_md_file()

    def getFlowData(self, directory):
        self.getFlowDataForFile(directory, 'main.yml')
        self.getOrphanedFlowData(directory)

    def getFlowDataForFile(self, directory, filename):
        with open(directory+"/"+filename, 'r') as stream:
            try:
                tasks = yaml.safe_load(stream)
                if tasks != None:
                    for task in tasks:
                        if 'block' in task.keys():
                            for btask in task["block"]:
                                try:
                                    if 'include_tasks' in btask.keys():
                                        self.getTaskReuseFile(btask, "include_tasks", filename)
                                    elif 'import_tasks' in btask.keys():
                                        self.getTaskReuseFile(btask, "import_tasks", filename)
                                except Exception:
                                    pass
                        try:
                            if 'include_tasks' in task.keys():
                                self.getTaskReuseFile(task, "include_tasks", filename)
                            elif 'import_tasks' in task.keys():
                                self.getTaskReuseFile(task, "import_tasks", filename)
                        except Exception:
                            pass
            except yaml.YAMLError as exc:
                print(exc)

    def getTaskReuseFile(self, task, reuse_type, filename):
        if task[reuse_type].startswith('{{') is False:
            if filename not in self.flow.keys():
                self.flow[filename] = []
            self.flow[filename].append({"include": task[reuse_type]})
            self.getFlowDataForFile(directory, task[reuse_type])


    def getOrphanedFlowData(self, directory):
        for (dirpath, dirnames, filenames) in walk(directory):
            for filename in filenames:
                relativeFilename = (os.path.relpath(dirpath, directory)+"/"+filename).replace("./","")
                if relativeFilename not in self.flow.keys():
                    self.getFlowDataForFile(directory, relativeFilename)
