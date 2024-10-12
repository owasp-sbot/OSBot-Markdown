from unittest import TestCase

from osbot_markdown.markdown.md__pre_processors.Pre_Processor__IFrame import Pre_Processor__IFrame


class test_Pre_Processor__IFrame(TestCase):

    def test_run(self):
        md           = None  # or a mock markdown instance if needed
        preprocessor = Pre_Processor__IFrame(md)

        input_lines = [
            'first line',
            '{{iframe:/docs}}',
            'last line.'
        ]

        expected_output = [
            'first line',
            '<iframe src="/docs" width="100%" height="500px" style="border:1px solid"></iframe>',
            'last line.'
        ]

        output_lines = preprocessor.run(input_lines)
        assert output_lines == expected_output
