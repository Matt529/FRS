from django.test import TestCase
from util.templatestring import TemplateString


class TemplateStringsTestCase(TestCase):

    def setUp(self):
        self.HELLO = TemplateString("Hello {noun}!")
        self.BLESS_THIS = TemplateString("Bless this {noun}. It's {happy_word}.")
        self.DOLLAR_BILLS = TemplateString("I got them $ $$ ya'll! Actually, more like ${amount}... Yeah.")

    def test_cleaning(self):
        """
        Assert that the format string is stored successfully.
        """

        self.assertEqual(self.DOLLAR_BILLS._format_string,
                         "I got them $ $$ ya'll! Actually, more like ${amount}... Yeah.")

    def test_format(self):
        """
        Assert that formatting works both using the TemplateString#format method and using TemplateString as a function
        itself. These both must return strings and must yield the same results.
        """

        # Setup both .format and __call__ results for comparison
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

    def test_template_add(self):
        """
        Tests that adding two TemplateStrings together yields the correct TemplateString and the correct format results.
         The possible result strings should realistically be all possible concatenations of all possible format strings
         from the first and second TemplateStrings.
        """
        hello_and_bless = self.HELLO + self.BLESS_THIS
        hello_and_dollars = self.HELLO + self.DOLLAR_BILLS

        self.assertIsInstance(hello_and_bless, TemplateString)
        self.assertEqual(self.HELLO._format_string + self.BLESS_THIS._format_string, hello_and_bless._format_string)

        hb_result = hello_and_bless(noun="World", happy_word="awful")
        hd_result = hello_and_dollars(noun="Guys", amount=1500.35)

        self.assertEqual(hb_result, "Hello World!Bless this World. It's awful.")
        self.assertEqual(hd_result, "Hello Guys!I got them $ $$ ya'll! Actually, more like $1500.35... Yeah.")

    def test_string_add(self):
        """
        Tests that adding a TemplateString and normal python string works properly. Both __add__ and __radd__. The
        string added can also contain format specifiers like {} and {identifier:modifiers}, these will also be part of
        formatting.
        """
        hello_and_gimme = self.HELLO + " Gimme that sweet sweet {}!"
        sometimes_and_bless = "Sometimes, I look at this codebase and... well, it makes me {:.2%} sad. " + self.BLESS_THIS

        self.assertIsInstance(hello_and_gimme, TemplateString)
        self.assertIsInstance(sometimes_and_bless, TemplateString)
        self.assertEqual(self.HELLO._format_string + " Gimme that sweet sweet {}!", hello_and_gimme._format_string)

        hg_result = hello_and_gimme("soda pop", noun="World")
        from math import e
        sb_result = sometimes_and_bless(1/e, noun="code", happy_word="an absolute dream")

        self.assertEqual(hg_result, "Hello World! Gimme that sweet sweet soda pop!")
        self.assertEqual(sb_result, "Sometimes, I look at this codebase and... well, it makes me %.2f%% sad. Bless this code. It's an absolute dream." % (100/e))
