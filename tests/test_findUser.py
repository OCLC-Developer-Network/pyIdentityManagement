import pytest
import json
import requests_mock
import pandas
from src import make_requests

with open('tests/mocks/searchResponse.json', 'r') as myfile:
    data=myfile.read()

# parse file
searchMock = json.loads(data)

def test_findUser(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    requests_mock.register_uri('POST', 'https://128807.share.worldcat.org/idaas/scim/v2/Users/.search', status_code=200, json=searchMock)
    user = make_requests.findUser(getTestConfig, '2200998');
    assert type(user) is pandas.core.series.Series
    assert user[0] == '1671151d-ac48-4b4d-a204-c858c3bf5d86'
    assert user[1] == ''
    assert user[2] == 'success'
    
def test_findUserCorrelationData(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    requests_mock.register_uri('POST', 'https://128807.share.worldcat.org/idaas/scim/v2/Users/.search', status_code=200, json=searchMock)
    user = make_requests.findUser(getTestConfig, '2200998', 'urn:mace:oclc:idm:ocpsb');
    assert type(user) is pandas.core.series.Series
    assert user[0] == '1671151d-ac48-4b4d-a204-c858c3bf5d86'
    assert user[1] == '069cc81f-395d-4272-86f2-99b54d8fbc29'   
    assert user[2] == 'success'
    
def test_findUserCorrelationDataNoMatches(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    requests_mock.register_uri('POST', 'https://128807.share.worldcat.org/idaas/scim/v2/Users/.search', status_code=200, json=searchMock)
    user = make_requests.findUser(getTestConfig, '2200998', 'urn:mace:oclc:idm:ocp');
    assert type(user) is pandas.core.series.Series
    assert user[0] == '1671151d-ac48-4b4d-a204-c858c3bf5d86'
    assert user[1] == ''   
    assert user[2] == 'success'        
    
    