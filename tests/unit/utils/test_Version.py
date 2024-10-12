from unittest import TestCase

import osbot_markdown
from osbot_markdown.utils.Version import Version, version__osbot_markdown
from osbot_utils.utils.Files import file_name, folder_name, parent_folder





class test_Version(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.version = Version()

    def test_path_code_root(self):
        assert self.version.path_code_root() == osbot_markdown.path

    def test_path_version_file(self):
        with self.version as _:
            assert parent_folder(_.path_version_file()) == osbot_markdown.path
            assert file_name    (_.path_version_file()) == 'version'

    def test_value(self):
        assert self.version.value() == version__osbot_markdown