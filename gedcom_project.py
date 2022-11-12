from cmath import e
from prettytable import PrettyTable
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import sys

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


def readfile(filename):
    individuals = {}
    families = {}
    currentInd = None
    currentFam = None
    dependent = ''
    with open(filename, 'r') as gedcom:
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
                    # duplicate id checking
                    if value in individuals:
                        value = 'dup ' + value
                    individuals[value] = {"id": value}
                    currentInd = value
                if tag == 'FAM':
                    # duplicate id checking
                    if value in families:
                        value = 'dup ' + value
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
    return [individuals, families]


if 'gedcom_unittests' in sys.argv[0]:
    filename = "test_file.ged"
elif len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    sys.exit("Please supply gedcom filename as program argument!")

individuals, families = readfile(filename)

#-----------------------------------------------------Helper Functions-----------------------------------------------------#


# Turns a date string into a datetime object
def toDateObj(d):
    if isinstance(d, date):
        return d
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


def timespan_days(date1, date2):
    # get timespan in days
    if not isinstance(date1, date):
        date1 = toDateObj(date1)
    if not isinstance(date2, date):
        date2 = toDateObj(date2)

    time = int((date2 - date1).days)  # days in year, gives time in years
    return time
# Gives the death of an individual takes into account death date
# US27


def calculateAge(indiv):
    birthDate = toDateObj(indiv['BIRT']['DATE'])
    compareDate = date.today() if not 'DEAT' in indiv else toDateObj(
        indiv["DEAT"]["DATE"])
    age = timespan(birthDate, compareDate)
    return age

def findRecent(individuals, case):
    people = []
    for indiv in individuals.keys():
        if (case in individuals[indiv]):
            date = individuals[indiv][case]["DATE"]
            date = date.split(" ")
            thirty_days_ago = datetime.today()-timedelta(days=30)
            datetime_date = datetime(
                int(date[2]), int(months[date[1]]), int(date[0]))
            if(thirty_days_ago <= datetime_date):
                people.append(individuals[indiv]["NAME"]+" ("+indiv+")")
    if(case == "DEAT"):
        errors.append(
            "US36: List of people who died in the last 30 days: "+str(people))
    if(case == "BIRT"):
        errors.append(
            "US35: List of people who were born in the last 30 days: "+str(people))
    return people
    
#-----------------------------------------------------Helper Functions END-----------------------------------------------------#

#Builds the individuals table
iTable = PrettyTable()

iTable.add_column("ID", [*individuals])

iTable.add_column("Name", list(
    map(lambda indiv: indiv['NAME'], [*individuals.values()])))

iTable.add_column("Gender", list(
    map(lambda indiv: indiv['SEX'], [*individuals.values()])))

iTable.add_column("Birthday", list(
    map(lambda indiv: indiv['BIRT']['DATE'], [*individuals.values()])))

#US27 include individual ages
iTable.add_column("Age", list(
    map(lambda indiv: calculateAge(indiv), [*individuals.values()])))

iTable.add_column("Alive", list(
    map(lambda indiv: False if 'DEAT' in indiv else True, [*individuals.values()])))

iTable.add_column("Death", list(map(
    lambda indiv: "N/A" if not 'DEAT' in indiv else indiv["DEAT"]["DATE"], [*individuals.values()])))

#Builds the family table
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

errors = []

#-----------------------------------------------------Sprint 1-----------------------------------------------------#
# US 02
birthBeforeMarriageErrors = []
husbs = []
wifes = []


def birthdayBeforeMarriage(person, birthday, spouse):
    for i in spouse:
        if (i[0] == person):
            marriage = i[1]
            marriage = marriage.split(" ")
            marriage = date(
                int(marriage[2]), months[marriage[1]], int(marriage[0]))
            days = int((marriage - birthday).days)
            if (days < 0):
                if(spouse == husbs):
                    birthBeforeMarriageErrors.append(
                        [i[0], marriage, birthday, "husband"])
                if(spouse == wifes):
                    birthBeforeMarriageErrors.append(
                        [i[0], marriage, birthday, "wife"])
                return False
    return True

