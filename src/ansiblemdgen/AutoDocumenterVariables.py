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

class VariablesWriter(WriterBase):

    defaults_dir = None
    vars_dir = None

    _all_descriptions = {}

    where_referenced = ""

    def render(self):

        self.defaults_dir = self.config.get_base_dir()+"/defaults"
        self.log.info("Defaults directory: "+self.defaults_dir)

        self.vars_dir = self.config.get_base_dir()+"/vars"
        self.log.info("Vars directory: "+self.vars_dir)

        self.makeDocsDir(self.config.get_output_defaults_dir())

        if (self.config.defaults != None and self.config.defaults['combinations'] != None):
            self.iterateOnCombinations(self.defaults_dir, self.config.defaults['combinations'], self.config.get_output_defaults_dir())
        else:
            self.iterateOnFilesAndDirectories(self.defaults_dir, self.config.get_output_defaults_dir())

        self.makeDocsDir(self.config.get_output_variables_dir())

        if (self.config.variables != None and self.config.variables['combinations'] != None):
            self.iterateOnCombinations(self.vars_dir, self.config.variables['combinations'], self.config.get_output_variables_dir())
        else:
            self.iterateOnFilesAndDirectories(self.vars_dir, self.config.get_output_variables_dir())


    def createMDFile(self, dirpath, filename, output_directory):

        self.log.info("(createMDFile) Create MD File")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        title_prefix = output_directory[output_directory.rfind('/')+1:].title()

        mdFile = MdUtils(file_name=output_directory+"/"+filename.replace('.yml',''))

        mdFile.new_header(level=1, title=filename) 

        mdFile.new_line("---")

        self.addVariables(dirpath+"/"+filename, mdFile)

        mdFile.create_md_file()
        self.log.info("(createMDFile) Create MD File Complete")

    
    def addVariables(self, filename, mdFile):
        self.log.debug("(addVariables) Filename: "+filename)

        self.getVarDescriptions(filename)

        with open(filename, 'r') as stream:
            try:
                variables = yaml.safe_load(stream)

                if variables != None:
                    for variable in variables:

                        mdFile.new_header(level=2, title=variable)
                        
                        if(variable in self._all_descriptions):
                            mdFile.new_paragraph(yaml.safe_dump(self._all_descriptions[variable][0]["value"],  default_flow_style=False))

                        mdFile.new_line("```")
                        mdFile.new_paragraph(yaml.safe_dump(variables[variable],  default_flow_style=False))
                        mdFile.new_line("```")

                        mdFile.new_line('Where Referenced', bold_italics_code='b', color='green')

                        self.where_referenced = ""
                        self.addVariableReferences(variable, filename, self.config.get_base_dir()+"/tasks", mdFile)
                        self.addVariableReferences(variable, filename, self.config.get_base_dir()+"/defaults", mdFile)
                        self.addVariableReferences(variable, filename, self.config.get_base_dir()+"/vars", mdFile)
                        self.addVariableReferences(variable, filename, self.config.get_base_dir()+"/templates", mdFile)
                        
                        if self.where_referenced == "":
                            mdFile.new_line("No references found")
                        

            except yaml.YAMLError as exc:
                print(exc)

    def addVariableReferences(self, variable, filename, directory, mdFile):
        for (dirpath, dirnames, refFilenames) in walk(directory):
            for refFilename in refFilenames:
                if dirpath+"/"+refFilename != filename:
                    with open(dirpath+"/"+refFilename) as f:
                        contents = f.read()
                        if variable in contents:
                            self.where_referenced = os.path.relpath(dirpath+"/"+refFilename, self.config.get_base_dir())
                            mdFile.new_line(self.where_referenced)

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