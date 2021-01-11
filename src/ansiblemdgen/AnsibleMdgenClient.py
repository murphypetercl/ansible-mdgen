#!/usr/bin/env python3

import os
import sys
import argparse
from ansiblemdgen.Config import SingleConfig
from ansiblemdgen.Utils import SingleLog
from ansiblemdgen.AutoDocumenter import Writer
from ansiblemdgen import __version__

class AnsibleMdgen:

    def __init__(self):

        self.config = SingleConfig()
        self.log = SingleLog(self.config.debug_level)
        args = self._cli_args()
        self._parse_args(args)

        print('Project Directory: '+self.config.get_base_dir())
        print('Output Directory: '+self.config.output_dir)

        writer = Writer()
        writer.render()
    
    def _cli_args(self):

        """
        use argparse for parsing CLI arguments
        :return: args objec
        """
        usage = '''ansible-mdgen [project_directory] [options]'''
        parser = argparse.ArgumentParser(description='Generate documentation from roles', usage=usage)

        parser.add_argument('project_dir', nargs='?', default=os.getcwd(),help="Project directory to scan, "
                                                                               "if empty current working will be used.")

        parser.add_argument('-C',"--conf", nargs='?', default="",help="Specify a configuration file")
        
        

        parser.add_argument('-o', action="store", dest="output", type=str, help='Define the destination '
                                                                               'folder of your documenation')

        parser.add_argument('-w', action="store_true", help='Clear the output directory without asking')
        parser.add_argument('-y', action='store_true', help='Overwrite the output without asking')

        parser.add_argument("--sample-config", action='store_true', help='Print the sample configuration yaml file')

        parser.add_argument('-V',"--version", action='store_true', help='Get versions')

        # print('debug_level')
        debug_level = parser.add_mutually_exclusive_group()
        debug_level.add_argument('-v', action='store_true', help='Set debug level to info')
        debug_level.add_argument('-vv', action='store_true', help='Set debug level to debug')
        debug_level.add_argument('-vvv', action='store_true', help='Set debug level to trace')

        return parser.parse_args()

    def _parse_args(self,args):

        """
        Use an args object to apply all the configuration combinations to the config object
        :param args:
        :return: None
        """
        self.config.set_base_dir(os.path.abspath(args.project_dir))

        # search for config file
        if args.conf != "":
            conf_file = os.path.abspath(args.conf)
            if os.path.isfile(conf_file) and os.path.basename(conf_file) == self.config.config_file_name:
                self.config.load_config_file(conf_file)
                # re apply log level based on config
                self.log.set_level(self.config.debug_level)
            else:
                self.log.warn("No configuration file found: "+conf_file)
        else:
            conf_file = self.config.get_base_dir()+"/"+self.config.config_file_name
            if os.path.isfile(conf_file):
                self.config.load_config_file(conf_file)
                # re apply log level based on config
                self.log.set_level(self.config.debug_level)

        # sample configuration
        if args.sample_config:
            print(self.config.sample_config)
            sys.exit()

        # version
        if args.version:
            print(__version__)
            sys.exit()

        # Debug levels
        if args.v is True:
            self.log.set_level("info")
        elif args.vv is True:
            self.log.set_level("debug")
        elif args.vvv is True:
            self.log.set_level("trace")

        # Clear
        if args.w is True:
            self.config.clear_output = True

        # Overwrite
        if args.y is True:
            self.config.output_overwrite = True

        # output dir
        if args.output is not None:
            self.config.output_dir = os.path.abspath(args.output)
        
        # need to send the message after the log levels have been set
        self.log.debug("using configuration file: "+conf_file)

        # some debug
        self.log.debug(args)
        self.log.info("Using base dir: "+self.config.get_base_dir())