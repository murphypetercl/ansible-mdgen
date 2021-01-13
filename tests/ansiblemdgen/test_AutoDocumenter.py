#!/usr/bin/python3
import os

from ansiblemdgen.Config import SingleConfig
from ansiblemdgen.AutoDocumenter import Writer

project_dir = os.path.realpath(os.path.dirname(os.path.realpath(__file__))+"../../../")
sample_project = os.path.realpath(os.path.dirname(os.path.realpath(__file__))+"../../test-roles/minio")


class TestGenerator(object):

    def test_render(self,tmpdir):
        config = SingleConfig()
        config.output_dir = str(tmpdir)+"/docs"
        config.set_base_dir(sample_project)

        writer = Writer()
        writer.render()

        rendered_file = open(str(tmpdir)+"/docs/index.md", "r")
        line = rendered_file.readline()

        print(line)
        assert line == "\n"