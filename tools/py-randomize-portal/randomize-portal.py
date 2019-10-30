# Creates a portal document with completely random content.
# Image and object identifiers used in the portal document are real ids on dev.nceas.ucsb.edu
# To run, call `python3 randomize-portal.py` and the resulting portal doc will be saved as `portal.xml`
# Author: Lauren Walker

import random
import string
import re
import datetime

global ID_POOL
global IMAGE_POOL
global WORD_POOL
global ICON_POOL
global STR_FIELD_POOL

def createRandomPools():
    #Get the list of ids from the local ids file
    idFile = open("ids.txt", "r")
    global ID_POOL
    ID_POOL = idFile.readlines()
    idFile.close()

    #Get the list of image ids from the local image ids file
    imageIdFile = open("imageIds.txt", "r")
    global IMAGE_POOL
    IMAGE_POOL = imageIdFile.readlines()
    imageIdFile.close()

    #Get the list of words from the local words file
    wordsFile = open("random_words.txt", "r")
    global WORD_POOL
    WORD_POOL = wordsFile.readlines()
    wordsFile.close()

    #Get the list of icons from the local icons file
    iconFile = open("icons.txt", "r")
    global ICON_POOL
    ICON_POOL = iconFile.readlines()
    iconFile.close()

    global STR_FIELD_POOL
    STR_FIELD_POOL = ["abstract", "attribute", "attributeDescription", "attributeLabel", "attributeName",
              "awardTitle", "fundingText", "gcmdKeyword", "keyConcept", "keywordsText", "projectText", "text", "title", "topicText"]

#Makes a single random word
def makeRandomWord():
    word = random.choice(WORD_POOL)
    word = re.sub("[^a-zA-Z0-9]", "", word)
    return word

#Gets a single random icon
def makeRandomIcon():
    icon = random.choice(ICON_POOL)
    icon = re.sub("[^a-zA-Z0-9]", "", icon)
    return icon

#Makes the given number of random words, separated by spaces
def makeRandomWords(numberWords=20):
    words = random.sample(WORD_POOL, numberWords)

    words = " ".join(words)

    return re.sub("[^a-zA-Z0-9 ]", "", words)

#Makes 1-10 random collection definition filters XML
def makeRandomFilters():
    filtersXML = ""

    for n in range(random.randint(1,10)):
        filtersXML += makeRandomFilter()

    return filtersXML

#Makes a single random filter
def makeRandomFilter():
    types = ["filter", "idFilter", "dateFilter", "booleanFilter"]
    chosenType = random.choice(types)
    if chosenType == "filter":
        return makeTextFilter()
    elif chosenType == "idFilter":
        return makeIdFilter()
    elif chosenType == "dateFilter":
        return makeDateFilter()
    elif chosenType == "booleanFilter":
        return makeBooleanFilter()

def makeFilterLabel():
    #Generate a random label or skip one altogether
    return "\t\t<label>" + makeRandomWords(random.randint(1,3)) + "</label>\n"

def makeFilterOperator():
    #Choose a random operator or skip one altogether
    operators = ["\t\t<operator>AND</operator>\n", "\t\t<operator>OR</operator>\n", ""]

    return random.choice(operators)

def makeFilterExclude():
    #Add an exclude element
    exclude = ["\t\t<exclude>true</exclude>\n", "\t\t<exclude>false</exclude>\n", ""]
    return random.choice(exclude)

#Makes a text filter with random values
def makeTextFilter():

    xml = "\t<filter>\n"

    xml += makeFilterLabel()

    #randomly create fields
    for n in range(random.randint(1,3)):
        xml += "\t\t<field>" + random.choice(STR_FIELD_POOL) + "</field>\n"

    xml += makeFilterOperator()

    xml += makeFilterExclude()

    #Add an matchSubstring element
    matchSubstring = ["\t\t<matchSubstring>true</matchSubstring>\n", "\t\t<matchSubstring>false</matchSubstring>\n", ""]
    xml += random.choice(matchSubstring)

    #randomly create values
    for n in range(random.randint(1,5)):
        xml += "\t\t<value>" + makeRandomWords(random.randint(1,3)) + "</value>\n"

    xml += "\t</filter>\n"

    return xml

#Generates an id filter
def makeIdFilter():
    xml = "\t<filter>\n"

    xml += makeFilterLabel()

    xml += "\t\t<field>id</field>\n"

    xml += makeFilterExclude()

    #Get the list of ids from the local ids file
    idFile = open("ids.txt", "r")
    ids = idFile.readlines()
    idFile.close()

    for n in range(random.randint(1,20)):
        xml += "\t\t<value>" + ids[random.randint(0, len(ids) - 1)].rstrip() + "</value>\n"

    xml += "\t</filter>\n"

    return xml

