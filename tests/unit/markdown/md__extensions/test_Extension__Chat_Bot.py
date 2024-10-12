from unittest import TestCase

import pytest
from markdown import Markdown

from osbot_markdown.markdown.md__extensions.Extension__Chat_Bot import Extension__Chat_Bot


class test_Extension__Chat_Bot(TestCase):

    ok__all_attr__markdown_code   = """{{chatbot url="/api/chat/completions" 
                                                 name="ChatBot" 
                                                 model="gpt-4" 
                                                 platform="web" 
                                                 provider="OpenAI" 
                                                 channel="chatbot-main" 
                                                 system_prompt="only speak in emojis"}}"""
    ok__all_attr__html            = """<p><chatbot-openai url="/api/chat/completions" name="ChatBot" model="gpt-4" platform="web" provider="OpenAI" channel="chatbot-main" system_prompt="only speak in emojis"></chatbot-openai></p>"""

    ok__no_attr__markdown_code    = """{{chatbot \n }}"""                                # with a new line works
    ok__no_attr__html             = """<p><chatbot-openai ></chatbot-openai></p>"""

    ok__one_attr__markdown_code   = """{{chatbot url="/api/chat/completions" \n }}"""
    ok__one_attr__html            = """<p><chatbot-openai url="/api/chat/completions"></chatbot-openai></p>"""

    ok__two_attr__markdown_code   = """{{chatbot url="/api/chat/completions" 
                                              name="ChatBot" }}"""
    ok__two_attr__html            = """<p><chatbot-openai url="/api/chat/completions" name="ChatBot"></chatbot-openai></p>"""

    ok__misc_order__markdown_code = """{{chatbot platform="web" channel="chatbot-main" url="/api/chat/completions" \n }}"""
    ok__misc_order__html          = """<p><chatbot-openai platform="web" channel="chatbot-main" url="/api/chat/completions"></chatbot-openai></p>"""

    fail__no_attr__markdown_code   = """{{chatbot }}"""                                 # without a new line doesn't
    fail__one_attr__markdown_code = """{{chatbot url="/api/chat/completions" }}"""
    #fail__no_attr__html            = """"""


    def setUp(self):
        self.md = Markdown(extensions=[Extension__Chat_Bot()])
        #self.markdown_code = """{{chatbot url="/api/chat/completions" name="ChatBot" model="gpt-4" platform="web" provider="OpenAI" channel="chatbot-main" system_prompt="only speak in emojis"}}"""
        #self.expected_html = """<p><chatbot-openai url="/api/chat/completions" name="ChatBot" model="gpt-4" platform="web" provider="OpenAI" channel="chatbot-main" system_prompt="only speak in emojis"></chatbot-openai></p>"""

    def test_extension_registration(self):                                      # Test that the extension is properly registered with Markdown
        self.assertIsInstance(self.md, Markdown)
        registered_block_processors = [ext.__class__.__name__ for ext in self.md.preprocessors]
        assert 'Pre_Processor__Chat_Bot' in registered_block_processors

    @pytest.mark.skip("needs fixing")       # todo: fix this test
    def test_mermaid_block(self):
        # use cases that work
        assert self.md.convert(self.ok__all_attr__markdown_code  ) == self.ok__all_attr__html
        assert self.md.convert(self.ok__no_attr__markdown_code   ) == self.ok__no_attr__html
        assert self.md.convert(self.ok__one_attr__markdown_code  ) == self.ok__one_attr__html
        assert self.md.convert(self.ok__two_attr__markdown_code  ) == self.ok__two_attr__html
        assert self.md.convert(self.ok__misc_order__markdown_code) == self.ok__misc_order__html

        # todo: add support for these use cases which don't work
        assert self.md.convert(self.fail__no_attr__markdown_code ) == ""
        assert self.md.convert(self.fail__one_attr__markdown_code) == ""
        print()

