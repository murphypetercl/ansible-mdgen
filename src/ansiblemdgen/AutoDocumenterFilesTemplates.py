#!/usr/bin/env python3

from ansiblemdgen.Config import SingleConfig
import sys
import yaml
import os
from os import walk
from ansiblemdgen.Utils import SingleLog,FileUtils
from mdutils.mdutils import MdUtils
import re

from ansiblemdgen.AutoDocumenterBase import WriterBase

class FilesTemplatesWriter(WriterBase):

    files_dir = None
    templates_dir = None

    _all_descriptions = {}

    def render(self):

        self.files_dir = self.config.get_base_dir()+"/files"
        self.log.info("Files directory: "+self.files_dir)

        self.templates_dir = self.config.get_base_dir()+"/templates"
        self.log.info("Templates directory: "+self.templates_dir)

        if self.config.output_files is True:
            self.makeDocsDir(self.config.get_output_files_dir())

            if (self.config.files != None and self.config.files['combinations'] != None):
                self.iterateOnCombinations(self.files_dir, self.config.files['combinations'], self.config.get_output_files_dir())
            else:
                self.iterateOnFilesAndDirectories(self.files_dir, self.config.get_output_files_dir())

        if self.config.output_templates is True:
            self.makeDocsDir(self.config.get_output_templates_dir())

            if (self.config.templates != None and self.config.templates['combinations'] != None):
                self.iterateOnCombinations(self.templates_dir, self.config.templates['combinations'], self.config.get_output_templates_dir())
            else:
                self.iterateOnFilesAndDirectories(self.templates_dir, self.config.get_output_templates_dir())


    def createMDFile(self, dirpath, filename, output_directory):

        self.log.info("(createMDFile) Create MD File")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        title_prefix = output_directory[output_directory.rfind('/')+1:].title()

        mdFile = MdUtils(file_name=output_directory+"/"+filename.replace('.yml',''))

        mdFile.new_header(level=1, title=filename) 

        mdFile.new_line("---")

        self.addFileOrTemplate(dirpath+"/"+filename, mdFile)

        mdFile.create_md_file()
        self.log.info("(createMDFile) Create MD File Complete")

    
    def addFileOrTemplate(self, filename, mdFile):
        self.log.debug("(addFileOrTemplate) Filename: "+filename)

        with open(filename, 'r') as stream:
            try:
                mdFile.new_line("```")
                mdFile.new_paragraph(stream.read())
                mdFile.new_line("```")

            except yaml.YAMLError as exc:
                print(exc)


    def createMDCombinationFile(self, comboFilename, directory, output_directory, filenamesToCombine):

        comboFilenameAbs = output_directory+"/"+comboFilename      
        comboFileDirectory = comboFilenameAbs[0:int(comboFilenameAbs.rfind('/'))]

        if not os.path.exists(comboFileDirectory):
            os.makedirs(comboFileDirectory)

        mdFile = MdUtils(file_name=comboFilenameAbs)

        mdFile.new_header(level=1, title=comboFilename[comboFilename.rfind('/')+1:]) 
        for filename in filenamesToCombine:
            mdFile.new_line("")
            mdFile.new_header(level=2, title=filename['name']) 

            self.addVariables(directory+"/"+filename['name'], mdFile)

        mdFile.create_md_file()
