import pytest
import json
import handler

# with open('tests/mocks/createUserInput.json', 'r') as myfile:
#     data=myfile.read()
# 
# # parse file
# userMock = json.loads(data)

def test_createUserJSON():
    user_fields = {
            "givenName": "Stacy", 
            "familyName": "Smith (test)",
            "email": "smiths@library.org",
            "streetAddress": "1142 Jasmine Ridge Court",
            "locality": "Bangor",
            "region": "ME",
            "postalCode": "04915",
            "institution": 128807
            }
    
    userJSON = handler.createUserJSON(user_fields);
    assert type(userJSON) is dict
    assert userJSON.get("name").get("givenName") == "Stacy"
    assert userJSON.get("name").get("familyName") == "Smith (test)"
    assert userJSON.get("emails")[0].get("value") == "smiths@library.org"
    assert userJSON.get("addresses")[0].get("streetAddress") == "1142 Jasmine Ridge Court"
    assert userJSON.get("addresses")[0].get("locality") == "Bangor"
    assert userJSON.get("addresses")[0].get("region") == "ME"
    assert userJSON.get("addresses")[0].get("postalCode") == "04915"
    assert userJSON.get("urn:mace:oclc.org:eidm:schema:persona:persona:20180305").get("institutionId") == 128807
    
    