# Completing US02 and US03
from prettytable import PrettyTable
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import sys

if 'gedcom_unittests' in sys.argv[0]:
    gedcom = open('test_file.ged', "r")
elif len(sys.argv) > 1:
    gedcom = open(sys.argv[1], "r")
else:
    sys.exit("Please supply gedcom filename as program argument!")


valid = {"INDI": True, "NAME": True, "SEX": True, "BIRT": True, "DEAT": True,
         "FAMC": True, "FAMS": True, "FAM": True, "MARR": True, "HUSB": True,
         "WIFE": True, "CHIL": True, "DIV": True, "DATE": True, "HEAD": True,
         "TRLR": True, "NOTE": True}

months = {"JAN": 1,
          "FEB": 2,
          "MAR": 3,
          "APR": 4,
          "MAY": 5,
          "JUN": 6,
          "JUL": 7,
          "AUG": 8,
          "SEP": 9,
          "OCT": 10,
          "NOV": 11,
          "DEC": 12}

individuals = {}
families = {}


currentInd = None
currentFam = None
dependent = ''
for line in gedcom:
    if currentFam:
        currentInd = None
    if currentInd:
        currentFam = None

    elements = line.strip().split(" ")
    level = elements[0]
    tag = elements[1]
    value = " ".join(elements[2:])

    if(len(elements) > 2 and (elements[2] == 'INDI' or elements[2] == 'FAM')):
        tag = elements[2]
        value = elements[1]
        if tag == 'INDI':
            individuals[value] = {"id": value}
            currentInd = value
        if tag == 'FAM':
            families[value] = {"id": value}
            currentFam = value

    if(currentInd != None and tag in valid):
        individuals[currentInd][tag] = value

    if(currentFam != None and tag in valid):
        if tag == 'CHIL':
            if 'CHIL' in families[currentFam]:
                families[currentFam][tag].append(value)
            else:
                families[currentFam][tag] = [value]
        else:
            families[currentFam][tag] = value

    if(currentInd != None and dependent != ''):
        individuals[currentInd][dependent] = {tag: value}

    if(currentFam != None and dependent != ''):
        families[currentFam][dependent] = {tag: value}

    dependent = ''

    if(tag == 'BIRT' or tag == 'DEAT' or tag == 'MARR' or tag == 'DIV'):
        dependent = tag

    # print(f'-->{line.strip()}')
    #print(f'<--{level}|{tag}|{ "Y" if tag in valid else "N" }|{value}')

iTable = PrettyTable()
# print([*individuals.values()][0])
# print([*families.values()][1])

iTable.add_column("ID", [*individuals])

iTable.add_column("Name", list(
    map(lambda indiv: indiv['NAME'], [*individuals.values()])))

iTable.add_column("Gender", list(
    map(lambda indiv: indiv['SEX'], [*individuals.values()])))

iTable.add_column("Birthday", list(
    map(lambda indiv: indiv['BIRT']['DATE'], [*individuals.values()])))


# Turns a date string into a datetime object
def toDateObj(d):
    dateArray = d.split(" ")
    return date(int(dateArray[2]), months[dateArray[1]], int(dateArray[0]))

# Takes give time in between date1 and date2 in years: date2 > date1


def timespan(date1, date2):
    if not isinstance(date1, date):
        date1 = toDateObj(date1)
    if not isinstance(date2, date):
        date2 = toDateObj(date2)

    days_in_year = 365.2425
    time = int((date2 - date1).days / days_in_year)
    return time

# Gives the death of an individual takes into account death date
# US27


def calculateAge(indiv):
    birthDate = toDateObj(indiv['BIRT']['DATE'])
    compareDate = date.today() if not 'DEAT' in indiv else toDateObj(
        indiv["DEAT"]["DATE"])
    age = timespan(birthDate, compareDate)
    return age


birthBeforeMarriageErrors = []


