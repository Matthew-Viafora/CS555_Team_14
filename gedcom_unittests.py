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


    # Tests for US03
    def test_birth_before_marriage(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '1 OCT 1930'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        family = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 1954'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = gedcom_project.birthBeforeMarriage(family, individuals)
        self.assertEqual(result, True)

    def test_marriage_before_birth(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '1 OCT 2000'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        family = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 1954'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = gedcom_project.birthBeforeMarriage(family, individuals)
        self.assertEqual(result, False)

    def test_birth_before_marriage2(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '4 JUL 1954'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        family = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 1954'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = gedcom_project.birthBeforeMarriage(family, individuals)
        self.assertEqual(result, True)

    def test_birth_before_marriage3(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '4 JUL 1954'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        family = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 1860'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = gedcom_project.birthBeforeMarriage(family, individuals)
        self.assertEqual(result, False)

    def test_birth_before_marriage4(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '4 JUL 1954'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        family = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = gedcom_project.birthBeforeMarriage(family, individuals)
        self.assertEqual(result, True)

    # Tests for US04
    def test_death_before_birth2(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '1 OCT 1930'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1900'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        result = gedcom_project.birthBeforeDeath(individuals)
        self.assertEqual(result, False)

    def test_birth_before_death(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'John /Smith/', 'SEX': 'F',
                                'BIRT': {'DATE': '17 OCT 2001'}, 'DEAT': {'DATE': '12 OCT 2099'}, 'FAMC': '@F1@'}}
        result = gedcom_project.birthBeforeDeath(individuals)
        self.assertEqual(result, True)

    def test_birth_before_death2(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'John /Smith/', 'SEX': 'F',
                                'BIRT': {'DATE': '17 OCT 2001'}, 'DEAT': {'DATE': '17 OCT 2001'}, 'FAMC': '@F1@'}}
        result = gedcom_project.birthBeforeDeath(individuals)
        self.assertEqual(result, True)

    def test_birth_before_death3(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'John /Smith/', 'SEX': 'F',
                                'BIRT': {'DATE': '17 OCT 0'}, 'DEAT': {'DATE': '17 OCT 2001'}, 'FAMC': '@F1@'}}
        result = gedcom_project.birthBeforeDeath(individuals)
        self.assertEqual(result, True)

    def test_death_before_birth3(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '1 OCT 20120010'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1900'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        result = gedcom_project.birthBeforeDeath(individuals)
        self.assertEqual(result, False)

    
    def test_recent_birth(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
        'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '4 JUL 1954'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
        '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result=gedcom_project.recent_births(families, individuals)
        self.assertEqual(result,[])

    def test_recent_birth2(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
        'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '2 OCT 2022'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
        '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result=gedcom_project.recent_births(families, individuals)
        self.assertEqual(result,['Bob /Matthews/ (@I5@)'])

    def test_correct_gender(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
        'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '2 OCT 2022'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
        '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result=gedcom_project.correct_gender(families, individuals)
        self.assertEqual(result,['ERROR: INDIVIDUAL: US21: Gender of Husband George /Smith/ (@I2@) in Family @F1@ is female.'])

    def test_correct_gender1(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
        'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '2 OCT 2022'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
        '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result=gedcom_project.correct_gender(families, individuals)
        self.assertEqual(result,[])   
        
   def test_birthBeforeMarriageOfParents(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'John /Smith/', 'SEX': 'F',
                                'BIRT': {'DATE': '17 OCT 2001'}, 'DEAT': {'DATE': '12 OCT 2099'}, 'FAMC': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
        '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = gedcom_project.birthBeforeMarriageOfParents(families, individuals)
        self.assertEqual(result, False)

    def test_birthBeforeMarriageOfParents2(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'John /Smith/', 'SEX': 'F',
                                'BIRT': {'DATE': '17 OCT 2001'}, 'DEAT': {'DATE': '12 OCT 2099'}, 'FAMC': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
        '@I3@'], 'MARR': {'DATE': '4 JUL 1950'}, 'DATE': '6 MAR 2010', 'DIV': {'DATE': '6 MAR 1970'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = gedcom_project.birthBeforeMarriageOfParents(families, individuals)
        self.assertEqual(result, False)

    def test_birthAfterDeathOfParents(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
        'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '4 JUL 1954'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 2010'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 1950'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
        '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 2010', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = gedcom_project.birthAfterDeathOfParents(families, individuals)
        self.assertEqual(result, False)


if __name__ == '__main__':
    unittest.main()
