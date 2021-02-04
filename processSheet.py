## need to import the relevant files
import argparse
import yaml
from src import handle_files, process_data, make_requests
import sys
import string

with open("config.yml", 'r') as stream:
    config = yaml.safe_load(stream)
    
def processArgs():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--itemFile', required=True, help='File you want to process')
        parser.add_argument('--operation', required=True, choices=['getUsers', 'createUsers', 'deleteUsers', 'findUsers', 'addCorrelationInfoToUsers'], help='Operation to run: getUsers, createUsers, deleteUsers, findUsers, addCorrelationInfoToUsers')    
        parser.add_argument('--outputDir', required=True, help='Directory to save output to')        
    
        args = parser.parse_args()
    except SystemExit:
        raise
    
def process(args):
    item_file = handle_files.readFileFromLocal(args.itemFile) 
    
    operation = args.operation
    output_dir = args.outputDir
    
    # get a token
    scope = ['SCIM']
    try:
        oauth_session = make_requests.createOAuthSession(config, scope)
    
        config.update({"oauth-session": oauth_session})
        processConfig = config
        csv_read = handle_files.loadCSV(item_file) 
        
        if operation == "getUsers":
            csv_read = process_data.retrieveUsers(processConfig, csv_read)
        elif operation == "createUsers":
            csv_read = process_data.createNewUsers(processConfig, csv_read)    
        elif operation == "deleteUsers":                
            csv_read = process_data.deleteUserInfo(processConfig, csv_read)   
        elif operation == "findUsers":
            csv_read = process_data.findUsersInfo(processConfig, csv_read)
        elif operation == "addCorrelationInfoToUsers":
            csv_read = process_data.addCorrelationInfo(processConfig, csv_read)            
    
        return handle_files.saveFileLocal(csv_read, output_dir)

    except BaseException as err:
        result = 'no access token ' + str(err)
        return result   

if __name__ == '__processSheet__':
    try:
        args = processArgs()
        print(process(args))
    except SystemExit:
        print("Invalid Operation specified")
else:
    try:
        args = processArgs()
        print(process(args))
    except SystemExit:
        print("Invalid Operation specified")
  