def birthBeforeMarriage(fam, individuals):
    for family in fam.keys():
        husbs.append([fam[family]['HUSB'], fam[family]['MARR']['DATE']])
        wifes.append([fam[family]['WIFE'], fam[family]['MARR']['DATE']])
    for indiv in individuals.keys():
        person = individuals[indiv]["id"]
        birthday = individuals[indiv]['BIRT']["DATE"]
        birthday = birthday.split(" ")
        birthday = date(
            int(birthday[2]), months[birthday[1]], int(birthday[0]))

        if(not birthdayBeforeMarriage(person, birthday, husbs)):
            return False
        if(not birthdayBeforeMarriage(person, birthday, wifes)):
            return False

    return True

# US03
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

birthBeforeMarriage(families, individuals)
birthBeforeDeath(individuals)

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


# Testing for Use Case 21: Correct Gender for Role
def correct_gender(families, individuals):
    genderErrors = []
    for family in list(families.values()):
        if individuals[family['HUSB']]['SEX'] != "M":
            genderErrors.append("ERROR: INDIVIDUAL: US21: Gender of Husband " +
                                individuals[family['HUSB']]['NAME']+' ('+family['HUSB']+') ' + "in Family "+family['FAM']+" "+"is female.")
        if individuals[family['WIFE']]['SEX'] != "F":
            genderErrors.append("ERROR: INDIVIDUAL: US21: Gender of Wife " +
                                individuals[family['WIFE']]['NAME']+' ('+family['WIFE']+') '+"in Family "+family['FAM']+" "+"is male.")
    return genderErrors
genderErrors = correct_gender(families, individuals)
errors = errors+genderErrors

# Testing for Use Case 35: List Recent Births
def recent_births(individuals):
    return findRecent(individuals, "BIRT")
recent_births(individuals)

# US10
# check for marriage before 14
def marriage_before_14(families, individuals):
    results = []
    for f, details in families.items():
        if "MARR" in details:
            if timespan(individuals[details["HUSB"]]["BIRT"]["DATE"], details["MARR"]["DATE"]) < 14 or timespan(individuals[details["WIFE"]]["BIRT"]["DATE"], details["MARR"]["DATE"]) < 14:
                results.append(f)
    return results

for f in marriage_before_14(families, individuals):
    errors.append(f"ERROR: FAMILY: US10: {f} marriage before 14 years of age")

#US 27 found in table output

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
        father_death_date = "N/A" if not 'DEAT' in individuals[family["HUSB"]
                                                               ] else individuals[family["HUSB"]]['DEAT']['DATE']
        mother_death_date = "N/A" if not 'DEAT' in individuals[family["WIFE"]
                                                               ] else individuals[family["WIFE"]]['DEAT']['DATE']

        if father_death_date != 'N/A':
            # child must be born before 9 months after death of father
            if toDateObj(father_death_date) + relativedelta(months=+9) < toDateObj(individuals[child]["BIRT"]["DATE"]):
                return True

        if mother_death_date != 'N/A':
            # child must be born before death of mother
            if toDateObj(mother_death_date) < toDateObj(individuals[child]["BIRT"]["DATE"]):
                return True

    return False

for f, details in families.items():
    # check for errors in families

    # US 08
    if birthBeforeMarriageOfParents(details, individuals):
        errors.append(
            f"ERROR: FAMILY: US08: {f} marriage after birth of child")

    # Makes sure a child couldnt have been born after their parents have died
    # US 09
    if birthAfterDeathOfParents(details, individuals):
        errors.append(
            f"ERROR: FAMILY: US09: {f} birth of child after death of parents")

#-----------------------------------------------------Sprint 1 end-----------------------------------------------------#
#-----------------------------------------------------Sprint 2-----------------------------------------------------#
# US04
marriageBeforeDivorceErrors = []


def marriageBeforeDivorce(fam):
    ans = False
    for family in fam.keys():
        try:
            if (fam[family]['DIV']):
                if (familyHasDivorce(fam, family)):
                    ans = True
        except:
            continue
    return ans

# Helper functions of MarriageBeforeDivorce() function for readability:


def familyHasDivorce(fam, family):
    divorce = fam[family]['DIV']['DATE']
    marriage = fam[family]['MARR']['DATE']
    if toDateObj(divorce) < toDateObj(marriage):
        marriageBeforeDivorceErrors.append(
            [fam[family]['FAM'], toDateObj(divorce), toDateObj(marriage)])
        return True
