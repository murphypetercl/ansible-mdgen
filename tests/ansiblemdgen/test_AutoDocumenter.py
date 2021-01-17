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

        assert os.path.isfile(str(tmpdir)+"/docs/index.md")
        assert os.path.isfile(str(tmpdir)+"/docs/defaults/main.md")
        assert os.path.isfile(str(tmpdir)+"/docs/tasks/directories.md")
        assert os.path.isfile(str(tmpdir)+"/docs/tasks/main.md")
        assert os.path.isfile(str(tmpdir)+"/docs/tasks/volumes.md")
        assert os.path.isfile(str(tmpdir)+"/docs/tasks/minio/minio.md")
        assert os.path.isfile(str(tmpdir)+"/docs/tasks/minio/users.md")
        assert os.path.isfile(str(tmpdir)+"/docs/tasks/minio/firewall.md")
        assert os.path.isfile(str(tmpdir)+"/docs/variables/main.md")