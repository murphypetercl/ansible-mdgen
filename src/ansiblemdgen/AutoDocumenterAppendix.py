#!/usr/bin/env python3

from ansiblemdgen.Config import SingleConfig
import sys
import yaml
import os
from os import walk
from ansiblemdgen.Utils import SingleLog,FileUtils
from mdutils.mdutils import MdUtils

class AppendixWriter:


    def __init__(self):
        self.config = SingleConfig()
        self.log = SingleLog()


    def render(self):
        self.createAppendixMDFile()


    def createAppendixMDFile(self):

        self.log.info("(createAppendixMDFile) Create Appendix MD File")

        mdFile = MdUtils(file_name=self.config.get_output_dir()+"/appendix.md")

        self.createMDFileContent(mdFile)

        mdFile.create_md_file()
        self.log.info("(createAppendixMDFile) Create Appendix MD File Complete")
    
    def createMDFileContent(self, mdFile):

        mdFile.new_header(level=1, title='Appendix')

        mdFile.new_line("---")

        if 'references' in self.config.appendix.keys():
            mdFile.new_header(level=2, title='References')

            table_entries = ["Description", "Link"]
            for ref in self.config.appendix["references"]:
                table_entries.extend([ref["description"], mdFile.new_inline_link(ref["link"])])

            num_rows = len(self.config.appendix["references"])

            mdFile.new_table(columns=2, rows=num_rows+1, text=table_entries, text_align='left')