def birthBeforeMarriage(fam, individuals):
    husbs = []
    wifes = []
    for family in fam.keys():
        husbs.append([fam[family]['HUSB'], fam[family]['MARR']['DATE']])
        wifes.append([fam[family]['WIFE'], fam[family]['MARR']['DATE']])
    for indiv in individuals.keys():
        person = individuals[indiv]["id"]
        birthday = individuals[indiv]['BIRT']["DATE"]
        birthday = birthday.split(" ")
        birthday = date(
            int(birthday[2]), months[birthday[1]], int(birthday[0]))
        for i in husbs:
            if (i[0] == person):
                marriage = i[1]
                marriage = marriage.split(" ")
                marriage = date(
                    int(marriage[2]), months[marriage[1]], int(marriage[0]))
                days = int((marriage - birthday).days)
                if (days < 0):
                    birthBeforeMarriageErrors.append(
                        [i[0], marriage, birthday, "husband"])
                    return False
                    
        for i in wifes:
            if (i[0] == person):
                marriage = i[1]
                marriage = marriage.split(" ")
                marriage = date(
                    int(marriage[2]), months[marriage[1]], int(marriage[0]))
                days = int((marriage - birthday).days)
                if (days < 0):
                    birthBeforeMarriageErrors.append(
                        [i[0], marriage, birthday, "wife"])
                    return False
                    
    return True


birthBeforeDeathErrors = []

def birthBeforeDeath(indiv):
    for indiv in indiv.keys():
        person = individuals[indiv]["id"]
        birthday = individuals[indiv]['BIRT']["DATE"]
        birthday = birthday.split(" ")
        birthday = date(
            int(birthday[2]), months[birthday[1]], int(birthday[0]))
        if ("DEAT" in individuals[indiv]):
            deathdate = individuals[indiv]['DEAT']["DATE"]
            deathdate = deathdate.split(" ")
            deathdate = date(
                int(deathdate[2]), months[deathdate[1]], int(deathdate[0]))
            days = int((deathdate - birthday).days)
            if (days < 0):
                birthBeforeDeathErrors.append([person, deathdate, birthday])
                return False
                
    return True

# User Story 08
def birthBeforeMarriageOfParents(family, individuals):
    if 'MARR' in family:
        for child in family["CHIL"]:
            if toDateObj(family['MARR']['DATE']) > toDateObj(individuals[child]["BIRT"]["DATE"]):
                return True
            if 'DIV' in family:
                if (toDateObj(family['DIV']['DATE']) + relativedelta(months=+9)) < toDateObj(individuals[child]["BIRT"]["DATE"]):
                    return True
    return False


# User Story 09
def birthAfterDeathOfParents(family, individuals):
    for child in family["CHIL"]:
        father_death_date = "N/A" if not 'DEAT' in individuals[family["HUSB"]] else individuals[family["HUSB"]]['DEAT']['DATE']
        mother_death_date = "N/A" if not 'DEAT' in individuals[family["WIFE"]] else individuals[family["WIFE"]]['DEAT']['DATE']

        if father_death_date != 'N/A':
            # child must be born before 9 months after death of father
            if toDateObj(father_death_date) + relativedelta(months=+9) < toDateObj(individuals[child]["BIRT"]["DATE"]):
                return True

        if mother_death_date != 'N/A':
            # child must be born before death of mother
            if toDateObj(mother_death_date) < toDateObj(individuals[child]["BIRT"]["DATE"]):
                return True

    return False



birthBeforeMarriage(families, individuals)
birthBeforeDeath(individuals)



# Testing for Use Case 21: Correct Gender for Role
def correct_gender(families,individuals):
    genderErrors = []
    for family in list(families.values()):
        if individuals[family['HUSB']]['SEX'] != "M":
            genderErrors.append("ERROR: INDIVIDUAL: US21: Gender of Husband " +
                        individuals[family['HUSB']]['NAME']+' ('+family['HUSB']+') ' + "in Family "+family['FAM']+" "+"is female.")
        if individuals[family['WIFE']]['SEX'] != "F":
            genderErrors.append("ERROR: INDIVIDUAL: US21: Gender of Wife " +
                        individuals[family['WIFE']]['NAME']+' ('+family['WIFE']+') '+"in Family "+family['FAM']+" "+"is male.")
    return genderErrors