#Generates an date filter
def makeDateFilter():
    xml = "\t<dateFilter>\n"

    #Make a filter label
    xml += makeFilterLabel()

    #The list of date fields in the search index
    fields = ["updateDate", "beginDate", "dateModified", "datePublished",
              "dateUploaded", "endDate", "pubDate", "replicaVerifiedDate"]

    #Randomly select a field
    xml += "\t\t<field>" + random.choice(fields) + "</field>\n"

    #Randomly generate an exlcude element
    xml += makeFilterExclude()

    #Generate a random date between 1980 and now
    thisYear = datetime.datetime.now().year
    date = datetime.datetime(random.randint(1980,thisYear), random.randint(1,12), random.randint(1,28))

    #Generate either a min and max range of dates or an exact date
    isRange = random.choice([True, False])
    if( isRange ):
        minDate = date
        maxDate = datetime.datetime(date.year+1, random.randint(1,12), random.randint(1,28))
        xml += "\t\t<min>" + minDate.strftime("%Y-%m-%d") + "T" + minDate.strftime("%H:%M:%S") + "Z</min>\n"
        xml += "\t\t<max>" + maxDate.strftime("%Y-%m-%d") + "T" + maxDate.strftime("%H:%M:%S") + "Z</max>\n"
    else:
        xml += "\t\t<value>" + date.strftime("%Y-%m-%d") + "T" + date.strftime("%H:%M:%S")  + "Z</value>\n"

    xml += "\t</dateFilter>\n"

    return xml

#Generates a boolean filter
def makeBooleanFilter():
    xml = "\t<booleanFilter>\n"

    #Make a filter label
    xml += makeFilterLabel()

    #The list of date fields in the search index
    fields = ["isPublic", "isService", "isSpatial"]

    #Randomly select and create fields
    for n in range(random.randint(1,2)):
        xml += "\t\t<field>" + random.choice(fields) + "</field>\n"

    #Randomly generate an operator element
    xml += makeFilterOperator()

    #Randomly generate an exlcude element
    xml += makeFilterExclude()

    xml += "\t\t<value>" + random.choice(["true", "false"]) + "</value>\n"

    xml += "\t</booleanFilter>\n"

    return xml

def makeUIFilterOptions():
    xml = "\t\t<filterOptions>\n"

    xml += "\t\t\t<placeholder>" + makeRandomWords(random.randint(2,10)) + "</placeholder>\n"
    xml += "\t\t\t<icon>" + makeRandomIcon()  + "</icon>\n"
    xml += "\t\t\t<description>" + makeRandomWords(random.randint(10,30)) + "</description>\n"

    xml += "\t\t</filterOptions>\n"
    return xml

def makeUIFilter():
    xml = "\t<filter>\n"

    xml += makeFilterLabel()

    #randomly create fields
    for n in range(random.randint(1,2)):
        xml += "\t\t<field>" + random.choice(STR_FIELD_POOL) + "</field>\n"

    xml += makeFilterOperator()

    #Add an matchSubstring element
    #matchSubstring = ["\t\t<matchSubstring>true</matchSubstring>\n", "\t\t<matchSubstring>false</matchSubstring>\n", ""]
    #xml += random.choice(matchSubstring)

    xml += makeUIFilterOptions()

    xml += "\t</filter>\n"

    return xml

def makeUIDateFilter():
    xml = "\t<dateFilter>\n"

    xml += makeFilterLabel()

    #The list of date fields in the search index
    fields = ["updateDate", "beginDate", "dateModified", "datePublished",
              "dateUploaded", "endDate", "pubDate", "replicaVerifiedDate"]

    #Randomly select a field
    xml += "\t\t<field>" + random.choice(fields) + "</field>\n"

    thisYear = datetime.datetime.now().year
    rangeMin = datetime.datetime(random.randint(1980,thisYear), random.randint(1,12), random.randint(1,28))
    rangeMax = datetime.datetime(rangeMin.year + random.randint(1,30), random.randint(1,12), random.randint(1,28))

    if random.choice([True,False]):
        xml += "\t\t<rangeMin>" + rangeMin.strftime("%Y-%m-%d") + "T" + rangeMin.strftime("%H:%M:%S") + "Z</rangeMin>\n"

    if random.choice([True,False]):
        xml += "\t\t<rangeMax>" + rangeMax.strftime("%Y-%m-%d") + "T" + rangeMax.strftime("%H:%M:%S") + "Z</rangeMax>\n"

    xml += makeUIFilterOptions()

    xml += "\t</dateFilter>\n"

    return xml

