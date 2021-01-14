# Creates a portal document with completely random content.
# Image and object identifiers used in the portal document are real ids on dev.nceas.ucsb.edu
# To run, call `python3 randomize-portal.py` and the resulting portal doc will be saved as `portal.xml`
# Author: Lauren Walker

import random
import string
import re
import datetime
import xml.dom.minidom as minidom

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

    #Get the list of query field names that use strings as values
    strFieldFile = open("str_fields.txt", "r")
    global STR_FIELD_POOL
    STR_FIELD_POOL = strFieldFile.read().splitlines()
    strFieldFile.close()

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
def makeRandomFilters(maxFilters=10):
    filtersXML = ""

    for n in range(random.randint(1,maxFilters)):
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
    return "<label>" + makeRandomWords(random.randint(1,3)) + "</label>"

def makeOperator():
    #Choose a random operator or skip one altogether
    operators = ["<operator>AND</operator>", "<operator>OR</operator>", ""]

    return random.choice(operators)

def makeFieldsOperator():
    #Choose a random operator or skip one altogether
    operators = ["<fieldsOperator>AND</fieldsOperator>", "<fieldsOperator>OR</fieldsOperator>", ""]

    return random.choice(operators)

def makeFilterExclude():
    #Add an exclude element
    exclude = ["<exclude>true</exclude>", "<exclude>false</exclude>", ""]
    return random.choice(exclude)

#Makes a text filter with random values
def makeTextFilter():

    xml = "<filter>"

    xml += makeFilterLabel()

    #randomly create fields
    for n in range(random.randint(1,3)):
        xml += "<field>" + random.choice(STR_FIELD_POOL) + "</field>"

    #create filter operator for the values
    xml += makeOperator()

    xml += makeFilterExclude()

    #Add an matchSubstring element
    matchSubstring = ["<matchSubstring>true</matchSubstring>", "<matchSubstring>false</matchSubstring>", ""]
    xml += random.choice(matchSubstring)

    #randomly create values
    for n in range(random.randint(1,5)):
        xml += "<value>" + makeRandomWords(random.randint(1,3)) + "</value>"

    #create filter operator for the fields
    xml += makeFieldsOperator()

    xml += "</filter>"

    return xml

#Generates an id filter
def makeIdFilter():
    xml = "<filter>"

    xml += makeFilterLabel()

    xml += "<field>id</field>"

    xml += makeFilterExclude()

    #Get the list of ids from the local ids file
    idFile = open("ids.txt", "r")
    ids = idFile.readlines()
    idFile.close()

    for n in range(random.randint(1,20)):
        xml += "<value>" + ids[random.randint(0, len(ids) - 1)].rstrip() + "</value>"

    xml += "</filter>"

    return xml

#Generates an date filter
def makeDateFilter():
    xml = "<dateFilter>"

    #Make a filter label
    xml += makeFilterLabel()

    #The list of date fields in the search index
    fields = ["updateDate", "beginDate", "dateModified", "datePublished",
              "dateUploaded", "endDate", "pubDate", "replicaVerifiedDate"]

    #Randomly select a field
    xml += "<field>" + random.choice(fields) + "</field>"

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
        xml += "<min>" + minDate.strftime("%Y-%m-%d") + "T" + minDate.strftime("%H:%M:%S") + "Z</min>"
        xml += "<max>" + maxDate.strftime("%Y-%m-%d") + "T" + maxDate.strftime("%H:%M:%S") + "Z</max>"
    else:
        xml += "<value>" + date.strftime("%Y-%m-%d") + "T" + date.strftime("%H:%M:%S")  + "Z</value>"

    xml += "</dateFilter>"

    return xml

#Generates a boolean filter
def makeBooleanFilter():
    xml = "<booleanFilter>"

    #Make a filter label
    xml += makeFilterLabel()

    #The list of date fields in the search index
    fields = ["isPublic", "isService", "isSpatial"]

    #Randomly select and create fields
    for n in range(random.randint(1,2)):
        xml += "<field>" + random.choice(fields) + "</field>"

    #Randomly generate an operator element
    xml += makeOperator()

    #Randomly generate an exlcude element
    xml += makeFilterExclude()

    xml += "<value>" + random.choice(["true", "false"]) + "</value>"

    xml += "</booleanFilter>"

    return xml

def makeUIFilterOptions():
    xml = "<filterOptions>"

    xml += "<placeholder>" + makeRandomWords(random.randint(2,10)) + "</placeholder>"
    xml += "<icon>" + makeRandomIcon()  + "</icon>"
    xml += "<description>" + makeRandomWords(random.randint(10,30)) + "</description>"

    xml += "</filterOptions>"
    return xml

