import yaml
import os
from src import handle_files, process_data, make_requests
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# load key/secret config info
# read a configuration file
with open("config.yml", 'r') as stream:
    config = yaml.safe_load(stream)
     
# get a token
scope = ['SCIM']
oauth_session = make_requests.createOAuthSession(config, scope)

processConfig = config.update({"oauth-session": oauth_session}) 

def getUsers(event, context):      
    item_file = handle_files.readFilesFromBucket(event)
    csv_read = handle_files.loadCSV(item_file)
    csv_read = process_data.retrieveUsers(processConfig, csv_read)
    handle_files.saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_updated", csv_read)             

def createUsers(event, context):  
    item_file = handle_files.readFilesFromBucket(event)
    csv_read = handle_files.loadCSV(item_file)
    csv_read = process_data.createNewUsers(processConfig, csv_read)
    handle_files.saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_updated", csv_read)     

def deleteUsers(event, context):  
    item_file = handle_files.readFilesFromBucket(event)
    csv_read = handle_files.loadCSV(item_file)
    csv_read = process_data.deleteUserInfo(processConfig, csv_read)
    handle_files.saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_updated", csv_read)         

def findUsers(event, context):  
    item_file = handle_files.readFilesFromBucket(event)
    csv_read = handle_files.loadCSV(item_file)
    csv_read = process_data.findUsersInfo(processConfig, csv_read)
    handle_files.saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_updated", csv_read)

def addCorrelationInfoToUsers(event, context):
    item_file = handle_files.readFilesFromBucket(event)
    csv_read = handle_files.loadCSV(item_file)
    csv_read = process_data.addCorrelationInfo(processConfig, csv_read)
    handle_files.saveFileToBucket(fileInfo['bucket'], fileInfo['key'] + "_updated", csv_read)    
            