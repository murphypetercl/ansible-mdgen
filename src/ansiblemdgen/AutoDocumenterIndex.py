#!/usr/bin/env python3

from ansiblemdgen.Config import SingleConfig
import sys
import yaml
import os
from os import walk
from ansiblemdgen.Utils import SingleLog,FileUtils
from mdutils.mdutils import MdUtils
from ansiblemdgen.AutoDocumenterTasks import TasksWriter
from ansiblemdgen.AutoDocumenterVariables import VariablesWriter

class IndexWriter:


    def __init__(self):
        self.config = SingleConfig()
        self.log = SingleLog()


    def render(self):
        self.createIndexMDFile()


    def createIndexMDFile(self):

        self.log.info("(createIndexMDFile) Create Index MD File")
        role_name = self.config.get_base_dir()[self.config.get_base_dir().rfind('/')+1:]
        page_title = "Role: "+role_name

        mdFile = MdUtils(file_name=self.config.get_output_dir()+"/index.md")

        self.createMDFileContent(mdFile)

        mdFile.create_md_file()
        self.log.info("(createIndexMDFile) Create Index MD File Complete")
    
    def createMDFileContent(self, mdFile):
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
        
        role_name = self.config.get_base_dir()[self.config.get_base_dir().rfind('/')+1:]
        mdFile.new_header(level=1, title='About')

        mdFile.new_line("---")
        mdFile.new_header(level=2, title='Role Name') 
        mdFile.new_line(role_name) 
        mdFile.new_line()

        mdFile.new_line("---")
        mdFile.new_header(level=2, title='Description') 
        mdFile.new_line(description)
        mdFile.new_line()

        mdFile.new_line("---")
        mdFile.new_header(level=2, title='Dependencies') 

        if dependencies != []:
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
        mdFile.new_header(level=2, title='Information') 

        table_entries = ["Author", "Company", "License","Minimum Ansible Version"]
        table_entries.extend([author, company, license, str(min_ansible_version)])
        mdFile.new_line()

        mdFile.new_table(columns=4, rows=2, text=table_entries, text_align='center')
