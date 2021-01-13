#!/usr/bin/env python3

import os
import yaml
from ansiblemdgen.Utils import Singleton
from ansiblemdgen.Utils import SingleLog

class Config:
    sample_config = """---
# About Ansible mdgen: Generate documentation from roles based on the task names
# https://github.com/......
# filename: .ansible-mdgen.yaml
# base directory to scan, relative dir to configuration file 
# base_dir: "./"
# documentation output directory, relative dir to configuration file.
output_dir: "./docs"

output_overwrite = True
clear_output = True

# set the debug level: trace | debug | info | warn
# see -v | -vv | -vvv
# debug_level: "warn"
"""
    # path to the documentation output dir
    output_dir = "./docs"
    output_tasks_dir = "tasks"
    output_defaults_dir = "defaults"
    output_variables_dir = "variables"

    output_overwrite = False
    clear_output = False

    # project base directory
    _base_dir = ""

    # current directory of this object,
    # used to get the default template directory
    script_base_dir = ""

    # name of the config file to search for
    config_file_name = ".ansible-mdgen.yaml"
    # if config file is not in root of project, this is used to make output relative to config file
    _config_file_dir = ""

    tasks = None
    defaults = None
    variables = None

    # default debug level
    debug_level = "warn"

    def set_base_dir(self,dir):
        self._base_dir = dir

    def get_base_dir(self):
        return self._base_dir

    def _set_is_role(self):
        # is role
        self.project_name = os.path.basename(self._base_dir)
        if os.path.isdir(self._base_dir+"/roles"):
            self.is_role = False
        elif os.path.isdir(self._base_dir+"/tasks"):
            self.is_role = True
        else:
            self.is_role = None

    def get_output_dir(self):
        """
        get the relative path to cwd of the output directory for the documentation
        :return: str path
        """
        if self.output_dir == "":
            return os.path.realpath(self._base_dir)
        elif os.path.isabs(self.output_dir):
            return os.path.realpath(self.output_dir)
        elif not os.path.isabs(self.output_dir):
            return os.path.realpath(self.get_base_dir()+"/"+self.output_dir)

    def get_output_tasks_dir(self):
        """
        get the relative path to cwd of the output directory for the documentation
        :return: str path
        """
        if self.output_tasks_dir == "":
            return os.path.realpath(self.get_output_dir())
        elif os.path.isabs(self.output_tasks_dir):
            return os.path.realpath(self.output_tasks_dir)
        elif not os.path.isabs(self.output_tasks_dir):
            return os.path.realpath(self.get_output_dir()+"/"+self.output_tasks_dir)

    def get_output_defaults_dir(self):
        """
        get the relative path to cwd of the output directory for the documentation
        :return: str path
        """
        if self.output_defaults_dir == "":
            return os.path.realpath(self.get_output_dir())
        elif os.path.isabs(self.output_defaults_dir):
            return os.path.realpath(self.output_defaults_dir)
        elif not os.path.isabs(self.output_defaults_dir):
            return os.path.realpath(self.get_output_dir()+"/"+self.output_defaults_dir)

    def get_output_variables_dir(self):
        """
        get the relative path to cwd of the output directory for the documentation
        :return: str path
        """
        if self.output_variables_dir == "":
            return os.path.realpath(self.get_output_dir())
        elif os.path.isabs(self.output_variables_dir):
            return os.path.realpath(self.output_variables_dir)
        elif not os.path.isabs(self.output_variables_dir):
            return os.path.realpath(self.get_output_dir()+"/"+self.output_variables_dir)

    def load_config_file(self, file):

        allow_to_overwrite = [
            "base_dir",
            "output_dir",
            "tasks",
            "defaults",
            "variables",
            "debug_level",
        ]

        with open(file, 'r') as yaml_file:

            try:
                self._config_file_dir = os.path.dirname(os.path.realpath(file))
                data = yaml.safe_load(yaml_file)
                if data:
                    for item_to_configure in allow_to_overwrite:
                        if item_to_configure in data.keys():
                            self.__setattr__(item_to_configure,data[item_to_configure])

            except yaml.YAMLError as exc:
                print(exc)


class SingleConfig(Config, metaclass=Singleton):
    pass