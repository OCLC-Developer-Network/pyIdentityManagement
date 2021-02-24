import pytest
import json
import requests_mock
import pandas
from src import make_requests

with open('tests/mocks/readUserResponse.json', 'r') as myfile:
    data=myfile.read()
    
userMock = json.loads(data)
    
with open('tests/mocks/addCorrelationInfoResponse.json', 'r') as myfile:
    data=myfile.read()

# parse file
userUpdateMock = json.loads(data)

def test_addCorrelationInfo(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    principalId = '1671151d-ac48-4b4d-a204-c858c3bf5d86'
    sourceSystem = 'https://some-organization-idm.org/SAML'
    sourceSystemId = 'smithk'    
    requests_mock.register_uri('GET', 'https://128807.share.worldcat.org/idaas/scim/v2/Users/' + principalId, status_code=200, json=userMock)
    requests_mock.register_uri('PUT', 'https://128807.share.worldcat.org/idaas/scim/v2/Users/' + principalId, status_code=200, json=userUpdateMock)
    
    user = make_requests.getUser(getTestConfig, principalId);
    user = make_requests.addCorrelationInfo(getTestConfig, principalId, sourceSystem, sourceSystemId);
    assert type(user) is pandas.core.series.Series
    assert user[0] == '1671151d-ac48-4b4d-a204-c858c3bf5d86'
    assert user[1] == 'https://some-organization-idm.org/SAML'
    assert user[2] == 'smithk'
    assert user[3] == 'success'
    
    