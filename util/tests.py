from django.test import TestCase
from util.strutils import TemplateString

from util.atomics import AtomicVar

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

import math


class AtomicVarTestCase(TestCase):
    def setUp(self):
        self.atomic_x = AtomicVar(10)
        self.atomic_y = AtomicVar(1/math.e)
        self.atomic_str = AtomicVar('Hello World!')
        self.atomic_atomic = AtomicVar(AtomicVar(0))

    def test_instantiation(self):

        a1 = self.atomic_x.value
        a2 = self.atomic_y.value
        a3 = self.atomic_str.value
        a4 = self.atomic_atomic.value

        self.assertEqual(a1, 10)
        self.assertEqual(a2, 1/math.e)
        self.assertEqual(a3, 'Hello World!')
        self.assertEqual(a4, AtomicVar(0))

    def test_atomic_on_atomic_operations(self):
        r1 = self.atomic_x + self.atomic_y
        r2 = self.atomic_y - self.atomic_y
        r3 = self.atomic_x / self.atomic_y
        r4 = self.atomic_y // self.atomic_x
        r5 = self.atomic_x * self.atomic_x
        r6 = self.atomic_y ** AtomicVar(-1)

        self.assertEqual(r1, AtomicVar(10 + 1/math.e))
        self.assertEqual(r2, AtomicVar(0))
        self.assertEqual(r3, AtomicVar(10*math.e))
        self.assertEqual(r4, AtomicVar((1/math.e) // 10))
        self.assertEqual(r5, AtomicVar(10*10))
        self.assertEqual(r6, AtomicVar((1/math.e) ** -1))
        self.assertLess(r5, 10**5)

        r5 += r5
        self.assertEqual(r5, AtomicVar(200))

    def test_atomic_on_non_atomic_operations(self):
        r1 = self.atomic_str + ' How are you?'
        r2 = self.atomic_x - 5
        r3 = self.atomic_x / 6
        r4 = self.atomic_x // 1000
        r5 = self.atomic_y * math.e
        r6 = self.atomic_y ** -1

        self.assertEqual(r1, "Hello World! How are you?")
        self.assertEqual(r2, 5)
        self.assertEqual(r3, 10/6)
        self.assertEqual(r4, 0)
        self.assertEqual(r5, 1)
        self.assertEqual(r6, math.e)
        self.assertLess(r4, 1)

        r3 += 335*math.e ** 2
        self.assertEqual(r3, (10/6) + (335*math.e ** 2))
