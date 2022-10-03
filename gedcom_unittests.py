import unittest
import gedcom_project

class TestGedcom(unittest.TestCase):

    #Tests for US27 - Age
    def test_age_alive(self):
        test_individual ={ "BIRT": {"DATE": "27 OCT 2000"} }                
        result = gedcom_project.calculateAge(test_individual)
        self.assertEqual(result, 21)
    def test_age_deceased(self):
        test_individual ={ "BIRT": {"DATE": "27 OCT 2000"}, "DEAT": {"DATE": "10 JAN 2021"} }                
        result = gedcom_project.calculateAge(test_individual)
        self.assertEqual(result, 20)

if __name__ == '__main__':
    unittest.main()