def makeUIFilter():
    xml = "<filter>"

    xml += makeFilterLabel()

    #randomly create fields
    for n in range(random.randint(1,2)):
        xml += "<field>" + random.choice(STR_FIELD_POOL) + "</field>"

    xml += makeOperator()

    #Add an matchSubstring element
    #matchSubstring = ["<matchSubstring>true</matchSubstring>", "<matchSubstring>false</matchSubstring>", ""]
    #xml += random.choice(matchSubstring)

    xml += makeUIFilterOptions()

    xml += "</filter>"

    return xml

def makeUIDateFilter():
    xml = "<dateFilter>"

    xml += makeFilterLabel()

    #The list of date fields in the search index
    fields = ["updateDate", "beginDate", "dateModified", "datePublished",
              "dateUploaded", "endDate", "pubDate", "replicaVerifiedDate"]

    #Randomly select a field
    xml += "<field>" + random.choice(fields) + "</field>"

    thisYear = datetime.datetime.now().year
    rangeMin = datetime.datetime(random.randint(1980,thisYear), random.randint(1,12), random.randint(1,28))
    rangeMax = datetime.datetime(rangeMin.year + random.randint(1,30), random.randint(1,12), random.randint(1,28))

    if random.choice([True,False]):
        xml += "<rangeMin>" + rangeMin.strftime("%Y-%m-%d") + "T" + rangeMin.strftime("%H:%M:%S") + "Z</rangeMin>"

    if random.choice([True,False]):
        xml += "<rangeMax>" + rangeMax.strftime("%Y-%m-%d") + "T" + rangeMax.strftime("%H:%M:%S") + "Z</rangeMax>"

    xml += makeUIFilterOptions()

    xml += "</dateFilter>"

    return xml

def makeUIBooleanFilter():
    xml = "<booleanFilter>"

    xml += makeFilterLabel()

    #The list of date fields in the search index
    fields = ["isPublic", "isService", "isSpatial"]

    #Randomly select a field
    for n in range(random.randint(1,3)):
        xml += "<field>" + random.choice(fields) + "</field>"

    xml += makeUIFilterOptions()

    xml += "</booleanFilter>"

    return xml

def makeUIToggleFilter():
    xml = "<toggleFilter>"

    xml += makeFilterLabel()

    #randomly create fields
    for n in range(random.randint(1,2)):
        xml += "<field>" + random.choice(STR_FIELD_POOL) + "</field>"

    xml += makeUIFilterOptions()

    xml += "<trueValue>" + makeRandomWord() + "</trueValue>"

    if random.choice([True,False]):
        xml += "<trueLabel>" + makeRandomWords(random.randint(1,5)) + "</trueLabel>"

    if random.choice([True,False]):
        xml += "<falseValue>" + makeRandomWord() + "</falseValue>"

    if random.choice([True,False]):
        xml += "<falseLabel>" + makeRandomWords(random.randint(1,5)) + "</falseLabel>"

    xml += "</toggleFilter>"

    return xml

def makeUIChoiceFilter():
    xml = "<choiceFilter>"

    xml += makeFilterLabel()

    #randomly create fields
    for n in range(random.randint(1,2)):
        xml += "<field>" + random.choice(STR_FIELD_POOL) + "</field>"

    xml += makeUIFilterOptions()

    for n in range(random.randint(2,50)):
        xml += "<choice>"
        xml += "<label>" + makeRandomWords(random.randint(1,8)) + "</label>"
        xml += "<value>" + makeRandomWords(random.randint(1,8)) + "</value>"
        xml += "</choice>"

    #Add a chooseMultiple element, or skip it
    xml += random.choice(["<chooseMultiple>true</chooseMultiple>", "<chooseMultiple>false</chooseMultiple>", ""])

    xml += "</choiceFilter>"

    return xml

def makeFilterGroupType(maxLevels = 6, maxFilters = 6, maxFilterGroups = 4):

    xml = ""
    xml += makeRandomFilters(maxFilters = maxFilters)

    levels = random.randint(1,maxLevels)

    levels -= 1

    for n in range(random.randint(0,maxFilterGroups)):
        if levels > 0:
            xml += "<filterGroup>"
            xml += makeFilterGroupType(maxLevels=levels, maxFilters=4, maxFilterGroups=4)
            xml += "</filterGroup>"
    xml += makeOperator()
    xml += makeFilterExclude()

    return xml

#Randomly selects an image id from the list of image ids
def getRandomImage():
    #Get the list of image ids from the local imageIds file
    idFile = open("imageIds.txt", "r")
    ids = idFile.readlines()
    idFile.close()

    return ids[random.randint(0, len(ids) - 1)].rstrip()

def makeRandomImageType():
    return "<identifier>" + getRandomImage() + "</identifier><label>" + makeRandomWords(random.randint(1,10)) + "</label>"