def makeUIBooleanFilter():
    xml = "\t<booleanFilter>\n"

    xml += makeFilterLabel()

    #The list of date fields in the search index
    fields = ["updateDate", "beginDate", "dateModified", "datePublished",
              "dateUploaded", "endDate", "pubDate", "replicaVerifiedDate"]

    #Randomly select a field
    for n in range(random.randint(1,3)):
        xml += "\t\t<field>" + random.choice(fields) + "</field>\n"

    xml += makeUIFilterOptions()

    xml += "\t</booleanFilter>\n"

    return xml

def makeUIToggleFilter():
    xml = "\t<toggleFilter>\n"

    xml += makeFilterLabel()

    #randomly create fields
    for n in range(random.randint(1,2)):
        xml += "\t\t<field>" + random.choice(STR_FIELD_POOL) + "</field>\n"

    xml += makeUIFilterOptions()

    xml += "\t\t<trueValue>" + makeRandomWord() + "</trueValue>\n"

    if random.choice([True,False]):
        xml += "\t\t<trueLabel>" + makeRandomWords(random.randint(1,5)) + "</trueLabel>\n"

    if random.choice([True,False]):
        xml += "\t\t<falseValue>" + makeRandomWord() + "</falseValue>\n"

    if random.choice([True,False]):
        xml += "\t\t<falseLabel>" + makeRandomWords(random.randint(1,5)) + "</falseLabel>\n"

    xml += "\t</toggleFilter>\n"

    return xml

def makeUIChoiceFilter():
    xml = "\t<choiceFilter>\n"

    xml += makeFilterLabel()

    #randomly create fields
    for n in range(random.randint(1,2)):
        xml += "\t\t<field>" + random.choice(STR_FIELD_POOL) + "</field>\n"

    xml += makeUIFilterOptions()

    for n in range(random.randint(2,50)):
        xml += "\t\t<choice>\n"
        xml += "\t\t\t<label>" + makeRandomWords(random.randint(1,8)) + "</label>\n"
        xml += "\t\t\t<value>" + makeRandomWords(random.randint(1,8)) + "</value>\n"
        xml += "\t\t</choice>\n"

    #Add a chooseMultiple element, or skip it
    xml += random.choice(["\t\t<chooseMultiple>true</chooseMultiple>\n", "\t\t<chooseMultiple>false</chooseMultiple>\n", ""])

    xml += "\t</choiceFilter>\n"

    return xml

#Randomly selects an image id from the list of image ids
def getRandomImage():
    #Get the list of image ids from the local imageIds file
    idFile = open("imageIds.txt", "r")
    ids = idFile.readlines()
    idFile.close()

    return ids[random.randint(0, len(ids) - 1)].rstrip()

def makeRandomImageType():
    return "\t<identifier>" + getRandomImage() + "</identifier>\n\t<label>" + makeRandomWords(random.randint(1,10)) + "</label>\n"

def makeSection():
    xml = "<section>\n"

    xml += "\t<label>" + makeRandomWords(random.randint(1,5)) + "</label>\n"

    booleanChoices = [True, False]

    #Make a title
    if random.choice(booleanChoices):
        xml += "\t<title>" + makeRandomWords(random.randint(1,10)) + "</title>\n"

    #Make an intro
    if random.choice(booleanChoices):
        xml += "\t<introduction>" + makeRandomWords(random.randint(10,100)) + "</introduction>\n"

    #Make an image
    if random.choice(booleanChoices):
        xml += "\t<image>" + makeRandomImageType() + "</image>\n"

    #Make some content
    xml += "\t<content><markdown>" + makeRandomWords(random.randint(100,600)) + "\n</markdown></content>\n"

    xml += "</section>\n"
    return xml

