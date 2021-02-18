import pytest
import json
import requests_mock
import io
import pandas
from pandas.testing import assert_frame_equal

from src import handle_files, process_data

def test_deleteUserInfo(requests_mock, mockOAuthSession, getTestConfig):
    requests_mock.register_uri('DELETE', 'https://128807.share.worldcat.org/idaas/scim/v2/Users/1671151d-ac48-4b4d-a204-c858c3bf5d86', status_code=200)
    item_file = "principalId\n1671151d-ac48-4b4d-a204-c858c3bf5d86"
    csv_read = handle_files.loadCSV(item_file) 
    getTestConfig.update({"oauth-session": mockOAuthSession})
    result = process_data.deleteUserInfo(getTestConfig, csv_read)
    assert type(result) is pandas.DataFrame
    #assert result.columns == ["principalId", "status"]
    final_result = pandas.DataFrame(data={"principalId": ['1671151d-ac48-4b4d-a204-c858c3bf5d86'], "status": ['success']})    
    assert_frame_equal(result, final_result) 