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

        indexWriter = IndexWriter()
        indexWriter.render()

        tasksWriter = TasksWriter()
        tasksWriter.render()

        variablesWriter = VariablesWriter()
        variablesWriter.render()

    def makeDocsDir(self):
        output_directory = self.config.get_output_dir()
        self.log.debug("(makeDocsDir) Output Directory: "+output_directory)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
