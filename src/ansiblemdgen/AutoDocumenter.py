#!/usr/bin/env python3

from ansiblemdgen.Config import SingleConfig
import sys
import yaml
import os
import shutil
from os import walk
from ansiblemdgen.Utils import SingleLog,FileUtils
from mdutils.mdutils import MdUtils
from ansiblemdgen.AutoDocumenterTasks import TasksWriter
from ansiblemdgen.AutoDocumenterVariables import VariablesWriter

class Writer:

    config = None
    tasks_dir = None

    def __init__(self):
        self.config = SingleConfig()
        self.log = SingleLog()

        self.log.info("Base directory: "+self.config.get_base_dir())

    def render(self):

        if os.path.exists(self.config.get_output_dir()) and len(os.listdir(self.config.get_output_dir())) > 0 and self.config.clear_output is False:
            SingleLog.print("There are existing files in the output directory ",self.config.get_output_dir())
            clear_results = FileUtils.query_yes_no("Do you want to clear the directory and rebuild all the docs?")
            if clear_results == "yes":
                shutil.rmtree(self.config.get_output_dir())

        if os.path.exists(self.config.get_output_dir()) and self.config.output_overwrite is False:
            SingleLog.print("The files in the output directory will be overwritten: ",self.config.get_output_dir())
            overwrite_results = FileUtils.query_yes_no("Do you want to continue?")
            if overwrite_results != "yes":
                sys.exit()

        self.makeDocsDir()

        self.createIndexMDFile()

        tasksWriter = TasksWriter()
        tasksWriter.render()

        variablesWriter = VariablesWriter()
        variablesWriter.render()


    def makeDocsDir(self):
        output_directory = self.config.get_output_dir()
        self.log.debug("(makeDocsDir) Output Directory: "+output_directory)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
    
    def createIndexMDFile(self):

        self.log.info("(createIndexMDFile) Create Index MD File")
        page_title = self.config.get_base_dir()[self.config.get_base_dir().rfind('/')+1:]
        author = ''
        description = ''
        company = ''
        license = ''
        min_ansible_version = ''
        dependencies = []

        galaxy_metafile = self.config.get_base_dir()+'/meta/main.yml'

        if os.path.isfile(galaxy_metafile):
            with open(galaxy_metafile, 'r') as stream:
                try:
                    metadata = yaml.safe_load(stream)
                    author = metadata.get("galaxy_info").get('author')
                    description = metadata.get("galaxy_info").get('description')
                    company = metadata.get("galaxy_info").get('company')
                    license = metadata.get("galaxy_info").get('license')
                    min_ansible_version = metadata.get("galaxy_info").get('min_ansible_version')
                    dependencies = metadata.get('dependencies')

                except yaml.YAMLError as exc:
                    print(exc)
        else:
            self.log.info("(createIndexMDFile) No meta/main.yml file")

        mdFile = MdUtils(file_name=self.config.get_output_dir()+"/index.md",title=page_title)

        mdFile.new_line("---")
        mdFile.new_header(level=1, title='Description', style='setext') 
        mdFile.new_line(description)
        mdFile.new_line()

        mdFile.new_line("---")
        mdFile.new_header(level=1, title='Dependencies', style='setext') 

        if dependencies != None:
            dependency_table_entries = ["Dependencies"]

            for dependency in dependencies:
                dependency_table_entries.extend([yaml.dump(dependency,  default_flow_style=False)])
                for dep_part in dependency:
                    mdFile.new_line("> "+dep_part+": "+dependency[dep_part])
                mdFile.new_line()
        else:
            mdFile.new_line('None')
        mdFile.new_line()

        mdFile.new_line("---")
        mdFile.new_header(level=1, title='Information', style='setext') 

        table_entries = ["Author", "Company", "License","Minimum Ansible Version"]
        table_entries.extend([author, company, license, str(min_ansible_version)])
        mdFile.new_line()

        mdFile.new_table(columns=4, rows=2, text=table_entries, text_align='center')

        mdFile.new_table_of_contents(table_title='Contents', depth=2)

        mdFile.create_md_file()
        self.log.info("(createIndexMDFile) Create Index MD File Complete")
