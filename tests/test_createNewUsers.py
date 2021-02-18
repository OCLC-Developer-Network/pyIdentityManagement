import pytest
import json
import requests_mock
import io
import pandas
from pandas.testing import assert_frame_equal

from src import handle_files, process_data

with open('tests/mocks/createUserResponse.json', 'r') as myfile:
    data=myfile.read()

userMock = json.loads(data)

def test_createNewUsers(requests_mock, mockOAuthSession, getTestConfig):
    requests_mock.register_uri('POST', 'https://128807.share.worldcat.org/idaas/scim/v2/Users/', status_code=200, json=userMock)
    item_file = "givenName,familyName,streetAddress,locality,region,postalCode,institution,barcode,borrowerCategory,homeBranch,expiration_date\nStacy,Smith (test),1142 Jasmine Ridge Court,Bangor,ME,04915,128807,330912,ADULT,129479,2018-09-07T00:00:00Z"
    csv_read = handle_files.loadCSV(item_file) 
    getTestConfig.update({"oauth-session": mockOAuthSession})
    result = process_data.createNewUsers(getTestConfig, csv_read)
    assert type(result) is pandas.DataFrame
    #assert result.columns == ["oclcNumber", "mergedOCNs", "status"]
    final_result = pandas.DataFrame(data={"givenName": ["Stacy"], "familyName": ["Smith (test)"], "streetAddress": ["1142 Jasmine Ridge Court"], "locality": ["Bangor"], "region": ["ME"], "postalCode": ["04915"], "institution": ["128807"], "barcode": ["330912"], "borrowerCategory":["ADULT"],"homeBranch":["129479"], "expiration_date": ["2018-09-07T00:00:00Z"] , "principalId": ['3ac7346f-3b61-4aa9-bcea-e0179f0a3c77'], "status": ['success']})
    assert_frame_equal(result, final_result)
    