import pytest
import json
import requests_mock
import io
import pandas
from pandas.testing import assert_frame_equal

from src import handle_files, process_data

with open('tests/mocks/readUserResponse.json', 'r') as myfile:
    data=myfile.read()
    
userMock = json.loads(data)

with open('tests/mocks/addCorrelationInfoResponse.json', 'r') as myfile:
    data=myfile.read()
    
userUpdateMock = json.loads(data) 

def test_addUserCorelationInfo(requests_mock, mockOAuthSession, getTestConfig):
    principalId = '1671151d-ac48-4b4d-a204-c858c3bf5d86'
    sourceSystem = 'https://some-organization-idm.org/SAML'
    sourceSystemId = 'smithk'
    
    requests_mock.register_uri('GET', 'https://128807.share.worldcat.org/idaas/scim/v2/Users/' + principalId, status_code=200, json=userMock)
    requests_mock.register_uri('PUT', 'https://128807.share.worldcat.org/idaas/scim/v2/Users/' + principalId, status_code=200, json=userUpdateMock)
    item_file = "principalId,sourceSystem,sourceSystemId\n" + principalId + "," + sourceSystem + "," + sourceSystemId
    csv_read = handle_files.loadCSV(item_file) 
    getTestConfig.update({"oauth-session": mockOAuthSession})
    result = process_data.addUserCorrelationInfo(getTestConfig, csv_read)
    assert type(result) is pandas.DataFrame
    #assert result.columns == [principalId", "sourceSystem", "sourceSystemId", "status"]
    final_result = pandas.DataFrame(data={"principalId": [principalId], "sourceSystem":[sourceSystem], "sourceSystemId":[sourceSystemId], "status": ['success']})
    assert_frame_equal(result, final_result)