from ansiblemdgen.Config import SingleConfig
from ansiblemdgen.Utils import SingleLog
import os
from os import walk
import yaml

class WriterBase:

    config = None

    def __init__(self):
        self.config = SingleConfig()
        self.log = SingleLog()

        self.log.info("Base directory: "+self.config.get_base_dir())

    def makeDocsDir(self, doc_directory):
        self.log.debug("(makeDocsDir) Output Directory: "+doc_directory)
        if not os.path.exists(doc_directory):
            os.makedirs(doc_directory)
    
    def iterateOnFilesAndDirectories(self, directory, output_directory):
        self.log.debug("(iterateOnFilesAndDirectories) directory: "+ directory)
        self.log.debug("(iterateOnFilesAndDirectories) output_directory: "+ output_directory)

        for (dirpath, dirnames, filenames) in walk(directory):
            self.log.debug("(iterateOnFilesAndDirectories) dirpath: "+ dirpath)
            relPath = dirpath.replace(directory,"")

            for filename in filenames:
                #ignore any existing md files and vault encrypted files
                if not filename.endswith('.md') and self.isFileVaultEncrypted(dirpath, filename) is False:
                        self.createMDFile(dirpath, filename, output_directory+"/"+relPath)

    def iterateOnCombinations(self, directory, combinations, output_directory):
        for combination in combinations:
            self.createMDCombinationFile(combination['filename'], directory, output_directory, combination['files_to_combine'])

    def isFileVaultEncrypted(self, directory, filename):
        with open(directory+"/"+filename, 'r') as stream:
            data = stream.readlines()
            if data[0].startswith('$ANSIBLE_VAULT;1.1;AES256'):
                return True
            else:
                return False