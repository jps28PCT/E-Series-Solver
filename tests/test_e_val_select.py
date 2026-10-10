"""
This test is for the main solver engine. It may take a while to fully run.

When writing tests, all intended test outputs must be coprime ( LCM = 1 ) to ensure only one valid solution set.
Use exclusive values from particular E-series to ensure tests match expected results.
e_val_select() is not to be used to calculate the outputs to test against.
"""

import unittest
from e_series_solver import e_val_select


class test_e_val_select(unittest.TestCase):

    ### ERROR TESTS
    # I have been unable to trigger all exceptions in e_val_select(). However, I am keeping them just in case something eventually triggers it.
    # If a prevously unraised exception gets raised, that will be analyzed and potentially used for its unittest.

    def test_no_component_names(self):
    # Tests case in which no component names have been passed.
        components = " "
        relationships = [ "3.3 = 5 * R2/(R1+R2)",  "5 / (R1+R2) = 0.01"]
        e_series_selection = (24, 24)
        decade_selection = (100, 1000)
        with self.assertRaisesRegex(ValueError, "No Components were passed. Unable to continue."):
            e_val_select(components=components, relationships=relationships, e_series_selection=e_series_selection, decade_selection=decade_selection)

    def test_too_few_e_series_selections(self):
    # Tests case in which there are less E-series selections than components.
        components = "R1 R2"
        relationships = [ "3.3 = 5 * R2/(R1+R2)",  "5 / (R1+R2) = 0.01"]
        e_series_selection = (24,)
        decade_selection = (100, 1000)
        with self.assertRaisesRegex(ValueError, "Too few E-Series selections were passed. There must be one E-Series selection per component."):
            e_val_select(components=components, relationships=relationships, e_series_selection=e_series_selection, decade_selection=decade_selection)
    
    def test_too_many_e_series_selections(self):
    # Tests case in which there are more E-series selections than components.
        components = "R1 R2"
        relationships = [ "3.3 = 5 * R2/(R1+R2)",  "5 / (R1+R2) = 0.01"]
        e_series_selection = (24, 24, 24)
        decade_selection = (100, 1000)
        with self.assertRaisesRegex(ValueError, "Too many E-Series selections were passed. There must be one E-Series selection per component."):
            e_val_select(components=components, relationships=relationships, e_series_selection=e_series_selection, decade_selection=decade_selection)

    def test_too_few_decade_selections(self):
    # Tests case in which there are less decade selections than components.
        components = "R1 R2"
        relationships = [ "3.3 = 5 * R2/(R1+R2)",  "5 / (R1+R2) = 0.01"]
        e_series_selection = (24, 24)
        decade_selection = (100,)
        with self.assertRaisesRegex(ValueError, "Too few decade selections were passed. There must be one decade selection per component."):
            e_val_select(components=components, relationships=relationships, e_series_selection=e_series_selection, decade_selection=decade_selection)
    
    def test_too_many_decade_selections(self):
    # Tests case in which there are more decade selections than components.
        components = "R1 R2"
        relationships = [ "3.3 = 5 * R2/(R1+R2)",  "5 / (R1+R2) = 0.01"]
        e_series_selection = (24, 24)
        decade_selection = (100, 1000, 10000)
        with self.assertRaisesRegex(ValueError, "Too many decade selections were passed. There must be one decade selection per component."):
            e_val_select(components=components, relationships=relationships, e_series_selection=e_series_selection, decade_selection=decade_selection)

    def test_invalid_e_series_selection(self):
    # Tests case where an invalid E-Series number is passed as part of the E-Series selection
        components = "R1"
        relationships = [
            "1000 = R1",
        ]
        e_series_selection = (
            10,
        )
        decade_selection = (
            1000,
        )

        with self.assertRaisesRegex(ValueError, "'10' is not a valid E-Series number."):
            e_val_select(components=components, relationships=relationships, e_series_selection=e_series_selection, decade_selection=decade_selection)
    

    def test_cannot_solve(self):
    # All cases which would result in imaginary, negative, or zero component values should be caught by this test.
    # This is because of the "positive=True" declaration in the sp.solve() calls in e_val_select()
        components = "R1"
        relationships = [
            "0 = R1",
        ]
        e_series_selection = (
            192,
        )
        decade_selection = (
            1000,
        )

        with self.assertRaisesRegex(ValueError, "The system of component relationship equations cannot be solved."):
            e_val_select(components=components, relationships=relationships, e_series_selection=e_series_selection, decade_selection=decade_selection)

    def test_fully_determined_infinity(self):
    # Tests if infinite component value is caught and handled in fully determined case.
        components = "R1"
        relationships = [
            "R1 = 99*10**9999",
        ]
        e_series_selection = (
            192,
        )
        decade_selection = (
            1000,
        )

        with self.assertRaisesRegex(ValueError, "Infinite component value detected. No real solution."):
            e_val_select(components=components, relationships=relationships, e_series_selection=e_series_selection, decade_selection=decade_selection)

    def test_underdetermined_infinity(self):
    # Tests if infinite component value is caught and handled in underdetermined case.
        components = "R1 R2"
        relationships = [
            "R1 * R2 = 99*10**9999",
        ]
        e_series_selection = (
            192,
            192
        )
        decade_selection = (
            1000,
            1000
        )

        with self.assertRaisesRegex(ValueError, "Component value that approached infinity detected. Unable to solve."):
            e_val_select(components=components, relationships=relationships, e_series_selection=e_series_selection, decade_selection=decade_selection)
    

    ### ROUNDING TESTS

    def test_round_up(self):
    # Tests if component value can be rounded up.
    # Value given in equation is exactly 3% below target value.
        components = "R1"
        relationships = [ "R1 = 970"]
        e_series_selection = (24,)
        decade_selection = (1000,)

        test_solution = (
            (0, 1000),      # Check component value (index 0) equals 1k
            (1, 0.03)       # Check error value (index 1) equals 0.03
        )

        solution = e_val_select(components=components, relationships=relationships, e_series_selection=e_series_selection, decade_selection=decade_selection)
        with self.subTest(solution=solution, test_solution=test_solution):
                    for item in test_solution:
                        self.assertAlmostEqual(solution["R1"][item[0]], item[1], 2)

    def test_round_down(self):
    # Tests if component value can be rounded down.
    # Value given in equation is exactly 3% above target value.
        components = "R1"
        relationships = [ "R1 = 1030"]
        e_series_selection = (24,)
        decade_selection = (1000,)

        test_solution = (
            (0, 1000),      # Check component value (index 0) equals 1k
            (1, 0.03)       # Check error value (index 1) equals 0.03
        )

        solution = e_val_select(components=components, relationships=relationships, e_series_selection=e_series_selection, decade_selection=decade_selection)
        with self.subTest(solution=solution, test_solution=test_solution):
                    for item in test_solution:
                        self.assertAlmostEqual(solution["R1"][item[0]], item[1], 2)

    def test_rounding_to_selected_e_series(self):
    # Tests if values are rounded to desired E-Series.
    # Each test value is not available in any lower E-Series lists.
        components = "R3 R6 R12 R24 R48 R96 R192"
        relationships = [
            "R3 = 2.2",
            "R6 = 1.5",
            "R12 = 3.9",
            "R24 = 5.1",
            "R48 = 2.49",
            "R96 = 2.43",
            "R192 = 2.46",
        ]
        e_series_selection = (
            3,
            6,
            12,
            24,
            48,
            96,
            192
        )
        decade_selection = (1, 1, 1, 1, 1, 1, 1)
        test_solution = {"R3":(2.2, 0.0), 
                         "R6":(1.5, 0.0),
                         "R12":(3.9, 0.0),
                         "R24":(5.1, 0.0),
                         "R48":(2.49, 0.0),
                         "R96":(2.43, 0.0),
                         "R192":(2.46, 0.0)}

        solution = e_val_select(components=components, relationships=relationships, e_series_selection=e_series_selection, decade_selection=decade_selection)
        with self.subTest(solution=solution, test_solution=test_solution):
            for key in test_solution:
                self.assertEqual(solution[key][0], test_solution[key][0])           # Check component values match exactly


    ### VALUE TESTS
    # All error is ignored during these checks, so error is set to 0.0 in test_solution

    def test_fully_determined(self):
    # Tests fully determined case - series-parallel resistor circuit
        components = "R1 R2 R3"
        relationships = [
            "2879 = 1/((1/R2) + (1/R3))",   # Adding R2 and R3 in parallel
            "3699 = R1 + 2879",             # Adding R1 in series with R2||R3
            "0.001 = 11 / R2"               # Current through R2 when applying 11V across it
        ]
        e_series_selection = (
            24,                 # R1
            24,                 # R2
            24                  # R3
        )
        decade_selection = (
            100,                # R1
            10000,              # R2
            1000                # R3
        )
        test_solution = {"R1":(820, 0.0), "R2":(11000, 0.0), "R3":(3900, 0.0)}

        solution = e_val_select(components=components, relationships=relationships, e_series_selection=e_series_selection, decade_selection=decade_selection)
        with self.subTest(solution=solution, test_solution=test_solution):
            for key in test_solution:
                self.assertEqual(solution[key][0], test_solution[key][0])           # Check component values match exactly


    def test_underdetermined_by_one(self):
    # Tests system that is underdetermined by one - LC oscillator
        components = "L1 C1"
        relationships = [
            "67016 = 1 / (2*3.14159265358979323846264338327950*sqrt(L1*C1))"    # LC resonant frequency
        ]
        e_series_selection = (
            12,                 # L1
            6                   # C1
        )
        decade_selection = (
            0.00001,            # L1
            0.0000001           # C1
        )
        test_solution = {"L1":(0.000012, 0.0), "C1":(0.00000047, 0.0)}

        solution = e_val_select(components=components, relationships=relationships, e_series_selection=e_series_selection, decade_selection=decade_selection)
        with self.subTest(solution=solution, test_solution=test_solution):
            for key in test_solution:
                self.assertEqual(solution[key][0], test_solution[key][0])           # Check component values match exactly

    def test_fully_underdetermined(self):
    # Tests system that is underdetermined - series resistor circuit
        components = "R1 R2 R3"
        relationships = [
            "1520 = R1 + R2 + R3"    # LC resonant frequency
        ]
        e_series_selection = (
            24,                 # R1
            12,                 # R2
            6                   # R3
        )
        decade_selection = (
            100,                # R1
            100,                # R2
            100                 # R3
        )
        test_solution = {"R1":(910, 0.0), "R2":(390, 0.0), "R3":(220, 0.0)}

        solution = e_val_select(components=components, relationships=relationships, e_series_selection=e_series_selection, decade_selection=decade_selection)
        with self.subTest(solution=solution, test_solution=test_solution):
            for key in test_solution:
                self.assertEqual(solution[key][0], test_solution[key][0])           # Check component values match exactly

if __name__ == '__main__':
    unittest.main()