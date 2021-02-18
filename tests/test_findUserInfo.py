import pytest
import json
import requests_mock
import io
import pandas
from pandas.testing import assert_frame_equal

from src import handle_files, process_data

with open('tests/mocks/searchResponse.json', 'r') as myfile:
    data=myfile.read()
    
search_results = json.loads(data)       

def test_findUserInfo(requests_mock, mockOAuthSession, getTestConfig):
    requests_mock.register_uri('POST', 'https://128807.share.worldcat.org/idaas/scim/v2/Users/.search', status_code=200, json=search_results)
    item_file = "barcode\n2200998"
    csv_read = handle_files.loadCSV(item_file) 
    getTestConfig.update({"oauth-session": mockOAuthSession})
    result = process_data.findUsersInfo(getTestConfig, csv_read)
    assert type(result) is pandas.DataFrame
    #assert result.columns == ["barcode", "sourceSystem", "principalId", "sourceSystemId", "status"]
    final_result = pandas.DataFrame(data={"barcode": [2200998], "sourceSystem": [None], "principalId":['1671151d-ac48-4b4d-a204-c858c3bf5d86'], "sourceSystemId":[None], "status": ['success']})
    assert_frame_equal(result, final_result)