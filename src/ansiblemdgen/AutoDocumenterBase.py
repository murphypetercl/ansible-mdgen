from ansiblemdgen.Config import SingleConfig
from ansiblemdgen.Utils import SingleLog
import os
from os import walk


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
        for (dirpath, dirnames, filenames) in walk(directory):
            for filename in filenames:
                self.createMDFile(dirpath, filename, output_directory)

            for dirname in dirnames:
                self.iterateOnFilesAndDirectories(dirpath+"/"+dirname, output_directory+"/"+dirname)

    def iterateOnCombinations(self, directory, combinations, output_directory):
        for combination in combinations:
            self.createMDCombinationFile(combination['filename'], directory, output_directory, combination['files_to_combine'])