# End of helper functions


marriageBeforeDeathErrors = []


def marriageBeforeDeath(fam, individuals):
    husbs = []
    wifes = []
    for family in fam.keys():
        husbs.append([fam[family]['HUSB'], fam[family]['MARR']['DATE']])
        wifes.append([fam[family]['WIFE'], fam[family]['MARR']['DATE']])
    for indiv in individuals.keys():
        person = individuals[indiv]["id"]
        try:
            deathdate = toDateObj(individuals[indiv]['DEAT']["DATE"])
        except:
            continue
        if (not iterThroughHusbsAndWives(husbs, person, deathdate, spouse='husb')):
            return False
        if (not iterThroughHusbsAndWives(wifes, person, deathdate, spouse='wife')):
            return False

    return True

# Helper functions of MarriageBeforeDeath() function for readability:


def iterThroughHusbsAndWives(spouses, person, deathdate, spouse):
    for i in spouses:
        if (i[0] == person):
            marriage = toDateObj(i[1])
            if (deathdate < marriage):
                if (spouse == "husb"):
                    marriageBeforeDeathErrors.append(
                        [i[0], marriage, deathdate, "husband"])
                    return False
                elif (spouse == "wife"):
                    marriageBeforeDeathErrors.append(
                        [i[0], marriage, deathdate, "wife"])
                    return False
    return True
# End of helper functions

marriageBeforeDivorce(families)
marriageBeforeDeath(families, individuals)
if (len(marriageBeforeDivorceErrors) > 0):
    for i in marriageBeforeDivorceErrors:
        errors.append(
            f"ERROR: FAMILY: US04 {i[0]} : Divorced {i[1]} before married {i[2]}")

if (len(marriageBeforeDeathErrors) > 0):
    for i in marriageBeforeDeathErrors:
        if (i[3] == 'husband'):
            errors.append(
                f"ERROR: FAMILY: US05 {i[0]} : Married {i[2]} after husband's death on {i[1]}")
        elif (i[3] == 'wife'):
            errors.append(
                f"ERROR: FAMILY: US05 {i[0]} : Married {i[2]} after wife's death on {i[1]}")

# Testing for Use Case 36: List Recent Deaths
def recent_deaths(individuals):
    return findRecent(individuals, "DEAT")
recent_deaths(individuals)

# Testing for Use Case 38: List Upcoming Birthdays
def upcoming_birthdays(individuals):
    people = []
    for person in list(individuals.values()):
        birthday = person["BIRT"]["DATE"].split()
        thirty_days_after = datetime.today()+timedelta(days=30)
        datetime_birthday = datetime(datetime.now().year, int(
            months[birthday[1]]), int(birthday[0]))
        if(datetime.today() <= datetime_birthday and datetime_birthday <= thirty_days_after):
            people.append(person["NAME"]+" ("+person["id"]+")")
    errors.append(
        "US38: List of people who have an upcoming birthday in the next 30 days: "+str(people))
    return people
upcoming_birthdays(individuals)

# Testing for Use Case 22: Unique IDs
def get_duplicates(individuals):
    return [i.replace('dup ', '') for i in individuals if 'dup' in i]
duplicates = get_duplicates(individuals)
if(duplicates):
    errors.append(
        f"ERROR: INDIVIDUAL/FAMILY: US23: Duplicate IDs found: {', '.join(duplicates)}")

# Testing for Use Case 29: List Diseased
def get_deceased(individuals):
    return [i for i, details in individuals.items() if 'DEAT' in details]
deceased = get_deceased(individuals)
if(len(deceased)):
    errors.append(
        f"US29: List of all deceased individuals: {', '.join(deceased)}")

# US12 parents not too old - Mother should be less than 60 years older than her children and faher should be less than 80 years older than his children
def parents_too_old(families, individuals):
    results = []
    for f, details in families.items():
        if "CHIL" in details:
            for child in details["CHIL"]:
                t = timespan(individuals[details["HUSB"]]["BIRT"]
                            ["DATE"], individuals[child]["BIRT"]["DATE"])
                if t > 80:
                    results.append([f, "father", 80, child] )
                t = timespan(individuals[details["WIFE"]]["BIRT"]
                            ["DATE"], individuals[child]["BIRT"]["DATE"])
                if t > 60:
                    results.append([f, "mother", 60, child] )
    return results
