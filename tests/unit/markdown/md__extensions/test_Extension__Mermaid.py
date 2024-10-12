from unittest import TestCase
from markdown import Markdown

from osbot_markdown.markdown.md__extensions.Extension__Mermaid import Extension__Mermaid


class test_Extension__Mermaid(TestCase):

    def setUp(self):
        self.md = Markdown(extensions=[Extension__Mermaid()])
        self.mermaid_code = '''
        {{ mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
        }}
        '''
        self.expected_html = '<pre class="mermaid">graph TD;\n    A--&gt;B;\n    A--&gt;C;\n    B--&gt;D;\n    C--&gt;D;</pre>'

    def test_extension_registration(self):                                      # Test that the extension is properly registered with Markdown
        self.assertIsInstance(self.md, Markdown)
        registered_block_processors = [ext.__class__.__name__ for ext in self.md.parser.blockprocessors]

        assert 'Block_Processor__Mermaid' in registered_block_processors

    def test_mermaid_block(self):                                               # Test that a mermaid block is converted correctly
        html_output = self.md.convert(self.mermaid_code).strip()
        assert html_output == self.expected_html