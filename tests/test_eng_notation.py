"""
This test is for the engineering notation parser and engineering notation string formatter.
"""

import unittest
from e_vals import eng_note, eng_to_float


class test_engineering_notation(unittest.TestCase):
    TEST_FLOAT = 3.1415926535897932384


    ### FLOAT TO ENGINEERING NOTATION
    
    def test_float_to_eng_zero(self):
    # Value of zero
        returnedStr = eng_note(inputValue=0.0, numSigFigs=1)
        self.assertEqual(returnedStr, "0  ")

    def test_float_to_eng_ascii_inf(self):
    # Value of positive infinity, ASCII output
        returnedStr = eng_note(inputValue=float('inf'), numSigFigs=1, encoding="ASCII")
        self.assertEqual(returnedStr, "inf  ")

    def test_float_to_eng_utf8_inf(self):
    # Value of positive infinity, UTF-8 output
        returnedStr = eng_note(inputValue=float('inf'), numSigFigs=1, encoding="UTF-8")
        self.assertEqual(returnedStr, "\u221E  ")

    def test_float_to_eng_ascii_neg_inf(self):
    # Value of negative infinity, ASCII output
        returnedStr = eng_note(inputValue=float('-inf'), numSigFigs=1, encoding="ASCII")
        self.assertEqual(returnedStr, "-inf  ")

    def test_float_to_eng_utf8_neg_inf(self):
    # Value of negative infinity, UTF-8 output
        returnedStr = eng_note(inputValue=float('-inf'), numSigFigs=1, encoding="UTF-8")
        self.assertEqual(returnedStr, "-\u221E  ")

    def test_float_to_eng_sig_figs(self):
    # Number of significant figures
        sig_fig_cases = [
                    (1,  "3  "),
                    (2,  "3.1  "),
                    (3,  "3.14  "),
                    (4,  "3.142  "),
                    (5,  "3.1416  "),
                    (6,  "3.14159  "),
                    (7,  "3.141593  "),
                    (8,  "3.1415927  "),
                    (9,  "3.14159265  "),
                    (10, "3.141592654  "),
                    (11, "3.1415926536  "),
                    (12, "3.14159265359  "),
                    (13, "3.141592653590  "),
                    (14, "3.1415926535898  "),
                    (15, "3.14159265358979  "),
                    (16, "3.141592653589793  ")]
        for sig_fig, expected in sig_fig_cases:
            with self.subTest(sig_fig=sig_fig):
                returnedStr = eng_note(inputValue=self.TEST_FLOAT, numSigFigs=sig_fig)
                self.assertEqual(returnedStr, expected)

    def test_float_to_eng_ascii_prefixes(self):
    # Engineering notation prefixes, ASCII output
        prefixes_cases = [
                (self.TEST_FLOAT*10**-25, "3.1416e-25  "),
                (self.TEST_FLOAT*10**-24, "3.1416 y"),
                (self.TEST_FLOAT*10**-23, "31.416 y"),
                (self.TEST_FLOAT*10**-22, "314.16 y"),
                (self.TEST_FLOAT*10**-21, "3.1416 z"),
                (self.TEST_FLOAT*10**-20, "31.416 z"),
                (self.TEST_FLOAT*10**-19, "314.16 z"),
                (self.TEST_FLOAT*10**-18, "3.1416 a"),
                (self.TEST_FLOAT*10**-17, "31.416 a"),
                (self.TEST_FLOAT*10**-16, "314.16 a"),
                (self.TEST_FLOAT*10**-15, "3.1416 f"),
                (self.TEST_FLOAT*10**-14, "31.416 f"),
                (self.TEST_FLOAT*10**-13, "314.16 f"),
                (self.TEST_FLOAT*10**-12, "3.1416 p"),
                (self.TEST_FLOAT*10**-11, "31.416 p"),
                (self.TEST_FLOAT*10**-10, "314.16 p"),
                (self.TEST_FLOAT*10**-9,  "3.1416 n"),
                (self.TEST_FLOAT*10**-8,  "31.416 n"),
                (self.TEST_FLOAT*10**-7,  "314.16 n"),
                (self.TEST_FLOAT*10**-6,  "3.1416 u"),
                (self.TEST_FLOAT*10**-5,  "31.416 u"),
                (self.TEST_FLOAT*10**-4,  "314.16 u"),
                (self.TEST_FLOAT*10**-3,  "3.1416 m"),
                (self.TEST_FLOAT*10**-2,  "31.416 m"),
                (self.TEST_FLOAT*10**-1,  "314.16 m"),
                (self.TEST_FLOAT*10**0,   "3.1416  "),
                (self.TEST_FLOAT*10**1,   "31.416  "),
                (self.TEST_FLOAT*10**2,   "314.16  "),
                (self.TEST_FLOAT*10**3,   "3.1416 k"),
                (self.TEST_FLOAT*10**4,   "31.416 k"),
                (self.TEST_FLOAT*10**5,   "314.16 k"),
                (self.TEST_FLOAT*10**6,   "3.1416 M"),
                (self.TEST_FLOAT*10**7,   "31.416 M"),
                (self.TEST_FLOAT*10**8,   "314.16 M"),
                (self.TEST_FLOAT*10**9,   "3.1416 G"),
                (self.TEST_FLOAT*10**10,  "31.416 G"),
                (self.TEST_FLOAT*10**11,  "314.16 G"),
                (self.TEST_FLOAT*10**12,  "3.1416 T"),
                (self.TEST_FLOAT*10**13,  "31.416 T"),
                (self.TEST_FLOAT*10**14,  "314.16 T"),
                (self.TEST_FLOAT*10**15,  "3.1416 P"),
                (self.TEST_FLOAT*10**16,  "31.416 P"),
                (self.TEST_FLOAT*10**17,  "314.16 P"),
                (self.TEST_FLOAT*10**18,  "3.1416 E"),
                (self.TEST_FLOAT*10**19,  "31.416 E"),
                (self.TEST_FLOAT*10**20,  "314.16 E"),
                (self.TEST_FLOAT*10**21,  "3.1416 Z"),
                (self.TEST_FLOAT*10**22,  "31.416 Z"),
                (self.TEST_FLOAT*10**23,  "314.16 Z"),
                (self.TEST_FLOAT*10**24,  "3.1416 Y"),
                (self.TEST_FLOAT*10**25,  "31.416 Y"),
                (self.TEST_FLOAT*10**26,  "314.16 Y"),
                (self.TEST_FLOAT*10**27,  "3.1416e+27  ")]
        
        for test_value, expected in prefixes_cases:
            with self.subTest(test_value=test_value):
                returnedStr = eng_note(inputValue=test_value, numSigFigs=5, encoding="ASCII")
                self.assertEqual(returnedStr, expected)

    def test_float_to_eng_utf8_prefixes(self):
    # Engineering notation prefixes, UTF-8 output
        prefixes_cases = [
                (self.TEST_FLOAT*10**-6,  "3.1416 \u03BC"),
                (self.TEST_FLOAT*10**-5,  "31.416 \u03BC"),
                (self.TEST_FLOAT*10**-4,  "314.16 \u03BC")]
        
        for test_value, expected in prefixes_cases:
            with self.subTest(test_value=test_value):
                returnedStr = eng_note(inputValue=test_value, numSigFigs=5, encoding="UTF-8")
                self.assertEqual(returnedStr, expected)


    ### ENGINEERING NOTATION TO FLOAT

    def test_eng_to_float_zero(self):
    # Value of zero
        returnedFloat = eng_to_float(inputStr="0")
        self.assertEqual(returnedFloat, 0)

    def test_eng_to_float_ascii_inf(self):
    # Value of positive infinity, ASCII input
        returnedFloat = eng_to_float(inputStr="inf")
        self.assertEqual(returnedFloat, float("inf"))

    def test_eng_to_float_utf8_inf(self):
    # Value of positive infinity, UTF-8 input
        returnedFloat = eng_to_float(inputStr="\u221E")
        self.assertEqual(returnedFloat, float("inf"))

    def test_eng_to_float_ascii_neg_inf(self):
    # Value of negative infinity, ASCII input
        returnedFloat = eng_to_float(inputStr="-inf")
        self.assertEqual(returnedFloat, float("-inf"))

    def test_eng_to_float_utf8_neg_inf(self):
    # Value of negative infinity, UTF-8 input
        returnedFloat = eng_to_float(inputStr="-\u221E")
        self.assertEqual(returnedFloat, float("-inf"))

    def test_eng_to_float_ascii_prefixes(self):
    # Engineering notation prefixes, ASCII input
        value_cases = [
                ("3.1416e-25  ", 3.1416e-25),
                ("3.1416 y", 3.1416e-24),
                ("31.416 y", 3.1416e-23),
                ("314.16 y", 3.1416e-22),
                ("3.1416 z", 3.1416e-21),
                ("31.416 z", 3.1416e-20),
                ("314.16 z", 3.1416e-19),
                ("3.1416 a", 3.1416e-18),
                ("31.416 a", 3.1416e-17),
                ("314.16 a", 3.1416e-16),
                ("3.1416 f", 3.1416e-15),
                ("31.416 f", 3.1416e-14),
                ("314.16 f", 3.1416e-13),
                ("3.1416 p", 3.1416e-12),
                ("31.416 p", 3.1416e-11),
                ("314.16 p", 3.1416e-10),
                ("3.1416 n", 3.1416e-9),
                ("31.416 n", 3.1416e-8),
                ("314.16 n", 3.1416e-7),
                ("3.1416 u", 3.1416e-6),
                ("31.416 u", 3.1416e-5),
                ("314.16 u", 3.1416e-4),
                ("3.1416 m", 3.1416e-3),
                ("31.416 m", 3.1416e-2),
                ("314.16 m", 3.1416e-1),
                ("3.1416  ", 3.1416e0),
                ("31.416  ", 3.1416e1),
                ("314.16  ", 3.1416e2),
                ("3.1416 k", 3.1416e3),
                ("31.416 k", 3.1416e4),
                ("314.16 k", 3.1416e5),
                ("3.1416 M", 3.1416e6),
                ("31.416 M", 3.1416e7),
                ("314.16 M", 3.1416e8),
                ("3.1416 G", 3.1416e9),
                ("31.416 G", 3.1416e10),
                ("314.16 G", 3.1416e11),
                ("3.1416 T", 3.1416e12),
                ("31.416 T", 3.1416e13),
                ("314.16 T", 3.1416e14),
                ("3.1416 P", 3.1416e15),
                ("31.416 P", 3.1416e16),
                ("314.16 P", 3.1416e17),
                ("3.1416 E", 3.1416e18),
                ("31.416 E", 3.1416e19),
                ("314.16 E", 3.1416e20),
                ("3.1416 Z", 3.1416e21),
                ("31.416 Z", 3.1416e22),
                ("314.16 Z", 3.1416e23),
                ("3.1416 Y", 3.1416e24),
                ("31.416 Y", 3.1416e25),
                ("314.16 Y", 3.1416e26),
                ("3.1416e+27  ", 3.1416e+27)]
        
        for test_value, expected in value_cases:
            with self.subTest(test_value=test_value):
                returnedFloat = eng_to_float(inputStr=test_value)
                self.assertEqual(returnedFloat, expected)

    def test_eng_to_float_utf8_prefixes(self):
    # Engineering notation prefixes, UTF-8 input
        returnedFloat = eng_to_float(inputStr="3.1416 \u03BC")
        self.assertEqual(returnedFloat, 3.1416e-6)

    def test_eng_to_float_invalid_string(self):
    # Invalid string input
        with self.assertRaisesRegex(ValueError, "invalid"):
            eng_to_float(inputStr="3.1416 x")

if __name__ == '__main__':
    unittest.main()
