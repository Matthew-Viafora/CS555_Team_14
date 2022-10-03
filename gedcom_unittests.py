import unittest
import gedcom_project
from datetime import date

class TestGedcom(unittest.TestCase):

    #Tests for US27 - Age
    def test_age_alive(self):
        test_individual ={ "BIRT": {"DATE": "27 OCT 2000"} }                
        result = gedcom_project.calculateAge(test_individual)
        self.assertEqual(result, gedcom_project.timespan(test_individual["BIRT"]["DATE"], date.today()))
    def test_age_alive2(self):
        test_individual ={ "BIRT": {"DATE": "1 OCT 2022"} }                
        result = gedcom_project.calculateAge(test_individual)
        self.assertEqual(result, gedcom_project.timespan(test_individual["BIRT"]["DATE"], date.today()))
    def test_age_alive3(self):
        test_individual ={ "BIRT": {"DATE": "1 OCT 2021"} }                
        result = gedcom_project.calculateAge(test_individual)
        self.assertGreaterEqual(result, 1)
    def test_age_deceased(self):
        test_individual ={ "BIRT": {"DATE": "27 OCT 2000"}, "DEAT": {"DATE": "10 JAN 2021"} }                
        result = gedcom_project.calculateAge(test_individual)
        self.assertEqual(result, 20)
    def test_age_deceased2(self):
        test_individual ={ "BIRT": {"DATE": "27 OCT 2000"}, "DEAT": {"DATE": "10 JAN 2001"} }                
        result = gedcom_project.calculateAge(test_individual)
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()