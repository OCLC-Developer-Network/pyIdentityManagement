import boto3
import yaml
import json
import pandas as pd  
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
import requests
import os
from io import StringIO
import time
from ebcli.lib.utils import save_file_from_url
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

credentials = boto3.Session().get_credentials()

s3 = boto3.client('s3')

# load key/secret config info
# read a configuration file
with open("config.yml", 'r') as stream:
    config = yaml.load(stream)
    
serviceURL = config.get('IDM_service_url')    
# get a token
scope = ['SCIM']
auth = HTTPBasicAuth(config.get('key'), config.get('secret'))
client = BackendApplicationClient(client_id=config.get('key'), scope=scope)
oauth_session = OAuth2Session(client=client)

try:
    token = oauth_session.fetch_token(token_url=config.get('token_url'), auth=auth)
except BaseException as err:
    print(err)
    
def findUser(identifier):
    filter = 'barcode eq "' + identifier + '"'
    search_body = {
                "schemas": ["urn:ietf:params:scim:api:messages:2.0:SearchRequest"],
                "filter": filter       
        }
    try:
        r = oauth_session.post(serviceURL + "/.search", data= search_body,headers={"Accept":"application/json"})
        r.raise_for_status
        try:
            result = r.json()
            principalId = result['Resources'][0]['urn:mace:oclc.org:eidm:schema:persona:persona:20180305']['oclcPPID']
            status = "success"
        except json.decoder.JSONDecodeError:
            principalId = ""
            status = "failed"
    except requests.exceptions.HTTPError as err:
        principalId = ""
        status = "failed"
    return pd.Series([principalId, status])

def getUser(principalId):
    try:
        r = oauth_session.post(serviceURL + "/" + principalId, headers={"Accept":"application/json"})
        r.raise_for_status
        try:
            result = r.json()
            first_name = result['name']['givenName']            
            last_name = result['name']['familyName']
            barcode = result['urn:mace:oclc.org:eidm:schema:persona:wmscircpatroninfo:20180101']['circulationInfo']['barcode']
            expiration_date = ['urn:mace:oclc.org:eidm:schema:persona:persona:20180305']['oclcExpirationDate']
            status = "success"
        except json.decoder.JSONDecodeError:
            status = "failed"
    except requests.exceptions.HTTPError as err:
        status = "failed"
    return pd.Series([first_name, last_name, barcode, expiration_date, status])

def deleteUser(principalId):
    try:
        r = oauth_session.delete(serviceURL + "/" + principalId, headers={"Accept":"application/json"})
        r.raise_for_status
        try:
            status = "success"
        except json.decoder.JSONDecodeError:
            status = "failed"
    except requests.exceptions.HTTPError as err:
        status = "failed"
    return pd.Series([principalId, status])

def addUser(fields):
    input = "";
    
    try:
        r = oauth_session.post(serviceURL + "/", data=input, headers={"Accept": "application/scim+json"})
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

def saveFile(bucket, filename, csv_dict):
    csv_buffer = StringIO()    
    csv_dict.to_csv(csv_buffer, sep="|", index=False)

    try:
        write_response = s3.put_object(Bucket=bucket, key= filename, Body=csv_buffer.getvalue())
        return "success"
    except ClientError as err:
        error_message = "Operation complete - output write failed"
        if err.response['Error']['Code']:
            error_message += err.response['Error']['Code']
        return error_message     

def getUsers(event, context):  
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    # need to get the file from S3
    response = s3.get_object(Bucket=bucket, Key=key)  
    item_file = response['Body'].read().decode('utf-8')
    csv_read = pd.read_csv(item_file, index_col=False)
    csv_read[['first_name', 'last_name', 'barcode', 'expiration_date', 'status']] = csv_read.apply (lambda row: getUser(row['principalId']), axis=1)    
         
    return saveFile(bucket, key + "_updated", csv_read)

def createUsers(event, context):  
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    # need to get the file from S3
    response = s3.get_object(Bucket=bucket, Key=key)  
    item_file = response['Body'].read().decode('utf-8')
    csv_read = pd.read_csv(item_file, index_col=False)
    csv_read[['principalId', 'status']] = csv_read.apply (lambda row: createUser(row), axis=1)    
     
    return saveFile(bucket, key + "_updated", csv_read)

def deleteUsers(event, context):  
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    # need to get the file from S3
    response = s3.get_object(Bucket=bucket, Key=key)  
    item_file = response['Body'].read().decode('utf-8')
    csv_read = pd.read_csv(item_file, index_col=False)
    csv_read[['principalId', 'status']] = csv_read.apply (lambda row: deleteUser(row['principalID']), axis=1)    
     
    return saveFile(bucket, key + "_updated", csv_read)

def findUsers(event, context):  
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    # need to get the file from S3
    response = s3.get_object(Bucket=bucket, Key=key)  
    item_file = response['Body'].read().decode('utf-8')
    csv_read = pd.read_csv(item_file, index_col=False)
    csv_read[['principalId', 'status']] = csv_read.apply (lambda row: findUser(row['barcode']), axis=1)    
     
    return saveFile(bucket, key + "_updated", csv_read)
    
  