# Testing for Use Case 35: List Recent Births
def recent_births(families,individuals):
    people = []
    for person in list(individuals.values()):
        birthday = person["BIRT"]["DATE"].split()
        thirty_days_ago = datetime.today()-timedelta(days=30)
        datetime_birthday = datetime(int(birthday[2]), int(
            months[birthday[1]]), int(birthday[0]))
        if(thirty_days_ago <= datetime_birthday):
            people.append(person["NAME"]+" ("+person["id"]+")")
    errors.append("US35: List of people who were born in the last 30 days: "+str(people))
    return people


iTable.add_column("Age", list(
    map(lambda indiv: calculateAge(indiv), [*individuals.values()])))

iTable.add_column("Alive", list(
    map(lambda indiv: False if 'DEAT' in indiv else True, [*individuals.values()])))

iTable.add_column("Death", list(map(
    lambda indiv: "N/A" if not 'DEAT' in indiv else indiv["DEAT"]["DATE"], [*individuals.values()])))

fTable = PrettyTable()

fTable.add_column("ID", [*families])

fTable.add_column("Married", list(map(
    lambda fam: 'N/A' if "MARR" not in fam else fam['MARR']['DATE'], [*families.values()])))

fTable.add_column("Divorced", list(map(
    lambda fam: 'N/A' if "DIV" not in fam else fam['DIV']['DATE'], [*families.values()])))

fTable.add_column("Husband ID", list(map(
    lambda fam: 'N/A' if "HUSB" not in fam else fam["HUSB"], [*families.values()])))

fTable.add_column("Husband Name", list(map(
    lambda fam: 'N/A' if "HUSB" not in fam else individuals[fam["HUSB"]]["NAME"], [*families.values()])))

fTable.add_column("Wife ID", list(map(
    lambda fam: 'N/A' if "WIFE" not in fam else fam["WIFE"], [*families.values()])))

fTable.add_column("Wife Name", list(map(
    lambda fam: 'N/A' if "WIFE" not in fam else individuals[fam["WIFE"]]["NAME"], [*families.values()])))

fTable.add_column("Children", list(map(
    lambda fam: 'N/A' if "CHIL" not in fam else fam['CHIL'], [*families.values()])))

# Error Area
# structure of indiv and fam: dictionary {id1: -> {details1}, id2: {details2} }
# accumulation array for all errors detecting during looping through individuals and families
errors=[]
genderErrors=correct_gender(families, individuals)
recent_births(families, individuals)
errors=errors+genderErrors


if (len(birthBeforeMarriageErrors) > 0):
    for i in birthBeforeMarriageErrors:
        if (i[3] == "husband"):
            errors.append(
                f"ERROR: FAMILY: US02: {i[0]} : Husband's birthdate {i[2]} occurs after marriage date {i[1]}")
        elif (i[3] == "wife"):
            errors.append(
                f"ERROR: FAMILY: US02: {i[0]} : Wife's birthdate {i[2]} occurs after marriage date {i[1]}")

if (len(birthBeforeDeathErrors) > 0):
    for i in birthBeforeDeathErrors:
        errors.append(
            f"ERROR: INDIVIDUAL: US03 {i[0]} : Died {i[1]} before born {i[2]}")

for i, details in individuals.items():
    # check for errors in individuals

    # Remove this when code is added to the loop
    break
for f, details in families.items():
    # check for errors in families

    #US 08
    if birthBeforeMarriageOfParents(details, individuals):
            errors.append(
                f"ERROR: FAMILY: US08: {f} marriage after birth of child")
    
    #Makes sure a child couldnt have been born after their parents have died
    #US 09
    if birthAfterDeathOfParents(details, individuals):
            errors.append(
                f"ERROR: FAMILY: US09: {f} birth of child after death of parents")
    # check for marriage before 14
    # US10
    if "MARR" in details:
        if timespan(individuals[details["HUSB"]]["BIRT"]["DATE"], details["MARR"]["DATE"]) < 14 or timespan(individuals[details["WIFE"]]["BIRT"]["DATE"], details["MARR"]["DATE"]) < 14:
            errors.append(
                f"ERROR: FAMILY: US10: {f} marriage before 14 years of age")

if __name__ == '__main__':
    print("Individuals:")
    print(iTable)
    print("Families:")
    print(fTable)
    # Print errors
    print()
    for error in errors:
        print(error)


gedcom.close()
