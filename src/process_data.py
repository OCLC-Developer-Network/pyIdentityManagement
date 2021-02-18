from src import handle_files
from src import make_requests

import pandas as pd

def retrieveUsers(processConfig, csv_read):
    csv_read[['first_name', 'last_name', 'barcode', 'expiration_date', 'status']] = csv_read.apply (lambda row: make_requests.getUser(processConfig, row['principalId']), axis=1)    
    return csv_read 

def createNewUsers(processConfig, csv_read):
    csv_read[['principalId', 'status']] = csv_read.apply (lambda row: make_requests.createUser(processConfig, row), axis=1)    
    return csv_read  

def deleteUserInfo(processConfig, csv_read):      
    csv_read[['principalId', 'status']] = csv_read.apply (lambda row: make_requests.deleteUser(processConfig, row['principalId']), axis=1)
    return csv_read    

def findUsersInfo(processConfig, csv_read):  
    csv_read[['barcode', 'sourceSystem', 'principalId', 'sourceSystemId', 'status']] = csv_read.apply (lambda row: make_requests.findUser(processConfig, row['barcode']), axis=1)    
    return csv_read

def findUserCorrelationInfo(processConfig, csv_read):  
    csv_read[['barcode', 'sourceSystem', 'principalId', 'sourceSystemId', 'status']] = csv_read.apply (lambda row: make_requests.findUser(processConfig, row['barcode'], row['sourceSystem']), axis=1)    
    return csv_read    

def addUserCorrelationInfo(processConfig, csv_read):  
    csv_read[['principalId', 'status']] = csv_read.apply (lambda row: make_requests.addCorrelationInfo(processConfig, row['principalId'], row['sourceSystem'], row['sourceSystemId']), axis=1)    
    return csv_read    
        
