from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
import pandas as pd  
import json
import requests
from io import StringIO

def createOAuthSession(config, scope):    
    auth = HTTPBasicAuth(config.get('key'), config.get('secret'))
    client = BackendApplicationClient(client_id=config.get('key'), scope=scope)
    oauth_session = OAuth2Session(client=client)
    try:
        token = oauth_session.fetch_token(token_url=config.get('token_url'), auth=auth)
        return oauth_session
    except BaseException as err:
        return err

def findUser(config, identifier, sourceSystemName=None):
    oauth_session = config.get('oauth-session')
    filter = 'barcode eq "' + str(identifier) + '"'
    search_body = {
                "schemas": ["urn:ietf:params:scim:api:messages:2.0:SearchRequest"],
                "filter": filter       
        }
    try:
        r = oauth_session.post(config.get('scim_service_url') + "/.search", data= search_body,headers={"Accept":"application/json"})
        r.raise_for_status
        try:
            result = r.json()
            principalId = result['Resources'][0]['urn:mace:oclc.org:eidm:schema:persona:persona:20180305']['oclcPPID']
            if sourceSystemName:
                correlationIds = result['Resources'][0]['urn:mace:oclc.org:eidm:schema:persona:correlationinfo:20180101']['correlationInfo']
                specifiedSourceName = [x for x in correlationIds if x['sourceSystem'] == sourceSystemName]
                if len(specifiedSourceName) > 0 : 
                    sourceSystemId = specifiedSourceName[0]['idAtSource']
                else:
                    sourceSystemId = None
            else:
                sourceSystemId = None       
            status = "success"
        except json.decoder.JSONDecodeError:
            principalId = None
            sourceSystemId = None
            status = "failed"
    except requests.exceptions.HTTPError as err:
        principalId = None
        status = "failed"
    return pd.Series([identifier, sourceSystemName, principalId, sourceSystemId, status])

def getUser(config, principalId):
    oauth_session = config.get('oauth-session')
    try:
        r = oauth_session.get(config.get('scim_service_url') + "/" + principalId, headers={"Accept":"application/json"})
        r.raise_for_status
        try:
            result = r.json()
            first_name = result['name']['givenName']            
            last_name = result['name']['familyName']
            barcode = result['urn:mace:oclc.org:eidm:schema:persona:wmscircpatroninfo:20180101']['circulationInfo']['barcode']
            expiration_date = result['urn:mace:oclc.org:eidm:schema:persona:persona:20180305']['oclcExpirationDate']
            status = "success"
        except json.decoder.JSONDecodeError:
            status = "failed"
    except requests.exceptions.HTTPError as err:
        status = "failed"
    return pd.Series([first_name, last_name, barcode, expiration_date, status])

def deleteUser(config, principalId):
    oauth_session = config.get('oauth-session')
    try:
        r = oauth_session.delete(config.get('scim_service_url') + "/" + principalId, headers={"Accept":"application/json"})
        r.raise_for_status
        try:
            status = "success"
        except json.decoder.JSONDecodeError:
            status = "failed"
    except requests.exceptions.HTTPError as err:
        status = "failed"
    return pd.Series([principalId, status])

def createUserJSON(user_fields):
        
    name = {
              "familyName": user_fields.get('familyName'),
              "givenName": user_fields.get('givenName'),
              "middleName": user_fields.get('middleName'),
              "honorificPrefix": user_fields.get('honorificPrefix'),
              "honorificSuffix": user_fields.get('honorificSuffix')
            }
    
    if user_fields.get('barcode') and user_fields.get('borrowerCategory') and user_fields.get('homeBranch'):
        
        circInfo = {
                        "barcode": user_fields.get('barcode'),
                        "borrowerCategory": user_fields.get('borrowerCategory'),
                        "homeBranch": user_fields.get('homeBranch')
                      }
    else:
        circInfo = {}
        
    jsonInput = {
        "schemas": [
              "urn:ietf:params:scim:schemas:core:2.0:User",
              "urn:mace:oclc.org:eidm:schema:persona:correlationinfo:20180101",
              "urn:mace:oclc.org:eidm:schema:persona:persona:20180305",
              "urn:mace:oclc.org:eidm:schema:persona:wmscircpatroninfo:20180101",
              "urn:mace:oclc.org:eidm:schema:persona:wsillinfo:20180101"
            ],
            "name": name,
            "emails": [
                  {
                    "value": user_fields.get('email'),
                    "type": "home",
                    "primary": True
                  }
                ],
            "addresses": [
              {
                "streetAddress": user_fields.get('streetAddress'),
                "locality": user_fields.get('locality'),
                "region": user_fields.get('region'),
                "postalCode": user_fields.get('postalCode'),
                "type": "home",
                "primary": False
              }
            ],
            "urn:mace:oclc.org:eidm:schema:persona:wmscircpatroninfo:20180101": {
                  "circulationInfo": circInfo                 
          },
          "urn:mace:oclc.org:eidm:schema:persona:persona:20180305": {
              "institutionId": user_fields.get('institution')
          }
      }
    
    return jsonInput

def addUser(config, user_fields):
    oauth_session = config.get('oauth-session')
    input = createUserJSON(user_fields);
    
    try:
        r = oauth_session.post(config.get('scim_service_url') + "/", data=input, headers={"Accept": "application/scim+json"})
        r.raise_for_status
        try:
            result = r.json()            
            principalId = result['urn:mace:oclc.org:eidm:schema:persona:persona:20180305']['oclcPPID']
            status = "success"
        except json.decoder.JSONDecodeError:
            principalId = ""
            status = "failed"
    except requests.exceptions.HTTPError as err:
        principalId = ""
        status = "failed"
    return pd.Series([principalId, status]) 

def addCorrelationInfo(config, principalId, sourceSystem, sourceSystemId):
    oauth_session = config.get('oauth-session')
    try:
        r = oauth_session.get(config.get('scim_service_url') + "/" + principalId, headers={"Accept":"application/json"})
        r.raise_for_status
        try:
            result = r.json()
            input = addCorrelationInfoJSON(result, sourceSystem, sourceSystemId)
            try:
                r = oauth_session.put(config.get('scim_service_url') + "/" + principalId, data=input, headers={"Accept": "application/scim+json"})
                r.raise_for_status
                try:
                    result = r.json()            
                    principalId = result['urn:mace:oclc.org:eidm:schema:persona:persona:20180305']['oclcPPID']
                    status = "success"
                except json.decoder.JSONDecodeError:
                    principalId = ""
                    status = "failed"
            except requests.exceptions.HTTPError as err:
                principalId = ""
                status = "failed"
        except json.decoder.JSONDecodeError:
            status = "failed"
    except requests.exceptions.HTTPError as err:
        status = "failed"        
    return pd.Series([principalId, status]) 

def addCorrelationInfoJSON(user, sourceSystem, sourceSystemId):
    user.get('urn:mace:oclc.org:eidm:schema:persona:correlationinfo:20180101').get('correlationInfo').append({"sourceSystem": sourceSystem, "idAtSource": sourceSystemId})
    
    return user