def makeSection():
    xml = "<section>"

    xml += "<label>" + makeRandomWords(random.randint(1,5)) + "</label>"

    booleanChoices = [True, False]

    #Make a title
    if random.choice(booleanChoices):
        xml += "<title>" + makeRandomWords(random.randint(1,10)) + "</title>"

    #Make an intro
    if random.choice(booleanChoices):
        xml += "<introduction>" + makeRandomWords(random.randint(10,100)) + "</introduction>"

    #Make an image
    if random.choice(booleanChoices):
        xml += "<image>" + makeRandomImageType() + "</image>"

    #Make some content
    xml += "<content><markdown>" + makeRandomWords(random.randint(100,600)) + "</markdown></content>"

    xml += "</section>"
    return xml

def makeEMLParty():
    xml = "<associatedParty>"

    xml += "<individualName>"

    if random.choice([True,False]):
        xml += "<salutation>" + random.choice(["Dr.", "Mr.", "Ms."]) + "</salutation>"

    for n in range(random.randint(0,2)):
        xml += "<givenName>" + makeRandomWord() + "</givenName>"

    xml += "<surName>" + makeRandomWord() + "</surName>"
    xml += "</individualName>"

    if random.choice([True,False]):
        xml += "<organizationName>" + makeRandomWords(random.randint(1,6)) + "</organizationName>"

    if random.choice([True,False]):
        xml += "<positionName>" + makeRandomWords(random.randint(1,4)) + "</positionName>"

    if random.choice([True,False]):
        xml += "<address>"
        xml += "<deliveryPoint>" + makeRandomWords(random.randint(1,3)) + "</deliveryPoint>"
        xml += "<city>" + makeRandomWord() + "</city>"
        xml += "<administrativeArea>" + makeRandomWord() + "</administrativeArea>"
        xml += "<postalCode>" + str(random.randint(10000, 99999)) + "</postalCode>"
        xml += "<country>" + makeRandomWord() + "</country>"
        xml += "</address>"

    if random.choice([True,False]):
        xml += "<phone>" + str(random.randint(100,999)) + "-" + str(random.randint(100,999)) + "-" + str(random.randint(1000,9999)) + "</phone>"

    if random.choice([True,False]):
        xml += "<electronicMailAddress>" + makeRandomWord() + "@fakeemail.fake</electronicMailAddress>"

    if random.choice([True,False]):
        xml += "<onlineUrl>https://" + makeRandomWord() + ".fake</onlineUrl>"

    xml += "<role>" + makeRandomWords(random.randint(1,4)) + "</role>"

    xml += "</associatedParty>"

    return xml

def makeUIFilterGroup():
    xml = "<filterGroup>"

    xml += "<label>" + makeRandomWords(random.randint(1,3)) + "</label>"
    xml += "<description>" + makeRandomWords(random.randint(3,20))  + "</description>"
    xml += "<icon>" + makeRandomIcon()  + "</icon>"

    filterTypes = ["filter", "dateFilter", "booleanFilter", "toggleFilter", "choiceFilter"]

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
        elif chosenType == "choiceFilter":
            xml += makeUIChoiceFilter()

    xml += "</filterGroup>"

    return xml

def makePortalDocument():
    createRandomPools()

    #Start the portal node
    xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><por:portal xmlns:por=\"https://purl.dataone.org/portals-1.1.0\">"

    label = makeRandomWord() + str(random.randint(10, 99))
    name = makeRandomWords(random.randint(5, 10))
    print("Label: " + label)
    print("Title: " + name)

    #Randomize the label
    xml += "<label>" + label + "</label>"

    #Randomize the name
    xml += "<name>" + name + "</name>"

    #Randomize the description
    xml += "<description>" + makeRandomWords(random.randint(50, 120)) + "</description>"

    #Randomize the definition
    xml += "<definition>"
    xml += makeFilterGroupType()
    xml += "</definition>"

    #Randomize a logo
    xml += "<logo>"
    xml += makeRandomImageType()
    xml += "</logo>"

    #Randomly create sections
    for n in range(random.randint(0,10)):
        xml += makeSection()

    #Randomize associated parties
    for n in range(random.randint(0,30)):
        xml += makeEMLParty()

    #Randomize the acknowledgments
    if random.choice([True,False]):
        xml += "<acknowledgments><markdown>" + makeRandomWords(random.randint(50, 400)) + "</markdown></acknowledgments>"

    #Randomize a logo
    for n in range(random.randint(0,15)):
        xml += "<acknowledgmentsLogo>"
        xml += makeRandomImageType()
        xml += "</acknowledgmentsLogo>"

    #Randomize filterGroups
    for n in range(random.randint(0,10)):
        xml += makeUIFilterGroup()

    #TODO: Make awards
    #TODO: Make datasource filter
    #TODO: Make user filter
    #TODO: Make geohash filter
    #TODO: Add images to associatedParty onlineUrls
    #TODO: Add support for isPartOf filter

    #Close the portal node
    xml += "</por:portal>"
    dom = minidom.parseString(xml)
    prettyXML = dom.toprettyxml()

    f = open("portal.xml", "w")
    f.write(prettyXML)
    f.close()

makePortalDocument()
