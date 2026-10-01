"""
This test is for the input validation functions.
"""

import unittest
import re
from e_vals import InvalidValueError, component_check, relationship_check, e_series_selection_check, decade_check


class test_input_validation(unittest.TestCase):

    ### COMPONENT CHECK

    keywords = ['pi','e', 'phi', 'sqrt_2','sqrt_3','Y', 'Z', 'E', 'P', 'T', 
                            'G', 'M', 'k', 'm', 'u', 'n', 'p', 'f', 'a', 'z', 'y' ]
    
    def test_component_invalid_output_str(self):
    # Passes invalid output string
        returnedStr = component_check(component="R1", out="TEST")
        self.assertEqual(returnedStr, "NONE SELECTED")

    def test_component_valid_str(self):
    # Valid component name, string output
        returnedStr = component_check(component="R1", out="str")
        self.assertEqual(returnedStr, "")

    def test_component_valid_err(self):
    # Valid component name, exception
        component_check(component="R1", out="exception")
        pass

    def test_component_first_letter_str(self):
    # First character in component name not a letter, string output
        returnedStr = component_check(component="1R", out="str")
        self.assertEqual(returnedStr, "First character is not a letter.")
    
    def test_component_first_letter_err(self):
    # First character in component name not a letter, exception
        with self.assertRaisesRegex(InvalidValueError, "First character is not a letter."):
            component_check(component="1R", out="exception")

    def test_component_other_symbols_str(self):
    # Non-alphanumeric or underscore characters in component name, string output
        returnedStr = component_check(component="R!", out="str")
        self.assertEqual(returnedStr, "Contains characters other than letters, numbers, or underscore.")

    def test_component_other_symbols_err(self):
    # Non-alphanumeric or underscore characters in component name, exception
        with self.assertRaisesRegex(InvalidValueError, "Contains characters other than letters, numbers, or underscore."):
            component_check(component="R!", out="exception")

    def test_component_keywords_str(self):
    # Keyword as component name, string output
        for keyword in self.keywords:
            with self.subTest(keyword=keyword):
                returnedStr = component_check(component=keyword, out="str")
                self.assertEqual(returnedStr, "Component name cannot be reserved keyword.")

    def test_component_keywords_err(self):
    # Keyword as component name, exception
        for keyword in self.keywords:
            with self.subTest(keyword=keyword):
                with self.assertRaisesRegex(InvalidValueError, "Component name cannot be reserved keyword."):
                    component_check(component=keyword, out="exception")


    ### RELATIONSHIP CHECK

    def test_relationship_invalid_output_str(self):
    # Passes invalid output string
        returnedStr = relationship_check(relationship="3.3 = 5 * (R2 / (R1 + R2))", out="TEST")
        self.assertEqual(returnedStr, "NONE SELECTED")

    def test_relationship_valid_str(self):
    # Valid relationship equation, string output
        returnedStr = relationship_check(relationship="3.3 = 5 * (R2 / (R1 + R2))", out="str")
        self.assertEqual(returnedStr, "")

    def test_relationship_valid_err(self):
    # Valid relationship equation, exception
        relationship_check(relationship="3.3 = 5 * (R2 / (R1 + R2))", out="exception")
        pass

    def test_relationship_no_equal_sign_str(self):
    # Relationship equation without equals sign, string output
        returnedStr = relationship_check(relationship="5 * (R2 / (R1 + R2))", out="str")
        self.assertEqual(returnedStr, "Relationship equation must contain an equals sign.")

    def test_relationship_no_equal_sign_err(self):
        # Relationship equation without equals sign, exception
        with self.assertRaisesRegex(InvalidValueError, re.escape("Relationship equation must contain an equals sign.")):
            relationship_check(relationship="5 * (R2 / (R1 + R2))", out="exception")

    def test_relationship_caret_str(self):
    # Relationship equation uses ^ instead of ** for exponentiation, string output
        returnedStr = relationship_check(relationship="10*k = 1/((2*pi*R1*C1)^(1/2))", out="str")
        self.assertEqual(returnedStr, "Caret cannot be used for exponentiation. Use two asterisks (A**B).")
    
    def test_relationship_caret_err(self):
    # Relationship equation uses ^ instead of ** for exponentiation, exception
        with self.assertRaisesRegex(InvalidValueError, re.escape("Caret cannot be used for exponentiation. Use two asterisks (A**B).")):
            relationship_check(relationship="10*k = 1/((2*pi*R1*C1)^(1/2))", out="exception")
    

    ### E-SERIES SELECTION CHECK

    e_series = [3, 6, 12, 24, 48, 96, 192]
    invalid_series = [-3, 0, 2, '1k', True]

    def test_e_series_selection_invalid_output_str(self):
    # Passes invalid output string
        returnedStr = e_series_selection_check(e_series_selection=24, out="TEST")
        self.assertEqual(returnedStr, "NONE SELECTED")

    def test_e_series_selection_valid_str(self):
    # Valid E-series values, string output
        for e_series_selection in self.e_series:
            with self.subTest(e_series_selection=e_series_selection):
                returnedStr = e_series_selection_check(e_series_selection=e_series_selection, out="str")
                self.assertEqual(returnedStr, "")

    def test_e_series_selection_valid_err(self):
    # Valid E-series values, exception
        for e_series_selection in self.e_series:
            with self.subTest(e_series_selection=e_series_selection):
                e_series_selection_check(e_series_selection=e_series_selection, out="exception")
                pass

    def test_e_series_selection_invalid_str(self):
    # Invalid E-series values, string output
        for value in self.invalid_series:
            with self.subTest(value=value):
                returnedStr = e_series_selection_check(e_series_selection=value, out="str")
                self.assertEqual(returnedStr, "Value must be a valid E-Series number.")
    
    def test_e_series_selection_invalid_err(self):
    # Invalid E-series values, exception
        for value in self.invalid_series:
            with self.subTest(value=value):
                with self.assertRaisesRegex(InvalidValueError, "Value must be a valid E-Series number."):
                    e_series_selection_check(e_series_selection=value, out="exception")
    


    ### DECADE CHECK

    decades = [0.000000000001, 0.00000000001, 0.0000000001, 0.000000001, 0.00000001, 
               0.0000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 
               1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000,
               10000000000, 100000000000, 1000000000000]
    invalid_decades = [0.02, 0.3, 4, 50, 600]

    def test_decade_invalid_output_str(self):
    # Passes invalid output string
        returnedStr = decade_check(decade=100, out="TEST")
        self.assertEqual(returnedStr, "NONE SELECTED")

    def test_decade_check_valid_str(self):
    # Valid decade values, string output
        for decade in self.decades:
            with self.subTest(test_value=decade):
                returnedStr = decade_check(decade=decade, out="str")
                self.assertEqual(returnedStr, "")

    def test_decade_check_valid_err(self):
    # Valid decade values, exception
        for decade in self.decades:
            with self.subTest(test_value=decade):
                decade_check(decade=decade, out="exception")
                pass

    def test_decade_zero_str(self):
    # Decade value of zero, string output
        returnedStr = decade_check(decade=0, out="str")
        self.assertEqual(returnedStr, "Decade cannot be zero.")

    def test_decade_zero_err(self):
    # Decade value of zero, exception
        with self.assertRaisesRegex(InvalidValueError, "Decade cannot be zero."):
            decade_check(decade=0, out="exception")

    def test_decade_negative_str(self):
    # Negative decade value, string output
        returnedStr = decade_check(decade=-1, out="str")
        self.assertEqual(returnedStr, "Decade cannot be negative.")
    
    def test_decade_negative_err(self):
    # Negative decade value, exception
        with self.assertRaisesRegex(InvalidValueError, "Decade cannot be negative."):
            decade_check(decade=-1, out="exception")

    def test_decade_invalid_str(self):
    # Nonnegative and nonzero invalid decade values, string output
        for value in self.invalid_decades:
            with self.subTest(value=value):
                returnedStr = decade_check(decade=value, out="str")
                self.assertEqual(returnedStr, "Value must be a decade expressed a power of 10.")
    
    def test_decade_invalid_err(self):
    # Nonnegative and nonzero invalid decade values, exception
        for value in self.invalid_decades:
            with self.subTest(value=value):
                with self.assertRaisesRegex(InvalidValueError, "Value must be a decade expressed a power of 10."):
                    decade_check(decade=value, out="exception")
    

if __name__ == '__main__':
    unittest.main()
