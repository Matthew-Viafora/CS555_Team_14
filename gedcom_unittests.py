import unittest
import gedcom_project
from datetime import date
from datetime import timedelta

today = date.today()


class TestGedcom(unittest.TestCase):

    # Tests for US27 - Age
    def test_age_alive(self):
        test_individual = {"BIRT": {"DATE": "27 OCT 2000"}}
        result = gedcom_project.calculateAge(test_individual)
        self.assertEqual(result, gedcom_project.timespan(
            test_individual["BIRT"]["DATE"], date.today()))

    def test_age_alive2(self):
        test_individual = {"BIRT": {"DATE": "1 OCT 2022"}}
        result = gedcom_project.calculateAge(test_individual)
        self.assertEqual(result, gedcom_project.timespan(
            test_individual["BIRT"]["DATE"], date.today()))

    def test_age_alive3(self):
        test_individual = {"BIRT": {"DATE": "1 OCT 2021"}}
        result = gedcom_project.calculateAge(test_individual)
        self.assertGreaterEqual(result, 1)

    def test_age_deceased(self):
        test_individual = {"BIRT": {"DATE": "27 OCT 2000"},
                           "DEAT": {"DATE": "10 JAN 2021"}}
        result = gedcom_project.calculateAge(test_individual)
        self.assertEqual(result, 20)

    def test_age_deceased2(self):
        test_individual = {"BIRT": {"DATE": "27 OCT 2000"},
                           "DEAT": {"DATE": "10 JAN 2001"}}
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
        self.assertEqual(result, False)

    # Tests for US04
    def test_death_before_birth1(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '1 OCT 1930'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1900'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        result = gedcom_project.birthBeforeDeath(individuals)
        self.assertEqual(result, True)

    def test_birth_before_death2(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'John /Smith/', 'SEX': 'F',
                                'BIRT': {'DATE': '17 OCT 2001'}, 'DEAT': {'DATE': '12 OCT 2099'}, 'FAMC': '@F1@'}}
        result = gedcom_project.birthBeforeDeath(individuals)
        self.assertEqual(result, True)

    def test_birth_before_death3(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'John /Smith/', 'SEX': 'F',
                                'BIRT': {'DATE': '17 OCT 2001'}, 'DEAT': {'DATE': '17 OCT 2001'}, 'FAMC': '@F1@'}}
        result = gedcom_project.birthBeforeDeath(individuals)
        self.assertEqual(result, True)

    def test_birth_before_death4(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'John /Smith/', 'SEX': 'F',
                                'BIRT': {'DATE': '17 OCT 0'}, 'DEAT': {'DATE': '17 OCT 2001'}, 'FAMC': '@F1@'}}
        result = gedcom_project.birthBeforeDeath(individuals)
        self.assertEqual(result, True)

    def test_death_before_birth5(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '1 OCT 20120010'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1900'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        result = gedcom_project.birthBeforeDeath(individuals)
        self.assertEqual(result, True)

    def test_recent_birth1(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '4 JUL 1954'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = gedcom_project.recent_births(individuals)
        self.assertEqual(result, [])

    def test_recent_birth2(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '2 OCT 2022'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        individuals["@I5@"]["BIRT"]["DATE"] = f'{(today).strftime("%d")} {list(gedcom_project.months.keys())[int(today.strftime("%m"))-1]} {today.strftime("%Y")}'
        result = gedcom_project.recent_births(individuals)
        self.assertEqual(result, ['Bob /Matthews/ (@I5@)'])

    def test_correct_gender1(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '2 OCT 2022'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = gedcom_project.correct_gender(families, individuals)
        self.assertEqual(result, [
                         'ERROR: INDIVIDUAL: US21: Gender of Husband George /Smith/ (@I2@) in Family @F1@ is female.'])

    def test_correct_gender2(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '2 OCT 2022'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = gedcom_project.correct_gender(families, individuals)
        self.assertEqual(result, [])

    def test_birthBeforeMarriageOfParents(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '2 OCT 2022'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = [gedcom_project.birthBeforeMarriageOfParents(
            f, individuals) for f in families.values()]
        self.assertEqual(result, [False, True, False])

    def test_birthBeforeMarriageOfParents2(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 1985'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '2 OCT 2022'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = [gedcom_project.birthBeforeMarriageOfParents(
            f, individuals) for f in families.values()]
        self.assertEqual(result, [True, True, False])

    def test_birthBeforeMarriageOfParents3(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 1985'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '2 OCT 2022'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1969'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = [gedcom_project.birthBeforeMarriageOfParents(
            f, individuals) for f in families.values()]
        self.assertEqual(result, [True, True, True])

    def test_birthAfterDeathOfParents(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '2 OCT 2022'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 2010', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = [gedcom_project.birthAfterDeathOfParents(
            f, individuals) for f in families.values()]
        self.assertEqual(result, [False, False, False])

    def test_birthAfterDeathOfParents2(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '15 OCT 2021'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '2 OCT 2022'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 2010', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = [gedcom_project.birthAfterDeathOfParents(
            f, individuals) for f in families.values()]
        self.assertEqual(result, [False, True, False])

    def test_recent_death(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '4 JUL 1954'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '8 OCT 2022'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}

        individuals["@I7@"]["DEAT"]["DATE"] = f'{(today).strftime("%d")} {list(gedcom_project.months.keys())[int(today.strftime("%m"))-1]} {today.strftime("%Y")}'

        result = gedcom_project.recent_deaths(individuals)
        self.assertEqual(result, ['Jimothy /Domingo/ (@I7@)'])

    def test_recent_death1(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '4 JUL 1954'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '19 SEP 2022'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '8 OCT 2022'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}

        individuals["@I7@"]["DEAT"]["DATE"] = f'{(today).strftime("%d")} {list(gedcom_project.months.keys())[int(today.strftime("%m"))-1]} {today.strftime("%Y")}'

        result = gedcom_project.recent_deaths(individuals)
        self.assertEqual(result, ['Jimothy /Domingo/ (@I7@)'])

    def test_upcoming_birthdays(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '2 OCT 2022'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '10 MAY 1969'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '16 APR 2015'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}

        individuals["@I3@"]["BIRT"]["DATE"] = f'{(today).strftime("%d")} {list(gedcom_project.months.keys())[int(today.strftime("%m"))%12]} {today.strftime("%Y")}'

        result = gedcom_project.upcoming_birthdays(individuals)
        self.assertEqual(result, ['Karen /Domingo/ (@I3@)'])
    # User story 22 Unique ids

    def test_unique_ids(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/'},
                       'dup @I1@': {'id': 'dup @I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/'}}
        result = gedcom_project.get_duplicates(individuals)
        self.assertEqual(result, ['@I1@'])

    # User Case 29: List Diseased
    def test_list_diseased(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '4 JUL 1954'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '19 SEP 2022'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '8 OCT 2022'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        result = gedcom_project.get_deceased(individuals)
        self.assertEqual(result, ['@I5@', '@I7@'])

    # User story 04: marriage before divorce
    def test_marrriage_before_divorce(self):
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 2020'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = gedcom_project.marriageBeforeDivorce(families)
        self.assertEqual(result, False)

    # User story 04: marriage before divorce
    def test_marrriage_before_divorce2(self):
        families = {'@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DIV': {'DATE': '6 MAR 1969'}}}
        result = gedcom_project.marriageBeforeDivorce(families)
        self.assertEqual(result, True)

    # User story 05: marriage before death
    def test_marriage_before_death1(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '4 JUL 1954'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '19 SEP 2022'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '8 OCT 2022'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 2001'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = gedcom_project.marriageBeforeDeath(families, individuals)
        self.assertEqual(result, True)

    # User story 05: marriage before death
    def test_marriage_before_death2(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '4 JUL 1954'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '19 SEP 2022'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '8 OCT 2022'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 2050'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = gedcom_project.marriageBeforeDeath(families, individuals)
        self.assertEqual(result, False)

    # User story 11: No bigamy

    def test_bigamy(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '4 JUL 1954'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '19 SEP 2022'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '8 OCT 2022'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 1969'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 2022'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1969'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = gedcom_project.get_bigamy(families, individuals)
        self.assertEqual(result, [['@I5@', '@I7@']])

    # User story 33: List Orphens
    def test_orphens(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'},
                       '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@',
                             'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}}
        result = gedcom_project.get_orphens(families, individuals)
        self.assertEqual(result, ['@I1@'])

    # User story 39: List Upcoming Anniversary
    def test_upcoming_anniversary(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'},
                       '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}}
        individuals['@I2@']["BIRT"]
        tomorrow = today + timedelta(days=1)
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {
            'DATE': f'{tomorrow.strftime("%d")} {list(gedcom_project.months.keys())[int(tomorrow.strftime("%m"))-1]} 1986'}, 'DATE': '6 MAY 1986'}}
        result = gedcom_project.upcoming_anniversary(families, individuals)
        self.assertEqual(
            result, ['George /Smith/ (@I2@) and Karen /Domingo/ (@I3@) in Family @F1@'])

    # User Story 1: Date Before Current Date
    def test_valid_date(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, "DEAT": {"DATE": "10 JAN 2056"}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'},
                       '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@',
                             'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '15 NOV 2025'}, 'DATE': '6 MAY 1986'}}
        result = gedcom_project.valid_date(families, individuals)
        self.assertEqual(result, ['US01: Death date of George /Smith/ (@I2@) should not be after current date.',
                         'US01: Marriage date of George /Smith/ (@I2@) and Karen /Domingo/ (@I3@) in Family @F1@ should not be after current date.'])

    # User story 06: Divorce Before Death
    def test_divorce_before_death(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'},
                       '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@',
                             'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}}
        result = gedcom_project.divorceAfterDeath(families, individuals)
        self.assertEqual(result, True)

    # User story 07: less than 150 years old
    def test_lessThan150YearsOld(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 1800'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'},
                       '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}}
        result = gedcom_project.lessThan150YearsOld(individuals)
        self.assertEqual(result, True)

    # User story 16: All male members of a family should have the same last name

    def test_male_lastname(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Daniel/', 'SEX': 'M', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'},
                       '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /HAROLD/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@',
                             'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}}
        result = gedcom_project.male_lastname(families, individuals)
        self.assertEqual(result, [['@F1@', '@I1@'], ['@F1@', '@I4@']])

    # User story 18: Siblings should not marry one another
    def test_sibling_marriage(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'},
                       '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}}
        individuals['@I1@']["FAMS"] = '@F2@'
        individuals['@I4@']["FAMS"] = '@F2@'
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@',
                             'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'},
                    '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I1@', 'WIFE': '@I4@',
                             'CHIL': [], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}}
        result = gedcom_project.sibling_marriage(families, individuals)
        self.assertEqual(
            result, [['@F1@', '@I1@', '@I4@'], ['@F1@', '@I4@', '@I1@']])

    # User Story 12 - parents not too old
    def test_parents_too_old(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1900'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'},
                       '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@',
                             'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'},
                    '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I1@', 'WIFE': '@I4@',
                             'CHIL': [], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}}

        result = gedcom_project.parents_too_old(families, individuals)
        self.assertEqual(
            result, [['@F1@', 'father', 80, '@I1@'], ['@F1@', 'father', 80, '@I4@']])

    # User Story 13 - Siblings spacing
    def test_siblings_spacing(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1900'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'},
                       '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@',
                             'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'},
                    '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I1@', 'WIFE': '@I4@',
                             'CHIL': [], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}}

        individuals['@I1@']["BIRT"]["DATE"] = f'{(today).strftime("%d")} {list(gedcom_project.months.keys())[int(today.strftime("%m"))-1]} {today.strftime("%Y")}'
        individuals['@I4@']["BIRT"]["DATE"] = f'{(today).strftime("%d")} {list(gedcom_project.months.keys())[int(today.strftime("%m"))-1]} {today.strftime("%Y")}'

        result = gedcom_project.siblings_spacing(families, individuals)
        self.assertEqual(
            result, [['@F1@', '@I1@', '@I4@'], ['@F1@', '@I4@', '@I1@']])

    # User Story 10 - marriage before 14
    def test_marriage_before_14(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1900'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'},
                       '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@',
                             'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'},
                    '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I1@', 'WIFE': '@I4@',
                             'CHIL': [], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}}
        result = gedcom_project.marriage_before_14(families, individuals)
        self.assertEqual(result, ['@F2@'])

    # Use case 14: Multiple births <= 5 (No more than five siblings should be born at the same time)
    def test_too_many_births(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1900'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'},
                       '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@',
                             'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'},
                    '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I1@', 'WIFE': '@I4@',
                             'CHIL': [], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}}
        individuals['@I5@'] = {'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Tom /Smith/',
                               'SEX': 'M', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}
        individuals['@I6@'] = {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Bob /Smith/',
                               'SEX': 'M', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}
        individuals['@I7@'] = {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Dick /Smith/',
                               'SEX': 'M', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}
        individuals['@I8@'] = {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'John /Smith/',
                               'SEX': 'M', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}
        individuals['@I9@'] = {'id': '@I9@', 'INDI': '@I9@', 'NAME': 'Perry /Smith/',
                               'SEX': 'M', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}
        individuals['@I10@'] = {'id': '@I10@', 'INDI': '@I10@', 'NAME': 'Josh /Smith/',
                                'SEX': 'M', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}

        families['@F1@']["CHIL"] += ['@I5@',
                                     '@I6@', '@I7@', '@I8@', '@I9@', '@I10@']
        result = gedcom_project.multiple_births(families, individuals)
        self.assertEqual(result, [['@F1@', '12 OCT 2010', 7]])

    # Use case 15: There should be fewer than 15 siblings in a family
    def test_max_siblings(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1900'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'},
                       '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@',
                             'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'},
                    '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I1@', 'WIFE': '@I4@',
                             'CHIL': [], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}}
        for i in range(15):
            individuals[f'@I{5+i}'] = {'id': f'@I{5+i}', 'INDI': f'@I{5+i}', 'NAME': f'Tom{i} /Smith/',
                                       'SEX': 'M', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}
            families['@F1@']["CHIL"].append(f'@I{5+i}')
        result = gedcom_project.maxSiblings(families)
        self.assertEqual(result, ['@F1@'])

    # Use Case 30: List living married
    def test_living_married(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '4 JUL 1954'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '19 SEP 2022'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '8 OCT 2022'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '4 JUL 2050'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = gedcom_project.living_married(families, individuals)
        self.assertEqual(result, ['George /Smith/ (@I2@) in Family @F1@',
                         'Karen /Domingo/ (@I3@) in Family @F1@', 'Rose /Viafora/ (@I6@) in Family @F3@'])

    # Use Case 42: Reject Illegitimate Dates
    def test_illegitimate_date(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '74 JUL 1954'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '19 SEP 2022'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '8 OCT 2022'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '34 JUL 2050'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = gedcom_project.illegitimate_date(families, individuals)
        self.assertEqual(result, ['US42: Birthday of Bob /Matthews/ (@I5@) is not a valid date',
                         'US42: Marriage date of Bob /Matthews/ (@I5@) and Rose /Viafora/ (@I6@) in Family @F2@ is not valid.'])

    # Use Case 37: List recent survivors
    def test_recent_survivors(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '74 JUL 1954'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '19 SEP 2022'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '8 OCT 2022'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}, '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I5@', 'WIFE': '@I6@', 'CHIL': [
            '@I3@'], 'MARR': {'DATE': '34 JUL 2050'}, 'DATE': '6 MAR 1969', 'DIV': {'DATE': '6 MAR 1969'}}, '@F3@': {'id': '@F3@', 'FAM': '@F3@', 'HUSB': '@I7@', 'WIFE': '@I6@', 'CHIL': ['@I8@'], 'MARR': {'DATE': '7 JUL 1970'}, 'DATE': '7 JUL 1970', 'TRLR': ''}}
        result = gedcom_project.list_recentSurvivors(families, individuals)
        self.assertEqual(result, ['Karen /Domingo/',
                         'Rose /Viafora/', 'Elise /Domingo/'])

    # Use Case 22: unique Name AndBirthdate
    def test_recent_survivors(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2002'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1958'}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'}, '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}, '@I5@': {
            'id': '@I5@', 'INDI': '@I5@', 'NAME': 'Bob /Matthews/', 'SEX': 'M', 'BIRT': {'DATE': '74 JUL 1954'}, 'DATE': '10 MAY 1969', 'DEAT': {'DATE': '19 SEP 2022'}, 'FAMS': '@F2@'}, '@I6@': {'id': '@I6@', 'INDI': '@I6@', 'NAME': 'Rose /Viafora/', 'SEX': 'F', 'BIRT': {'DATE': '9 SEP 1933'}, 'DATE': '9 SEP 1933', 'FAMS': '@F3@'}, '@I7@': {'id': '@I7@', 'INDI': '@I7@', 'NAME': 'Jimothy /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '6 FEB 1950'}, 'DATE': '16 APR 2015', 'DEAT': {'DATE': '8 OCT 2022'}, 'FAMS': '@F3@'}, '@I8@': {'id': '@I8@', 'INDI': '@I8@', 'NAME': 'Elise /Domingo/', 'SEX': 'F', 'BIRT': {'DATE': '8 SEP 1970'}, 'DATE': '8 SEP 1970', 'FAMC': '@F3@', 'FAM': '@F1@'}}
        result = gedcom_project.uniqueNameAndBirthdate(individuals)
        self.assertEqual(result, False)

    # User Story 19 First cousins should not marry one another  
    def test_cousin_marriage(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1900'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'},
                       '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@',
                             'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'},
                    '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I1@', 'WIFE': '@I4@',
                             'CHIL': [], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}}

        result = gedcom_project.cousin_marriage(families, individuals)
        self.assertEqual(result, [])
        
    # User Story 20: Aunts and uncles should not marry their nieces or nephews
    def test_aunt_uncle_marriage(self):
        individuals = {'@I1@': {'id': '@I1@', 'INDI': '@I1@', 'NAME': 'Gabriela /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '12 OCT 2010'}, 'DATE': '12 OCT 2002', 'FAMC': '@F1@'}, '@I2@': {'id': '@I2@', 'INDI': '@I2@', 'NAME': 'George /Smith/', 'SEX': 'F', 'BIRT': {'DATE': '7 MAR 1900'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '7 MAR 1958', 'FAMS': '@F1@'},
                       '@I3@': {'id': '@I3@', 'INDI': '@I3@', 'NAME': 'Karen /Domingo/', 'SEX': 'M', 'BIRT': {'DATE': '15 OCT 1965'}, "DEAT": {"DATE": "10 JAN 2000"}, 'DATE': '15 OCT 1965', 'FAMS': '@F1@', 'FAMC': '@F2@'}, '@I4@': {'id': '@I4@', 'INDI': '@I4@', 'NAME': 'Matthew /Smith/', 'SEX': 'M', 'BIRT': {'DATE': '31 JUL 2001'}, 'DATE': '31 JUL 2001', 'FAMC': '@F1@'}}
        families = {'@F1@': {'id': '@F1@', 'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@',
                             'CHIL': ['@I1@', '@I4@'], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'},
                    '@F2@': {'id': '@F2@', 'FAM': '@F2@', 'HUSB': '@I1@', 'WIFE': '@I4@',
                             'CHIL': [], 'MARR': {'DATE': '6 MAY 1986'}, 'DATE': '6 MAY 1986'}}

        result = gedcom_project.removed_marriage(families, individuals)
        self.assertEqual(result, [])
if __name__ == '__main__':
    unittest.main()
