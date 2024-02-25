import unittest

import smact
from smact.dopant_prediction import doper
from smact.structure_prediction import utilities


class dopant_prediction_test(unittest.TestCase):
    def test_dopant_prediction(self):
        num_dopants = 10
        test_specie = ("Cu1+", "Ga3+", "S2-")
        test = doper.Doper(test_specie)

        # Assert: Length of the list and return type (dictionary: list)
        self.assertIs(type(test.get_dopants()), dict)
        for ls in test.get_dopants().values():
            self.assertIs(type(ls), list)

        # Assert: (cation) higher charges for n-type and lower charges for p-type
        n_sub_list_cat = test.get_dopants().get("n-type cation substitutions")
        p_sub_list_cat = test.get_dopants().get("p-type cation substitutions")
        n_sub_list_an = test.get_dopants().get("n-type anion substitutions")
        p_sub_list_an = test.get_dopants().get("p-type anion substitutions")
        for n_atom, p_atom in zip(n_sub_list_cat, p_sub_list_cat):
            self.assertGreater(
                utilities.parse_spec(n_atom[0])[1],
                utilities.parse_spec(n_atom[1])[1],
            )
            self.assertLess(
                utilities.parse_spec(p_atom[0])[1],
                utilities.parse_spec(p_atom[1])[1],
            )

        for n_atom, p_atom in zip(n_sub_list_an, p_sub_list_an):
            self.assertGreater(
                utilities.parse_spec(n_atom[0])[1],
                utilities.parse_spec(n_atom[1])[1],
            )
            self.assertLess(
                utilities.parse_spec(p_atom[0])[1],
                utilities.parse_spec(p_atom[1])[1],
            )


if __name__ == "__main__":
    TestLoader = unittest.TestLoader()
    DoperTests = unittest.TestSuite()
    DoperTests.addTests(
        TestLoader.loadTestsFromTestCase(dopant_prediction_test)
    )

    runner = unittest.TextTestRunner()
    result = runner.run(DoperTests)
