import requests

mnBaseUrl = "https://arcticdata.io"
mnMetacatContext = "/metacat"
collectionLabel = "DBO"
cnBaseUrl = "https://cn.dataone.org"
maxCollectionSize = 5000;

mnQueryAPI = "/d1/mn/v2/query/solr/"
cnQueryAPI = "/cn/v2/query/solr/"

#Get the collection query from the MN
query = "?q=label:" + collectionLabel + " AND -obsoletedBy:*&rows=1&fl=collectionQuery&wt=json"
r = requests.get(mnBaseUrl + mnMetacatContext + mnQueryAPI + query)
results = r.json()
collectionQuery = results["response"]["docs"][0]["collectionQuery"]

#Query for the collection on the MN
query = "?q=" + collectionQuery + "&rows=" + str(maxCollectionSize) + "&fl=id&wt=json"
r = requests.get(mnBaseUrl + mnMetacatContext + mnQueryAPI + query)
mnResults = r.json()

#Query for the collection on the CN
query = "?q=" + collectionQuery + "&rows=" + str(maxCollectionSize) + "&fl=id&wt=json"
r = requests.get(cnBaseUrl + cnQueryAPI + query)
cnResults = r.json()

# Get the number of results found in each collection
numFoundMN = mnResults["response"]["numFound"]
numFoundCN = cnResults["response"]["numFound"]
print("Num found on MN: " + str(numFoundMN))
print("Num found on CN: " + str(numFoundCN))

#If the number of results are different, find the difference in pids
mnIds = []
cnIds = []
uniqueToCN = []
uniqueToMN = []

if numFoundMN != numFoundCN:
    for doc in mnResults["response"]["docs"]:
        mnIds.append(doc["id"])

    for doc in cnResults["response"]["docs"]:
        cnIds.append(doc["id"])

    for id in mnIds:
        try:
            index = cnIds.index(id)
        except:
            uniqueToMN.append(id)

    for id in cnIds:
        try:
            index = mnIds.index(id)
        except:
            uniqueToCN.append(id)

print("\IDs in the MN collection that are NOT in the CN collection: ")
print("------------------------------------------------------------")
print(uniqueToMN)
print("\nIDs in the CN collection that are NOT in the MN collection: ")
print("------------------------------------------------------------")
print(uniqueToCN)
