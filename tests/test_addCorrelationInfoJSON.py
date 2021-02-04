import pytest
import json
from src import make_requests

with open('tests/mocks/readUserResponse.json', 'r') as myfile:
    data=myfile.read()
    
user = json.loads(data)

def test_addCorrelationInfoJSON():
    sourceSystem = 'https://some-organization-idm.org/SAML'
    sourceSystemId = 'smithk'
    
    updatedUserJSON =  make_requests.addCorrelationInfoJSON(user, sourceSystem, sourceSystemId);
    assert type(updatedUserJSON) is dict
    assert updatedUserJSON.get("name").get("givenName") == "Karen"
    assert updatedUserJSON.get("name").get("familyName") == "Coombs"
    assert updatedUserJSON.get("emails")[0].get("value") == "coombsk@oclc.org"
    assert updatedUserJSON.get("addresses")[0].get("streetAddress") == "6565 Kilgour Pl"
    assert updatedUserJSON.get("addresses")[0].get("locality") == "Dublin"
    assert updatedUserJSON.get("addresses")[0].get("region") == "OH"
    assert updatedUserJSON.get("addresses")[0].get("postalCode") == "43017"
    assert updatedUserJSON.get("urn:mace:oclc.org:eidm:schema:persona:persona:20180305").get("institutionId") == "128807"
    #assert updatedUserJSON.get("urn:mace:oclc.org:eidm:schema:persona:correlationinfo:20180101").get("correlationInfo") is list
    assert updatedUserJSON.get("urn:mace:oclc.org:eidm:schema:persona:correlationinfo:20180101").get("correlationInfo")[1].get("idAtSource") == "smithk"
    

    