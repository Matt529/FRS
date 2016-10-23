from django.test import TestCase
from util.templatestring import TemplateString

class TemplateStringsTestCase(TestCase):

    def setUp(self):

        self.HELLO = TemplateString("Hello ${noun}!")
        self.BLESS_THIS = TemplateString("Bless this ${noun}. It's ${happy_word}.")
        self.DOLLAR_BILLS = TemplateString("I got them $ $$ ya'll! Actually, more like $${amount}... Yeah.")

    def test_cleaning(self):
        self.assertEqual(self.DOLLAR_BILLS._format_string, "I got them $$ $$$$ ya'll! Actually, more like $$${amount}... Yeah.")

    def test_basic_format(self):
        noun_var = "World"
        hello_result = self.HELLO.format(noun=noun_var)
        hello_applied = self.HELLO(noun=noun_var)

        bless_result = self.BLESS_THIS(noun="Horrific Mess", happy_word="grrrrreat")
        dollar_result = self.DOLLAR_BILLS(amount="1.50")

        self.assertIsInstance(hello_result, str)
        self.assertIsInstance(hello_applied, str)

        self.assertEqual(hello_result, "Hello " + noun_var + "!")
        self.assertEqual(hello_result, hello_applied)
        self.assertEqual(bless_result, "Bless this Horrific Mess. It's grrrrreat.")
        self.assertEqual(dollar_result, "I got them $ $$ ya'll! Actually, more like $1.50... Yeah.")

