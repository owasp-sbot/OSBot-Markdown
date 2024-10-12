from unittest import TestCase
from markdown                                           import Markdown
from osbot_markdown.markdown.Markdown_Parser            import Markdown_Parser
from osbot_utils.utils.Misc                             import list_set


class test_Markdown_Parser(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.markdown_parser = Markdown_Parser()

    def test_parse_markdown_text(self):
        markdown_text = "# this is an header"
        markdown_text__with_meta  ="""\
meta_1: value 1
meta_2: value 2
-----

# back to markdown
1234"""

        with self.markdown_parser as _:
            result_1 = _.parse(markdown_text)
            assert list_set(result_1) == ['html', 'markdown_text', 'meta']
            assert result_1 == {'html'         : '<h1>this is an header</h1>' ,
                                'markdown_text': markdown_text              ,
                                'meta'         : {}                           }

            result_2 = _.parse(markdown_text__with_meta)
            assert result_2 == { 'html'         : '<h1>back to markdown</h1>\n<p>1234</p>'      ,
                                 'markdown_text': markdown_text__with_meta                      ,
                                 'meta'         : {'meta_1': 'value 1', 'meta_2': 'value 2'}}


    def test_markdown_to_html_and_metadata(self):

        markdown_text__with_meta = """\
meta_1: value 1
meta_2: 42
meta_3: [1,2,3]
meta_4: multi_lines
        text are joined together
        with spaces
meta_5: duplicated values
meta_5: are also joined together with spaces
meta_6 : a space after : is not supported

# back to markdown
1234"""
        with self.markdown_parser as _:
            result = _.markdown_to_html_and_metadata(markdown_text__with_meta)
            assert result == { 'html'    : '<p>meta_6 : a space after : is not supported</p>\n<h1>back to markdown</h1>\n<p>1234</p>'      ,
                               'metadata': {'meta_1': 'value 1',
                                            'meta_2': '42',
                                            'meta_3': '[1,2,3]',                                            # note, markdown doesn't support natively arrays
                                            'meta_4': 'multi_lines text are joined together with spaces' ,
                                            'meta_5': 'duplicated values are also joined together with spaces'
                                            }}

    def test_markdown_ex_mermaid(self):
        md_text = """\
# Sample Markdown with Mermaid
Here is a Mermaid diagram:

{{mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
}}
"""
        expected_html = ('<h1>Sample Markdown with Mermaid</h1>\n'
                         '<p>Here is a Mermaid diagram:</p>\n'
                         '<pre class="mermaid">graph TD;\n'
                         '    A--&gt;B;\n'
                         '    A--&gt;C;\n'
                         '    B--&gt;D;\n'
                         '    C--&gt;D;</pre>')
                         # '<script type="module">\n'
                         # "                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.esm.min.mjs';\n"
                         # '                mermaid.initialize({ startOnLoad: true });\n'
                         # '            </script>')
        html = self.markdown_parser.markdown_to_html(md_text)
        assert html == expected_html

    def test_video_extension(self):
        md_text = """\
# Video extension

Here is a video:

[video:https://www.example.com/video.mp4]
        """
        expected_html = ('<h1>Video extension</h1>\n'
                         '<p>Here is a video:</p>\n'
                         '<p>\n'
                         '<video controls="" width="500"><source '
                         'src="https://www.example.com/video.mp4" type="video/mp4" /></video>\n'
                         '</p>')
        assert self.markdown_parser.markdown_to_html(md_text) == expected_html


    def test_markdown(self):
        with self.markdown_parser as _:
            markdown = _.markdown()
            assert type(markdown) is Markdown

    def test_markdown_to_html(self):

        markdown_text = "# This is a header\n\n* bullet 1\n* bullet 2"
        expected_html = "<h1>This is a header</h1>\n<ul>\n<li>bullet 1</li>\n<li>bullet 2</li>\n</ul>"

        assert self.markdown_parser.markdown_to_html(markdown_text) == expected_html

    def test_content_to_html(self):
        content = "---\ntitle: Test Title\n---\n\n# This is a header\n\n* bullet 1\n* bullet 2"
        expected_html = "<h1>This is a header</h1>\n<ul>\n<li>bullet 1</li>\n<li>bullet 2</li>\n</ul>"
        assert self.markdown_parser.content_to_html(content) == expected_html

    def test_default_extension__table(self):
        markdown_text ="""\
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| cell 1   | cell 2   | cell 3   |"""
        expected_html = ('<table>\n' '<thead>\n' '<tr>\n' '<th>Header 1</th>\n' '<th>Header 2</th>\n' '<th>Header 3</th>\n' '</tr>\n' '</thead>\n'
                         '<tbody>\n' '<tr>\n' '<td>cell 1</td>\n' '<td>cell 2</td>\n' '<td>cell 3</td>\n' '</tr>\n' '</tbody>\n' '</table>')


        assert self.markdown_parser.markdown_to_html(markdown_text) == expected_html

    def test_default_extension__attribute_lists(self):
        markdown_text ="""\
This is a paragraph.
{: #an_id .a_class }

A setext style header {: #setext}
=================================
### A hash style header ### {: #hash }
"""
        expected_html = ('<p class="a_class" id="an_id">This is a paragraph.</p>\n'
                         '<h1 id="setext">A setext style header</h1>\n'
                         '<h3 id="hash">A hash style header</h3>')
        assert self.markdown_parser.markdown_to_html(markdown_text) == expected_html

    def test_default_extension__definition_lists(self):
        markdown_text = """\
Apple
:   Pomaceous fruit of plants of the genus Malus in
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.        
"""
        expected_html = ('<dl>\n'
                         '<dt>Apple</dt>\n'
                         '<dd>Pomaceous fruit of plants of the genus Malus in\n'
                         'the family Rosaceae.</dd>\n'
                         '<dt>Orange</dt>\n'
                         '<dd>The fruit of an evergreen tree of the genus Citrus.        </dd>\n'
                         '</dl>')
        assert self.markdown_parser.markdown_to_html(markdown_text) == expected_html


    def test_default_extension__foot_notes(self):
        markdown_text = """\
Footnotes[^1] have a label[^@#$%] and the footnote's content.

[^1]: This is a footnote content.
[^@#$%]: A footnote on the label: "@#$%"."""
        expected_html = ('<p>Footnotes<sup id="fnref:1"><a class="footnote-ref" ' 'href="#fn:1">1</a></sup> have a label<sup id="fnref:@#$%"><a ' 'class="footnote-ref" href="#fn:@#$%">2</a></sup> and the footnote\'s ' 'content.</p>\n' 
                         '<div class="footnote">\n' '<hr />\n' '<ol>\n' '<li id="fn:1">\n' '<p>This is a footnote content.&#160;<a class="footnote-backref" ' 'href="#fnref:1" title="Jump back to footnote 1 in the text">&#8617;</a></p>\n' 
                         '</li>\n' '<li id="fn:@#$%">\n' '<p>A footnote on the label: "@#$%".&#160;<a class="footnote-backref" ' 'href="#fnref:@#$%" title="Jump back to footnote 2 in the ' 'text">&#8617;</a></p>\n' '</li>\n' '</ol>\n' '</div>')

        assert self.markdown_parser.markdown_to_html(markdown_text) == expected_html


#     def test_default_extension__(self):
#         markdown_text = """\
# """
#         expected_html = ''
#         pprint(self.markdown_parser.markdown_to_html(markdown_text))
#         #assert self.markdown_parser.markdown_to_html(markdown_text) == expected_html
#
#
#     def test_default_extension__(self):
#         markdown_text = """\
# """
#         expected_html = ''
#         pprint(self.markdown_parser.markdown_to_html(markdown_text))
#         #assert self.markdown_parser.markdown_to_html(markdown_text) == expected_html
#
#     def test_default_extension__(self):
#         markdown_text = """\
# """
#         expected_html = ''
#         pprint(self.markdown_parser.markdown_to_html(markdown_text))
#         #assert self.markdown_parser.markdown_to_html(markdown_text) == expected_html
