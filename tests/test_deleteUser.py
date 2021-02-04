import pytest
import json
import requests_mock
import pandas
from src import make_requests

def test_deleteUser(requests_mock, mockOAuthSession, getTestConfig):
    getTestConfig.update({'oauth-session': mockOAuthSession})
    requests_mock.register_uri('DELETE', 'https://128807.share.worldcat.org/idaas/scim/v2/Users/1671151d-ac48-4b4d-a204-c858c3bf5d86', status_code=200)
    user = make_requests.deleteUser(getTestConfig, '1671151d-ac48-4b4d-a204-c858c3bf5d86');
    assert type(user) is pandas.core.series.Series
    assert user[0] == '1671151d-ac48-4b4d-a204-c858c3bf5d86'
    assert user[1] == 'success'
    
    