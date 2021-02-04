import pytest
import json
import requests_mock
import pandas
from src import make_requests

with open('tests/mocks/readUserResponse.json', 'r') as myfile:
    data=myfile.read()

# parse file
userMock = json.loads(data)

def test_getUser(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    requests_mock.register_uri('GET', 'https://128807.share.worldcat.org/idaas/scim/v2/Users/1671151d-ac48-4b4d-a204-c858c3bf5d86', status_code=200, json=userMock)
    user = make_requests.getUser(getTestConfig, '1671151d-ac48-4b4d-a204-c858c3bf5d86');
    assert type(user) is pandas.core.series.Series
    assert user[0] == 'Karen'
    assert user[1] == 'Coombs'
    assert user[2] == '2200998'
    assert user[3] == '2018-09-07T00:00:00Z'
    assert user[4] == 'success'
    
    