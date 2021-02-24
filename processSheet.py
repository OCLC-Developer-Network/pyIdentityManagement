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
        parser.add_argument('--operation', required=True, choices=['getUsers', 'createUsers', 'deleteUsers', 'findUsers', 'addCorrelationInfoToUsers', 'findUserCorrelationInfo'], help='Operation to run: getUsers, createUsers, deleteUsers, findUsers, addCorrelationInfoToUsers')    
        parser.add_argument('--outputDir', required=True, help='Directory to save output to')        
    
        args = parser.parse_args()
        return args
    except SystemExit:
        raise        
def validateOperation(csv_read, operation):
    if operation == "getUsers":
        if 'principalId' not in csv_read.columns.values.tolist():
            sys.exit("CSV does not contain column principalId")
    elif operation == "createUsers":
        requiredFields = ['name']
        if not all(item in csv_read.columns.values.tolist() for item in requiredFields): 
            sys.exit("CSV does not contain column name")
    elif operation == "deleteUsers":  
        if 'principalId' not in csv_read.columns.values.tolist():              
            sys.exit("CSV does not contain column principalId")       
    elif operation == "findUsers":
        if 'barcode' not in csv_read.columns.values.tolist():
            sys.exit("CSV does not contain column barcode") 
    elif operation == "findUserCorrelationInfo":
        requiredFields = ['barcode', 'sourceSystem']
        if not all(item in csv_read.columns.values.tolist() for item in requiredFields):   
            sys.exit("CSV does not contain columns barcode and sourceSystem")                    
    elif operation == "addCorrelationInfoToUsers":
        requiredFields = ['principalId', 'sourceSystem', 'sourceSystemId']
        if not all(item in csv_read.columns.values.tolist() for item in requiredFields):
            sys.exit("CSV does not contain columns principalId, sourceSystem, sourceSystemId")
    return operation
   
def process(args):
    item_file = handle_files.readFileFromLocal(args.itemFile) 
    
    operation = args.operation
    output_dir = args.outputDir

    csv_read = handle_files.loadCSV(item_file)     
    process_function = validateOperation(csv_read, operation)
    
    # get a token
    scope = ['SCIM']
    try:
        oauth_session = make_requests.createOAuthSession(config, scope)
    
        config.update({"oauth-session": oauth_session})
        processConfig = config

        csv_read = process_data.process_function(processConfig, csv_read)        
        return handle_files.saveFileLocal(csv_read, output_dir)

    except BaseException as err:
        result = str(err)
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
  