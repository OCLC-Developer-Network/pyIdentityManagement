import pytest
import json
import requests_mock
import pandas
import handler

with open('tests/mocks/createUserResponse.json', 'r') as myfile:
    data=myfile.read()

# parse file
userMock = json.loads(data)

def test_getUser(requests_mock):
    requests_mock.register_uri('POST', 'https://128807.share.worldcat.org/idaas/scim/v2/Users/', status_code=200, json=userMock)
    fields = {
            givenName: "Stacy", 
            familyName: "Smith (test)",
            email: "smiths@library.org",
            streetAddress: "1142 Jasmine Ridge Court",
            locality: "Bangor",
            region: "ME",
            postalCode: "04915",
            institution: 128807
            }
    
    user = handler.createUser(fields);
    assert type(user) is pandas.core.series.Series
    assert user[0] == '3ac7346f-3b61-4aa9-bcea-e0179f0a3c77'
    assert user[1] == 'success'
    
    