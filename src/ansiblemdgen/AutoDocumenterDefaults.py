#!/usr/bin/env python3

from ansiblemdgen.Config import SingleConfig
import sys
import yaml
import os
from os import walk
from ansiblemdgen.Utils import SingleLog,FileUtils
from mdutils.mdutils import MdUtils
import re

class DefaultsWriter:

    config = None
    defaults_dir = None

    _all_descriptions = {}

    def __init__(self):
        self.config = SingleConfig()
        self.log = SingleLog()

        self.defaults_dir = self.config.get_base_dir()+"/defaults"
        self.log.info("Defaults directory: "+self.defaults_dir)

    def render(self):

        self.makeDocsDefaultsDir()

        if (self.config.defaults != None and self.config.defaults['combinations'] != None):
            self.iterateOnCombinations(self.config.get_base_dir(), self.config.defaults['combinations'])
        else:
            self.iterateOnFilesAndDirectories(self.defaults_dir)


    def makeDocsDefaultsDir(self):
        output_defaults_directory = self.config.get_output_defaults_dir()
        self.log.debug("(makeDocsDefaultsDir) Output Directory: "+output_defaults_directory)
        if not os.path.exists(output_defaults_directory):
            os.makedirs(output_defaults_directory)

    def iterateOnFilesAndDirectories(self, defaults_dir):
        for (dirpath, dirnames, filenames) in walk(defaults_dir):

            for filename in filenames:
                if filename.endswith('.yml'):
                    self.createMDFile(dirpath, filename)

            for dirname in dirnames:
                self.iterateOnFilesAndDirectories(dirpath+"/"+dirname)

    def createMDFile(self, dirpath, filename):

        self.log.info("(createMDFile) Create MD File")
        docspath = dirpath.replace(self.defaults_dir,self.config.get_output_defaults_dir())
        if not os.path.exists(docspath):
            os.makedirs(docspath)

        mdFile = MdUtils(file_name=self.config.get_output_defaults_dir()+"/"+filename.replace('.yml',''),title=filename.replace('.yml',''))
        mdFile.new_line("---")
        mdFile.new_header(level=1, title='Defaults') 
        mdFile.new_line("---")

        mdFile.new_header(level=2, title=filename.replace('.yml','')) 

        self.addDefaults(dirpath+"/"+filename, mdFile)

        mdFile.new_table_of_contents(table_title='Contents', depth=2)
        mdFile.create_md_file()
        self.log.info("(createMDFile) Create MD File Complete")

    
    def addDefaults(self, filename, mdFile):
        self.log.debug("(addDefaults) Filename: "+filename)

        self.getVarDescriptions(filename)

        with open(filename, 'r') as stream:
            try:
                defaults = yaml.safe_load(stream)

                if defaults != None:
                    for default in defaults:
                        
                        mdFile.new_line("---")
                        mdFile.new_header(level=3, title=default)

                        mdFile.new_header(level=4, title='Description')
                        
                        if(default in self._all_descriptions):
                            mdFile.new_paragraph(yaml.safe_dump(self._all_descriptions[default][0]["value"],  default_flow_style=False))

                        mdFile.new_header(level=4, title='Value')
                        mdFile.new_line("```")
                        mdFile.new_paragraph(yaml.safe_dump(defaults[default],  default_flow_style=False))
                        mdFile.new_line("```")

            except yaml.YAMLError as exc:
                print(exc)

    def getVarDescriptions(self, filename):
        file = open(filename, 'r')
        while True:
            line = file.readline()
            
            if not line:
                break
        
            regex = "(\#\ *\@var:\ +.*)"
            if re.match(regex, line):
                # step1 remove the annotation
                reg1 = "(\#\ *\@var:\ *)"
                line1 = re.sub(reg1, '', line).strip()

                # step3 take the main key value from the annotation
                parts = line1.split(":",1)
                key = str(parts[0].strip())
                value = str(parts[1].strip())

                item = AnnotationItem()

                if key.strip() == "":
                    key = "_unset_"
                item.key = key

                item.value = value

                if item.key not in self._all_descriptions.keys():
                    self._all_descriptions[item.key] = []

                self._all_descriptions[item.key].append(item.get_obj())

    def iterateOnCombinations(self, rolepath, combinations):
        for combination in combinations:
            self.createMDCombinationFile(combination['filename'], combination['files_to_combine'])

    def createMDCombinationFile(self, comboFilename, filenamesToCombine):

        comboFilenameAbs = self.config.get_output_defaults_dir()+"/"+comboFilename      
        comboFileDirectory = comboFilenameAbs[0:int(comboFilenameAbs.rfind('/'))]

        if not os.path.exists(comboFileDirectory):
            os.makedirs(comboFileDirectory)

        mdFile = MdUtils(file_name=comboFilenameAbs,title=comboFilename[comboFilename.rfind('/')+1:])
        mdFile.new_line("---")
        mdFile.new_header(level=1, title='Defaults') 
        for filename in filenamesToCombine:
            mdFile.new_line("")
            mdFile.new_header(level=2, title=filename['name']) 

            self.addDefaults(self.defaults_dir+"/"+filename['name'], mdFile)

        mdFile.new_table_of_contents(table_title='Contents', depth=2)
        mdFile.create_md_file()

class AnnotationItem:

    key = ""  # annotation identifying key
    value = ""  # annotation data

    def __str__(self):
        s = "{"
        s += "key: "+self.key+", "
        s += "value: "+self.value+", "
        s += "}"
        return s

    def get_obj(self):
        return {
            "key": self.key,
            "value": self.value,
        }