from src import handle_files
from src import make_requests

import pandas as pd

def retrieveUsers(processConfig, csv_read):
    csv_read[['first_name', 'last_name', 'barcode', 'expiration_date', 'status']] = csv_read.apply (lambda row: make_requests.getUser(row['principalId']), axis=1)    
    return csv_read 

def createNewUsers(processConfig, csv_read):
    csv_read[['principalId', 'status']] = csv_read.apply (lambda row: make_requests.createUser(row), axis=1)    
    return csv_read  

def deleteUserInfo(processConfig, csv_read):      
    csv_read[['principalId', 'status']] = csv_read.apply (lambda row: make_requests.deleteUser(row['principalID']), axis=1)
    return csv_read    

def findUsersInfo(processConfig, csv_read):  
    csv_read[['principalId', 'status']] = csv_read.apply (lambda row: make_requests.findUser(row['barcode']), axis=1)    
    return csv_read    

def addUserCorrelationInfo(processConfig, csv_read):  
    csv_read[['principalId', 'status']] = csv_read.apply (lambda row: make_requests.addCorrelationInfo(row['principalID'], row['sourceSystem'], row['sourceSystemID']), axis=1)    
    return csv_read    
        
