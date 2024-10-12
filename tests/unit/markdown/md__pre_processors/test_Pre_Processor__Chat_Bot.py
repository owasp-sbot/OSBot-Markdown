from unittest import TestCase

import pytest

from osbot_markdown.markdown.md__pre_processors.Pre_Processor__Chat_Bot import Pre_Processor__Chat_Bot


@pytest.mark.skip("needs fixing")       # todo: fix this test
class test_Pre_Processor__Chat_Bot(TestCase):

    def test_run(self):
        md           = None  # or a mock markdown instance if needed
        preprocessor = Pre_Processor__Chat_Bot(md)

        input_lines = [
            'first line',
            """{{chatbot url="/api/chat/completions" 
                 name="ChatBot" 
                 model="gpt-4" 
                 platform="web" 
                 provider="OpenAI" 
                 channel="chatbot-main" 
                 system_prompt="only speak in emojis" 
                 }}""",
            'last line.'
        ]

        expected_output = [
            'first line',
            """<chatbot url="/api/chat/completions" name="ChatBot" model="gpt-4" platform="web" provider="OpenAI" channel="chatbot-main" system_prompt="only speak in emojis"></chatbot-openai>""",
            'last line.'
        ]

        output_lines = preprocessor.run(input_lines)
        assert output_lines == expected_output
