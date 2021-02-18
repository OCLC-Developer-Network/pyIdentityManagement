import pytest
import json
import requests_mock
import io
import pandas
from pandas.testing import assert_frame_equal

from src import handle_files, process_data

from src import process_data

with open('tests/mocks/readUserResponse.json', 'r') as myfile:
    data=myfile.read()

# parse file
userMock = json.loads(data)

def test_retrieveUsers(requests_mock, mockOAuthSession, getTestConfig):
    requests_mock.register_uri('GET', 'https://128807.share.worldcat.org/idaas/scim/v2/Users/1671151d-ac48-4b4d-a204-c858c3bf5d86', status_code=200, json=userMock)
    item_file = "principalId\n1671151d-ac48-4b4d-a204-c858c3bf5d86"
    csv_read = handle_files.loadCSV(item_file) 
    getTestConfig.update({"oauth-session": mockOAuthSession})
    result = process_data.retrieveUsers(getTestConfig, csv_read)
    assert type(result) is pandas.DataFrame
    #assert result.columns == ["principalId", "first_name", "last_name", "barcode", "expiration_date", "status"]
    final_result = pandas.DataFrame(data={"principalId": ['1671151d-ac48-4b4d-a204-c858c3bf5d86'], "first_name":["Karen"], "last_name": ["Coombs"], "barcode":["2200998"], "expiration_date":["2018-09-07T00:00:00Z"], "status": ['success']})    
    assert_frame_equal(result, final_result)