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

    _all_var_meta = {}

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

        self.config.yaml_extension
        mdFile = MdUtils(file_name=output_directory+"/" +
                         filename.replace(self.config.yaml_extension,''))

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
                # vault encrypted variables throw errors on loading so replacing the ! with ____ to workaround that and reverting it when outputting to the value.
                stream = stream.read().replace('!vault','____vault')
                variables = yaml.safe_load(stream)

                if variables != None:
                    for variable in variables:

                        mdFile.new_header(level=2, title=variable)

                        if(variable in self._all_var_meta):
                            mdFile.new_paragraph(yaml.safe_dump(self._all_var_meta[variable]["description"],  default_flow_style=False, allow_unicode=True))
                                
                        mdFile.new_line("```")
                        mdFile.new_paragraph(yaml.safe_dump(variables[variable],  default_flow_style=False, allow_unicode=True).replace('____vault','!vault'))
                        mdFile.new_line("```")

                        self.where_referenced = ""
                        self.addVariableReferences(variable, filename, self.config.get_base_dir()+"/tasks", mdFile)
                        self.addVariableReferences(variable, filename, self.config.get_base_dir()+"/defaults", mdFile)
                        self.addVariableReferences(variable, filename, self.config.get_base_dir()+"/vars", mdFile)
                        self.addVariableReferences(variable, filename, self.config.get_base_dir()+"/templates", mdFile)
                        
                        table_entries = []
                        table_data = []

                        if (not self.config.transpose_variable_table):
                            num_columns = 1

                            if(variable in self._all_var_meta):
                                for metaKey in self._all_var_meta[variable].keys():
                                    # Description is displayed outside of table so ignore this here
                                    if (metaKey.lower() != 'description'):
                                        table_entries.append(metaKey.capitalize().replace('_',' ').replace('-',' '))
                                        table_data.append(str(self._all_var_meta[variable][metaKey]))
                                        num_columns = num_columns + 1 

                                table_entries.append("Where referenced")
                                table_data.append(self.where_referenced)

                                table_entries.extend(table_data)

                                num_rows = 2

                                mdFile.new_table(columns=num_columns, rows=num_rows, text=table_entries, text_align='left')
                        else:
                            num_columns = 2
                            num_rows = 1
                            table_entries.append('Meta')
                            table_entries.append('Value')

                            if(variable in self._all_var_meta):
                                for metaKey in self._all_var_meta[variable].keys():
                                    # Description is displayed outside of table so ignore this here
                                    if (metaKey.lower() != 'description'):
                                        table_data.append('<strong>'+metaKey.capitalize().replace('_',' ').replace('-',' ')+'</strong>')
                                        table_data.append(str(self._all_var_meta[variable][metaKey]))
                                        num_rows = num_rows + 1 

                                table_data.append('<strong>Where referenced</strong>')
                                table_data.append(self.where_referenced)
                                table_entries.extend(table_data)
                                num_rows = num_rows + 1

                                mdFile.new_table(columns=num_columns, rows=num_rows, text=table_entries, text_align='left')
                        

            except yaml.YAMLError as exc:
                print(exc)

    def addVariableReferences(self, variable, filename, directory, mdFile):
        for (dirpath, dirnames, refFilenames) in walk(directory):
            for refFilename in refFilenames:
                if dirpath+"/"+refFilename != filename:
                    with open(dirpath+"/"+refFilename) as f:
                        contents = f.read()
                        if variable in contents:
                            self.where_referenced = self.where_referenced + os.path.relpath(dirpath+"/"+refFilename, self.config.get_base_dir()) + "<br/>"

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
                
                if (line1 != ''):
                    # step3 take the main key value from the annotation
                    parts = line1.split(":",1)
                    key = str(parts[0].strip())
                    value = str(parts[1].strip())

                    if key not in self._all_var_meta.keys():
                        self._all_var_meta[key] = []

                    self._all_var_meta[key] = {'description': value}
                else:
                    # if line has no data then this must be the start of meta block
                    try:
                        self.getVarMeta(file)
                    except Exception as err:
                        print("File: "+filename+" - "+str(err))

    def getVarMeta(self, file):
        meta = ""
        varLine = file.readline()
        while(varLine):
            if (varLine[0] != '#'):
                raise Exception("Missing @var_end annotation or blank line identified. Please fix variable annotation.")

            if (varLine.strip() == '# @var_end'):
                break
            else:
                meta += varLine.replace('# ','')
                varLine = file.readline()

        _meta = yaml.safe_load(meta)

        for key in _meta.keys():
            if key not in self._all_var_meta.keys():
                self._all_var_meta[key] = _meta.get(key)
        

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
