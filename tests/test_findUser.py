import pytest
import json
import requests_mock
import pandas
import handler

with open('tests/mocks/searchResponse.json', 'r') as myfile:
    data=myfile.read()

# parse file
searchMock = json.loads(data)

def test_findUser(requests_mock):
    requests_mock.register_uri('POST', 'https://128807.share.worldcat.org/idaas/scim/v2/Users/.search', status_code=200, json=searchMock)
    user = handler.findUser('2200998');
    assert type(user) is pandas.core.series.Series
    assert user[0] == '1671151d-ac48-4b4d-a204-c858c3bf5d86'
    assert user[1] == 'success'
    
    