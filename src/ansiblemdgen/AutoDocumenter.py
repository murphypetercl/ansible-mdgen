#!/usr/bin/env python3

from ansiblemdgen.Config import SingleConfig
import sys
import yaml
import os
import shutil
from os import walk
from ansiblemdgen.Utils import SingleLog,FileUtils
from mdutils.mdutils import MdUtils
from ansiblemdgen.AutoDocumenterIndex import IndexWriter
from ansiblemdgen.AutoDocumenterTasks import TasksWriter
from ansiblemdgen.AutoDocumenterVariables import VariablesWriter
from ansiblemdgen.AutoDocumenterFilesTemplates import FilesTemplatesWriter
from ansiblemdgen.AutoDocumenterAppendix import AppendixWriter

from ansiblemdgen.AutoDocumenterBase import WriterBase

class Writer(WriterBase):

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

        self.makeDocsDir(self.config.get_output_dir())

        indexWriter = IndexWriter()
        indexWriter.render()

        tasksWriter = TasksWriter()
        tasksWriter.render()

        variablesWriter = VariablesWriter()
        variablesWriter.render()

        if self.config.output_files is True or self.config.output_templates is True:
            filesTemplatesWriter = FilesTemplatesWriter()
            filesTemplatesWriter.render()

        if self.config.appendix is not None:
            appendixWriter = AppendixWriter()
            appendixWriter.render()