for f, member, years, child in parents_too_old(families, individuals):
    errors.append(f"ERROR: FAMILY: US12: {f} {member} is more than {years} years older than the child {child}")
    
# US 13 - Siblings spacing - Birth dates of siblings should be more than 8 months apart or less than 2 days apart
def siblings_spacing(families, individuals):
    results = []
    for f, details in families.items():
        if "CHIL" in details:
            for child in details["CHIL"]:
                for child2 in details["CHIL"]:
                    if child != child2:
                        t = timespan_days(individuals[child]["BIRT"]
                                        ["DATE"], individuals[child2]["BIRT"]["DATE"])
                        if (t < 2 or t > 8*30) and t >= 0:
                            results.append([f, child, child2])
    return results
for f, child, child2 in siblings_spacing(families, individuals):
    errors.append(f"ERROR: FAMILY: US13: {f} siblings {child} and {child2} are not born within 2 days or 8 months")
#-----------------------------------------------------Sprint 2 end-----------------------------------------------------#
#-----------------------------------------------------Sprint 3-----------------------------------------------------#
#Testing for Use Case 29: List Upcoming Anniversaries
def upcoming_anniversary(family,individuals):
    families = []
    for fam in list(family.values()):
        anniversary = fam["MARR"]["DATE"].split()
        thirty_days_after = datetime.today()+timedelta(days=30)
        datetime_anniversary = datetime(datetime.now().year, int(
            months[anniversary[1]]), int(anniversary[0]))
        if(datetime.today() <= datetime_anniversary and datetime_anniversary <= thirty_days_after):
            families.append(individuals[fam['HUSB']]['NAME']+' ('+fam['HUSB']+') and ' + individuals[fam['WIFE']]['NAME']+' ('+fam['WIFE']+') ' "in Family "+fam['FAM'])
    errors.append(
        "US29: List of people who have an upcoming anniversary in the next 30 days: "+str(families))
    return families
upcoming_anniversary(families, individuals)

#Testing for Use Case 1:Dates Before Current Date
def valid_date(families,individuals):
    notValid=[]
    for indiv in individuals.keys():
        birthday = individuals[indiv]['BIRT']["DATE"]
        birthday = birthday.split(" ")
        birthday = datetime(int(birthday[2]), months[birthday[1]], int(birthday[0]))
        if(birthday>datetime.today()):
            notValid.append("US01: Birthday of "+individuals[indiv]['NAME']+' ('+individuals[indiv]["id"]+') should not be after current date.')
        
        if ("DEAT" in individuals[indiv]):
            deathdate = individuals[indiv]['DEAT']["DATE"]
            deathdate = deathdate.split(" ")
            deathdate = datetime(int(deathdate[2]), months[deathdate[1]], int(deathdate[0]))
            if(deathdate>datetime.today()):
                notValid.append("US01: Death date of "+individuals[indiv]['NAME']+' ('+individuals[indiv]["id"]+') should not be after current date.')

    for fam in families:
        marriage=families[fam]['MARR']['DATE']
        marriage=marriage.split(" ")
        marriage = datetime(int(marriage[2]), months[marriage[1]], int(marriage[0]))
        if(marriage>datetime.today()):
            notValid.append("US01: Marriage date of "+individuals[families[fam]['HUSB']]['NAME']+' ('+families[fam]['HUSB']+') and ' + individuals[families[fam]['WIFE']]['NAME']+' ('+families[fam]['WIFE']+") in Family "+families[fam]['FAM']+ " should not be after current date.")

        if("DIV" in fam):
            divorcedate=fam['DIV']['DATE']
            divorcedate=divorcedate.split(" ")
            divorcedate=datetime(int(divorcedate[2]), months[divorcedate[1]], int(divorcedate[0]))
            if(divorcedate>datetime.today()):
                notValid.append("US01: Divorce date of "+individuals[families[fam]['HUSB']]['NAME']+' ('+families[fam]['HUSB']+') and ' + individuals[families[fam]['WIFE']]['NAME']+' ('+families[fam]['WIFE']+') ' "in Family "+families[fam]['FAM']+' should not be after current date.')
    return notValid

