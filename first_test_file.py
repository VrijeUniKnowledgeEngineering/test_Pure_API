import requests
import json
import pprint

data = {"data" : "24.3"}
data_json = json.dumps(data)
# Accept: application/json

headers = {'Accept': 'application/json'}

resp_person = requests.get("https://research.vu.nl/ws/api/59/persons?q=harmelen&apiKey=1aecc9b3-0b58-4e00-b757-c1a8026cbbfd",  headers=headers)
response_person = resp_person.json()
# pprint.pprint(response_person)

#Details author
title = response_person['items'][0]['titles'][0]['value']
firstName = response_person['items'][0]['name']['firstName']
lastName = response_person['items'][0]['name']['lastName']
scopusID = response_person['items'][0]['ids'][1]['value']
pureID = response_person['items'][0]['uuid']

lastName = lastName.replace(" ","_")
firstName = firstName.replace(" ","_")
title = title.replace(" ","_")
pureID = str(pureID)

print(scopusID)
print(pureID)
resp_research_outputs = requests.get('https://research.vu.nl/ws/api/59/persons/'+ pureID +'/research-outputs?apiKey=1aecc9b3-0b58-4e00-b757-c1a8026cbbfd',  headers=headers)

if resp_person.status_code != 200:
    # This means something went wrong.
    print('life is hard')
    raise ApiError('GET /tasks/ {}'.format(resp_person.status_code))

response_research_outputs = resp_research_outputs.json()
# pprint.pprint(response_research_outputs)

totalPublications = response_research_outputs['count']
publicationsItems = response_research_outputs['items']

# print publicationsItems
print(len(publicationsItems))
pprint.pprint(publicationsItems)

#no.1
print(publicationsItems[0]['title'])
print(publicationsItems[0]['electronicVersions'][1]['doi'])

print(len(publicationsItems))
for i in range(len(publicationsItems)):

    print (i)
    print (publicationsItems[i]['title'])
    print (publicationsItems[i]['electronicVersions'][0]['file']['fileURL'])

# [{u'created': u'2017-02-05T12:55:32.326+0000', u'creator': u'root', u'accessType': [{u'uri': u'/dk/atira/pure/core/openaccesspermission/open', u'value': u'Open'}], u'visibleOnPortalDate': u'2017-02-05T12:55:32.326+0000', u'file': {u'mimeType': u'application/pdf', u'digestAlgorithm': u'SHA1', u'fileName': u'swj588 0.pdf', u'fileURL': u'https://research.vu.nl/ws/files/666163/swj588%200.pdf', u'digest': u'9C9F042A242D74C01FC69DD44DFA57EA27070FC0', u'size': 307701}, u'versionType': [{u'uri': u'/dk/atira/pure/publication/electronicversion/versiontype/publishersversion', u'value': u'Final published version'}], u'id': 666162},
#  {u'accessType': [{u'uri': u'/dk/atira/pure/core/openaccesspermission/unknown', u'value': u'Unknown'}], u'doi': u'http://dx.doi.org/10.3233/SW-140158', u'visibleOnPortalDate': u'2017-02-05T12:55:32.326+0000', u'id': 666164, u'versionType': [{u'uri': u'/dk/atira/pure/publication/electronicversion/versiontype/publishersversion', u'value': u'Final published version'}]}]



#==============================
# Extra Information from PURE
#==============================
# #IDS
# print(response_person['items'][0]['externalableInfo']['secondarySources']) #Same ID a Scopus ID
# print(response_person['items'][0]['ids']) #Second element [1] is the same as the scopus ID
# id_person = response_person['items'][0]['uuid'] #Person-ID of Pure?
#
#     #Name Variance
# print(response_person['items'][0]['nameVariants'])
# #Name Title
# print(response_person['items'][0]['titles'])
#
# #E-mail
# print(response_person['items'][0]['staffOrganisationAssociations'][0]['emails'][0]['value'])


#Keywords workfield?
# print(response_person['items'][0]['keywordGroups'][0]['keywords'])



# #=========================
# # Publications
# #========================
# resp_publications = requests.get("https://research.vu.nl/ws/api/59/persons/" + id_person +"/research-outputs?apiKey=1aecc9b3-0b58-4e00-b757-c1a8026cbbfd",  headers=headers)
#
#
# resp_publications = requests.get("https://research.vu.nl/ws/api/59/persons/b36edb65-746c-46be-9ecb-e532eb23c24e/research-outputs?apiKey=1aecc9b3-0b58-4e00-b757-c1a8026cbbfd",  headers=headers)
# if resp_publications.status_code != 200:
#     # This means something went wrong.
#     print('life is hard')
#     raise ApiError('GET /tasks/ {}'.format(resp_publications.status_code))
#
# response_publications = resp_publications.json()
# pprint.pprint(response_publications)
#
#
# print (response_publications['count'])
#
# print (response_publications['items'])



#=======================
#RDFLIB
#=======================

# from rdflib import Graph, RDF, Namespace, Literal, URIRef

# g = Graph()
#
# EX = Namespace('http://example.com/KE4KE/')
# g.bind('ex', EX)

# rdfLastName = URIRef("http://example.com/KE4KE/" + scopusID)


# from rdflib import URIRef, BNode, Literal
#
# krr_url = 'https://krr.cs.vu.nl/'
#
# title = URIRef(krr_url + title)
# firstName = URIRef(krr_url + firstName)
# lastName = URIRef(krr_url + lastName)
# scopusID = URIRef(krr_url + scopusID)
# pureID = URIRef(krr_url + pureID)
#
# hasScopusID = URIRef("https://krr.cs.vu.nl/hasScopusID")
# hasPureID = URIRef("https://krr.cs.vu.nl/hasPureID")
#
# from rdflib.namespace import RDF, FOAF
#
#
# # RDF.type = rdflib.term.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
#
# # FOAF.knows = rdflib.term.URIRef(u'http://xmlns.com/foaf/0.1/knows')
#
#
# from rdflib import Graph
# g = Graph()
#
# g.add( (lastName, RDF.type, FOAF.Person) )
# g.add( (lastName, FOAF.title, title) )
# g.add( (lastName, FOAF.firstName, firstName) )
# g.add( (lastName, FOAF.lastName, lastName) )
# g.add( (lastName, hasScopusID, scopusID) )
# g.add( (lastName, hasPureID, pureID) )
#
#
# # print (g.serialize(format='turtle'))
#
#
# file = open("data.ttl", mode="w")
#
# def serialize(filename):
#     g.serialize(destination=filename, format='turtle')
#     print("File is saved")
#
# def save(filename):
#     with open(filename, 'w') as f:
#         g.serialize(f, format='turtle')
#
#
# def load(filename):
#     with open(filename, 'r') as f:
#         g.load(f, format='turtle')
#
#
# serialize('data.ttl')
