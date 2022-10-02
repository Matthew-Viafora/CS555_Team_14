# Completing US02 and US03
from prettytable import PrettyTable
from datetime import date

gedcom = open("test_file.ged", "r")

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

# Need to fix to adjust for death date


def calculateAge(indiv):
    dateArray = indiv['BIRT']['DATE'].split(" ")
    birthDate = date(int(dateArray[2]),
                     months[dateArray[1]], int(dateArray[0]))
    days_in_year = 365.2425
    age = int((date.today() - birthDate).days / days_in_year)
    return age


birthBeforeMarriageErrors = []


def birthBeforeMarriage(fam):
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
    return True


birthBeforeDeathErrors = []


def birthBeforeDeath(indiv):
    for indiv in individuals.keys():
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
    return True


birthBeforeMarriage(families)
birthBeforeDeath(individuals)


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


print("Individuals:")
print(iTable)
print("Families:")
print(fTable)

errors = []

if (len(birthBeforeMarriageErrors) > 0):
    for i in birthBeforeMarriageErrors:
        if (i[3] == "husband"):
            errors.append(
                f"ERROR: FAMILY: {i[0]} : Husband's birthdate {i[2]} occurs after marriage date {i[1]}")
        elif (i[3] == "wife"):
            errors.append(
                f"ERROR: FAMILY: {i[0]} : Wife's birthdate {i[2]} occurs after marriage date {i[1]}")

if (len(birthBeforeDeathErrors) > 0):
    for i in birthBeforeDeathErrors:
        errors.append(
            f"ERROR: INDIVIDUAL: {i[0]} : Died {i[1]} before born {i[2]}")


gedcom.close()