validDate=valid_date(families,individuals)
if len(validDate):
    for i in range(len(validDate)):
        errors.append(validDate[i])

# US 06
divorceAfterDeathErrors = []
def divorceAfterDeath(fam, individuals):
    husbs = []
    wifes = []
    for family in fam.keys():
        try:
            if (fam[family]['DIV']):
                husbs.append([fam[family]['HUSB'], fam[family]['DIV']['DATE']])
                wifes.append([fam[family]['WIFE'], fam[family]['DIV']['DATE']])
        except:
            continue
    for indiv in individuals.keys():
        person = individuals[indiv]["id"]
        for husb in husbs:
            if (husb[0] == person):
                divorce = toDateObj(husb[1])
                try:
                    deathdate = toDateObj(individuals[indiv]['DEAT']["DATE"])
                except:
                    continue
                if (divorce > deathdate):
                    divorceAfterDeathErrors.append(
                        [husb[0], divorce, deathdate, "husb"])
                    return False

        for wife in wifes:
            if (wife[0] == person):
                divorce = toDateObj(wife[1])
                try:
                    deathdate = toDateObj(individuals[indiv]['DEAT']["DATE"])
                except:
                    continue
                print(divorce)
                print(deathdate)
                if (divorce > deathdate):
                    divorceAfterDeathErrors.append(
                        [wife[0], divorce, deathdate, "wife"])
                    return False
    return True
divorceAfterDeath(families, individuals)

# US 07
lessThan150Errors = []
def lessThan150YearsOld(individuals):
    res = False
    for indiv in individuals.keys():
        person = individuals[indiv]["id"]
        try:
            # dead
            deathdate = toDateObj(individuals[indiv]['DEAT']["DATE"])
            birthdate = toDateObj(individuals[indiv]['BIRT']["DATE"])
            if (deathdate - birthdate >= 150):
                lessThan150Errors.append([person, birthdate])
                res = True
        except:
            # living
            birthdate = toDateObj(individuals[indiv]['BIRT']["DATE"])
            ans = toDateObj(date.today()) - birthdate
            if ((int(ans.days))/365 >= 150):
                lessThan150Errors.append([person, birthdate])
                res = True
    return res
lessThan150YearsOld(individuals)

if (len(divorceAfterDeathErrors) > 0):
    for i in divorceAfterDeathErrors:
        if (i[3] == 'husb'):
            errors.append(
                f"ERROR: FAMILY: US06 {i[0]} : Divorced {i[1]} after husband's death on {i[2]}"
            )
        elif (i[3] == 'wife'):
            errors.append(
                f"ERROR: FAMILY: US06 {i[0]} : Divorced {i[1]} after husband's death on {i[2]}"
            )
if (len(lessThan150Errors) > 0):
    for i in lessThan150Errors:
        errors.append(
            f"ERROR: INDIVIDUAL: US07 : {i[0]} : More than 150 years old - Birth date {i[1]}"
        )

# US 16
# All male members of a family should have the same last name
def male_lastname(families, individuals):
    results = []
    for f, details in families.items():
        if "CHIL" in details:
            for child in details["CHIL"]:
                # get the last name of the child
                childLastName = individuals[child]["NAME"].split(" ")[-1]
                # get the last name of the father
                fatherLastName = individuals[details["HUSB"]]["NAME"].split(" ")[-1]
                # if the child is male and father is male and the last names are different
                if childLastName != fatherLastName and individuals[child]["SEX"] == "M":
                    results.append([f, child])

    return results
for f, child in male_lastname(families, individuals):
    errors.append(f"ERROR: FAMILY: US16: {f} child {child} has a different last name than their parents")

# US 18
# Siblings should not marry one another
def sibling_marriage(families, individuals):
    results = []
    for f, details in families.items():
        if "CHIL" in details:
            for child in details["CHIL"]:
                for child2 in details["CHIL"]:
                    if child != child2:
                        if "FAMS" in individuals[child] and "FAMS" in individuals[child2]:
                            if individuals[child]["FAMS"] == individuals[child2]["FAMS"]:
                                results.append([f, child, child2])
    return results
