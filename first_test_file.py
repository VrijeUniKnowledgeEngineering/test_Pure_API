import requests
import json
import pprint
from rdflib import Graph, RDF, Namespace, Literal, URIRef
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF


data = {"data" : "24.3"}
data_json = json.dumps(data)
# Accept: application/json

headers = {'Accept': 'application/json'}

#data from PURE system
resp_person = requests.get("https://research.vu.nl/ws/api/59/persons?q=harmelen&apiKey=1aecc9b3-0b58-4e00-b757-c1a8026cbbfd",  headers=headers)
response_person = resp_person.json()

# data_person = response_person               #data from scopus

#data from JSON file
with open('data_pure_author.json') as json_file:
    data_json_file = json.load(json_file)

data_person = data_json_file       #data from JSON file

# with open('data_pure_author.json', 'w') as outfile:
#     json.dump(response_person, outfile)

# pprint.pprint(data_person)



# def serialize(filename):
#     g.serialize(destination=filename, format='turtle')
#     print("File is saved")

def save(filename):
    with open(filename, 'a+') as f:
        g.serialize(destination=filename, format='turtle')
        print("File is saved")


def load(filename):
    with open(filename, 'r') as f:
        g.load(f, format='turtle')


# Initialize author with uri
URI = "https://krr.cs.vu.nl/"

def transformToRDF(strURI):

    if strURI[0:] == '_':
        strURI = strURI[0:].replace("_", "")  # delete     (does not work)

    strURI = strURI.replace(":", "") #delete :
    strURI = strURI.replace("/", "")  #delete /
    strURI = strURI.replace(" ", "_") #replace the space into
    strURI = strURI.replace(",", "") #delete ,
    strURI = strURI.replace("'", "") #delete single quote       (does not work)
    strURI = strURI.replace("''", "") #delete dubble quote      (does not work)
    strURI = strURI.replace("""""", "") #delete dubble quote    (does not work)
    strURI = strURI.replace("(", "") #delete (
    strURI = strURI.replace(")", "") #delete )
    strURI = strURI.replace("-", "_") #delete -
    strURI = strURI.replace("?", "") #delete ?
    strURI = strURI.replace(".", "_") #delete .
    strURI = strURI.replace(";", "") #delete ;
    strURI = strURI.replace("©", "") #delete ©
    strURI = strURI.replace("%", "") #delete %
    strURI = strURI.replace("=", "") #delete =
    strURI = strURI.replace("!", "") #delete !
    strURI = strURI.replace("[", "") #delete .
    strURI = strURI.replace("]", "") #delete .
    strURI = strURI.replace("é", "e") #delete .

    return URIRef(URI + strURI) #create URI


#Details author
title = data_person['items'][0]['titles'][0]['value']
firstName = data_person['items'][0]['name']['firstName']
lastName = data_person['items'][0]['name']['lastName']
scopusID = data_person['items'][0]['ids'][1]['value']
pureID = data_person['items'][0]['uuid']


lastName = lastName.replace(" ","_")
firstName = firstName.replace(" ","_")
title = title.replace(" ","_")
pureID = str(pureID)



print(scopusID)
# print(pureID)



#============================
# RESEARCH OUTPUT
#============================
# resp_publications = requests.get('https://research.vu.nl/ws/api/59/persons/'+ pureID +'/research-outputs?apiKey=1aecc9b3-0b58-4e00-b757-c1a8026cbbfd',  headers=headers)
# response_publications = resp_publications.json()
# data_publications = response_publications               #data from Pure
#

#data from JSON file
with open('data_pure_publications.json') as json_file:
    data_json_file = json.load(json_file)
data_publications = data_json_file       #data from JSON file

# with open('data_pure_publications.json', 'w') as outfile:
#     json.dump(response_publications, outfile)
pprint.pprint(data_publications)


if resp_person.status_code != 200:
    # This means something went wrong.
    print('life is hard')
    raise ApiError('GET /tasks/ {}'.format(resp_person.status_code))


totalPublications = data_publications['count']
publicationsItems = data_publications['items']

publications = []
print(len(publicationsItems))
for i in range(len(publicationsItems)):

    publications.append({
        'title': publicationsItems[i]['title'],
        # 'issn': publicationsItems['journalAssociation']['issn'],
        # 'pages': publicationsItems['pages'],
        # 'fileURL': publicationsItems[i]['electronicVersions'][0]['file']['fileURL'],
        'doi': publicationsItems[0]['electronicVersions'][1]['doi']

    })


#==============================
# Extra Information from PURE
#==============================
# #IDS
print(data_person['items'][0]['externalableInfo']['secondarySources']) #Same ID a Scopus ID
print(data_person['items'][0]['ids']) #Second element [1] is the same as the scopus ID
id_person = data_person['items'][0]['uuid'] #Person-ID of Pure?

#     #Name Variance
print(data_person['items'][0]['nameVariants'])
# #Name Title
print(data_person['items'][0]['titles'])
#
# #E-mail
print(data_person['items'][0]['staffOrganisationAssociations'][0]['emails'][0]['value'])


#Keywords workfield?
print(data_person['items'][0]['keywordGroups'][0]['keywords'])



# #=========================
# # Publications
# #========================
resp_publications = requests.get("https://research.vu.nl/ws/api/59/persons/" + id_person +"/research-outputs?apiKey=1aecc9b3-0b58-4e00-b757-c1a8026cbbfd",  headers=headers)


resp_publications = requests.get("https://research.vu.nl/ws/api/59/persons/b36edb65-746c-46be-9ecb-e532eb23c24e/research-outputs?apiKey=1aecc9b3-0b58-4e00-b757-c1a8026cbbfd",  headers=headers)
if resp_publications.status_code != 200:
    # This means something went wrong.
    print('life is hard')
    raise ApiError('GET /tasks/ {}'.format(resp_publications.status_code))

response_publications = resp_publications.json()
pprint.pprint(response_publications)


print (response_publications['count'])

print (response_publications['items'])


#=======================
# RDF Lib
#=======================
g = Graph()

EX = Namespace('https://krr.cs.vu.nl/')
g.bind('krr', EX)

hasScopusID = transformToRDF('hasScopusID')
hasPureID = transformToRDF('hasPureID')


title = transformToRDF(title)
firstName = transformToRDF(firstName)
lastName = transformToRDF(lastName)
scopusID = transformToRDF(scopusID)
pureID = transformToRDF(pureID)

g.add( (lastName, RDF.type, FOAF.Person) )
g.add( (lastName, FOAF.title, title) )
g.add( (lastName, FOAF.firstName, firstName) )
g.add( (lastName, FOAF.lastName, lastName) )
g.add( (lastName, hasScopusID, scopusID) )
g.add( (lastName, hasPureID, pureID) )


save("data.ttl")