def makeEMLParty():
    xml = "<associatedParty>\n"

    xml += "\t<individualName>\n"

    if random.choice([True,False]):
        xml += "\t\t<salutation>" + random.choice(["Dr.", "Mr.", "Ms."]) + "</salutation>\n"

    for n in range(random.randint(0,2)):
        xml += "\t\t<givenName>" + makeRandomWord() + "</givenName>\n"

    xml += "\t\t<surName>" + makeRandomWord() + "</surName>\n"
    xml += "\t</individualName>\n"

    if random.choice([True,False]):
        xml += "\t<organizationName>" + makeRandomWords(random.randint(1,6)) + "</organizationName>\n"

    if random.choice([True,False]):
        xml += "\t<positionName>" + makeRandomWords(random.randint(1,4)) + "</positionName>\n"

    if random.choice([True,False]):
        xml += "\t<address>\n"
        xml += "\t\t<deliveryPoint>" + makeRandomWords(random.randint(1,3)) + "</deliveryPoint>\n"
        xml += "\t\t<city>" + makeRandomWord() + "</city>\n"
        xml += "\t\t<administrativeArea>" + makeRandomWord() + "</administrativeArea>\n"
        xml += "\t\t<postalCode>" + str(random.randint(10000, 99999)) + "</postalCode>\n"
        xml += "\t\t<country>" + makeRandomWord() + "</country>\n"
        xml += "\t</address>\n"

    if random.choice([True,False]):
        xml += "\t<phone>" + str(random.randint(100,999)) + "-" + str(random.randint(100,999)) + "-" + str(random.randint(1000,9999)) + "</phone>\n"

    if random.choice([True,False]):
        xml += "\t<electronicMailAddress>" + makeRandomWord() + "@fakeemail.fake</electronicMailAddress>\n"

    if random.choice([True,False]):
        xml += "\t<onlineUrl>https://" + makeRandomWord() + ".fake</onlineUrl>\n"

    xml += "\t<role>" + makeRandomWords(random.randint(1,4)) + "</role>\n"

    xml += "</associatedParty>\n"

    return xml

def makeFilterGroup():
    xml = "<filterGroup>\n"

    xml += "\t<label>" + makeRandomWords(random.randint(1,3)) + "</label>\n"
    xml += "\t<description>" + makeRandomWords(random.randint(3,20))  + "</description>\n"
    xml += "\t<icon>" + makeRandomIcon()  + "</icon>\n"

    filterTypes = ["filter", "dateFilter", "booleanFilter", "toggleFilter"]

    for n in range(random.randint(1,9)):
        chosenType = random.choice(filterTypes)

        if chosenType == "filter":
            xml += makeUIFilter()
        elif chosenType == "dateFilter":
            xml += makeUIDateFilter()
        elif chosenType == "booleanFilter":
            xml += makeUIBooleanFilter()
        elif chosenType == "toggleFilter":
            xml += makeUIToggleFilter()

    xml += "</filterGroup>\n"

    return xml

def makePortalDocument():
    createRandomPools()

    #Start the portal node
    xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<por:portal xmlns:por=\"https://purl.dataone.org/portals-1.0.0\">\n"

    label = makeRandomWord() + str(random.randint(10, 99))
    name = makeRandomWords(random.randint(5, 10))
    print("Label: " + label)
    print("Title: " + name)

    #Randomize the label
    xml += "<label>" + label + "</label>\n"

    #Randomize the name
    xml += "<name>" + name + "</name>\n"

    #Randomize the description
    xml += "<description>" + makeRandomWords(random.randint(50, 120)) + "</description>\n"

    #Randomize the definition
    xml += "<definition>\n"
    xml += makeRandomFilters()
    xml += "</definition>\n"

    #Randomize a logo
    xml += "<logo>\n"
    xml += makeRandomImageType()
    xml += "</logo>\n"

    #Randomly create sections
    for n in range(random.randint(0,10)):
        xml += makeSection()

    #Randomize associated parties
    for n in range(random.randint(0,30)):
        xml += makeEMLParty()

    #Randomize the acknowledgments
    if random.choice([True,False]):
        xml += "<acknowledgments><markdown>" + makeRandomWords(random.randint(50, 400)) + "\n</markdown></acknowledgments>\n"

    #Randomize a logo
    for n in range(random.randint(0,15)):
        xml += "<acknowledgmentsLogo>\n"
        xml += makeRandomImageType()
        xml += "</acknowledgmentsLogo>\n"

    #Randomize filterGroups
    for n in range(random.randint(0,10)):
        xml += makeFilterGroup()

    #TODO: Make awards
    #TODO: Make datasource filter
    #TODO: Make user filter
    #TODO: Make geohash filter
    #TODO: Add images to associatedParty onlineUrls
    #TODO: Add support for isPartOf filter

    #Close the portal node
    xml += "</por:portal>"

    f = open("portal.xml", "w")
    f.write(xml)
    f.close()

makePortalDocument()