for f, child, child2 in sibling_marriage(families, individuals): 
    errors.append(f"ERROR: FAMILY: US18: {f} siblings {child} and {child2} are married")

# Use Case 11: No bigamy (marriage during current marriage)
def get_bigamy(families, individuals):
    married_pairs = {}
    for id, info in families.items():
        if info["HUSB"] not in married_pairs:
            married_pairs[info["HUSB"]] = [
                [info["WIFE"], info["MARR"], info.get("DIV", {"DATE": date.today()})]]
        else:
            married_pairs[info["HUSB"]].append(
                [info["WIFE"], info["MARR"], info.get("DIV", {"DATE": date.today()})])

        if info["WIFE"] not in married_pairs:
            married_pairs[info["WIFE"]] = [
                [info["HUSB"], info["MARR"], info.get("DIV", {"DATE": date.today()})]]
        else:
            married_pairs[info["WIFE"]].append(
                [info["HUSB"], info["MARR"], info.get("DIV", {"DATE": date.today()})])

    bigamy_pairs = []
    for id, partners in married_pairs.items():
        if len(partners) > 1:
            # If any marriage ranges overlap then there is bigamy
            for p in range(len(partners)):
                for other_p in range(p + 1, len(partners)):
                    if (toDateObj(partners[p][1]["DATE"]) <= toDateObj(partners[other_p][2]["DATE"])) and (toDateObj(partners[other_p][1]["DATE"]) <= toDateObj(partners[p][2]["DATE"])):
                        bigamy_pairs.append(
                            [partners[p][0], partners[other_p][0]])
    return bigamy_pairs
bigamy_pairs = get_bigamy(families, individuals)
if len(bigamy_pairs):
    errors.append(
        f"ERROR: FAMILY: US11: Bigamy between pairs {' '.join(bigamy_pairs)} ")

# Use case 33: List Orphens (both parents dead < 18 years old)
def get_orphens(families, individuals):
    orphens = []
    for id, info in families.items():
        # Checks if both parents are deceased
        if "DEAT" in individuals[info["HUSB"]] and "DEAT" in individuals[info["WIFE"]]:
            for c in info["CHIL"]:
                if calculateAge(individuals[c]) < 18:
                    orphens.append(c)

    return orphens
orphens = get_orphens(families, individuals)
if len(orphens):
    errors.append(f"US33: List of all orphens: {', '.join(orphens)}")
#-----------------------------------------------------Sprint 3 end-----------------------------------------------------#
#-----------------------------------------------------Sprint 4-----------------------------------------------------#
# Use case 14: Multiple births <= 5 (No more than five siblings should be born at the same time)
def multiple_births(families, individuals):
    results = []
    for id, info in families.items():
        birthtimes = {}
        if "CHIL" in info:
            for c in info["CHIL"]:
                if individuals[c]["BIRT"]["DATE"] in birthtimes:
                    birthtimes[individuals[c]["BIRT"]["DATE"]] += 1  
                else:
                    birthtimes[individuals[c]["BIRT"]["DATE"]] = 1
        
        for d, births in birthtimes.items():
            if births > 5:
                results.append([id, d, births])
    return results

tooManyBirths = multiple_births(families, individuals)
for fam, d, births in tooManyBirths:
        errors.append(f"ERROR: FAMILY: US14: FAM {fam} has too many births on {d} births: {births}")

# Use case 15: There should be fewer than 15 siblings in a family
def maxSiblings(families):
    return  [f for f, details in families.items() if len(details["CHIL"]) >= 15]

for fam in maxSiblings(families):
    errors.append(f"ERROR: FAMILY: US15: FAM {fam} has 15 or more siblings")

#-----------------------------------------------------Sprint 4 end-----------------------------------------------------#









if __name__ == '__main__':
    print("Individuals:")
    print(iTable)
    print("Families:")
    print(fTable)
    # Print errors
    print()
    #Sort errors by user story
    errors.sort(key=lambda x:int(x[x.find("US")+2:x.find("US")+4]))
    for error in errors:
        print(error)
