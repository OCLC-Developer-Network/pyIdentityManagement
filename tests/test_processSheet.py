import pytest
import sys
import io
import processSheet
from src import handle_files, process_data, make_requests

def testProcessArgs(mocker):
    # mocker doesn't seem to be setting the system arguments
    mocker.patch('sys.argv', ["", "--itemFile", "samples/barcodes.csv", "--operation", "findUsers", "--outputDir", "samples/results"])    
    args = processSheet.processArgs()
    assert args.itemFile == "samples/barcodes.csv"
    assert args.operation == "findUsers"
    assert args.outputDir == "samples/results"                   

def testProcessWrongOperation(mocker, capfd):
    mocker.patch('sys.argv', ["", "--itemFile", "samples/barcodes.csv", "--operation", "junkrequest", "--outputDir", "samples/results"])    
    with pytest.raises(SystemExit):
        args = processSheet.processArgs()
    captured = capfd.readouterr()
    assert "usage:  [-h] --itemFile ITEMFILE --operation" in captured.err
    assert "{getUsers,createUsers,deleteUsers,findUsers,addCorrelationInfoToUsers,findUserCorrelationInfo}" in captured.err
    assert "--outputDir OUTPUTDIR" in captured.err
    assert "error: argument --operation: invalid choice: 'junkrequest' (choose from 'getUsers', 'createUsers', 'deleteUsers', 'findUsers', 'addCorrelationInfoToUsers', 'findUserCorrelationInfo')" in captured.err  
     
def testProcessMissingArgumentItemFile(mocker, capfd):
    mocker.patch('sys.argv', ["", "--operation", "findUsers", "--outputDir", "samples/results"])    
    with pytest.raises(SystemExit):
        args = processSheet.processArgs()
    captured = capfd.readouterr()
    assert "usage:  [-h] --itemFile ITEMFILE --operation" in captured.err
    assert "{getUsers,createUsers,deleteUsers,findUsers,addCorrelationInfoToUsers,findUserCorrelationInfo}" in captured.err
    assert "--outputDir OUTPUTDIR" in captured.err
    assert "error: the following arguments are required: --itemFile" in captured.err         
         
def testProcessMissingArgumentOperation(mocker, capfd):
    mocker.patch('sys.argv', ["", "--itemFile", "samples/oclc_numbers.csv", "--outputDir", "samples/results"])    
    with pytest.raises(SystemExit):
        args = processSheet.processArgs()
    captured = capfd.readouterr()
    assert "usage:  [-h] --itemFile ITEMFILE --operation" in captured.err
    assert "{getUsers,createUsers,deleteUsers,findUsers,addCorrelationInfoToUsers,findUserCorrelationInfo}" in captured.err
    assert "--outputDir OUTPUTDIR" in captured.err
    assert "error: the following arguments are required: --operation" in captured.err     
       
def testProcessMissingArgumentOutputDir(mocker, capfd):
    mocker.patch('sys.argv', ["", "--itemFile", "samples/barcodes.csv", "--operation", "findUsers"])    
    with pytest.raises(SystemExit):
        args = processSheet.processArgs() 
    captured = capfd.readouterr()
    assert "usage:  [-h] --itemFile ITEMFILE --operation" in captured.err 
    assert "{getUsers,createUsers,deleteUsers,findUsers,addCorrelationInfoToUsers,findUserCorrelationInfo}" in captured.err
    assert "--outputDir OUTPUTDIR" in captured.err
    assert "error: the following arguments are required: --outputDir" in captured.err

def testOperationGetUsersMissingColumn():
    item_file = "barcode\n2200998"
    csv_read = handle_files.loadCSV(item_file)
    with pytest.raises(SystemExit):
        processSheet.validateOperation(csv_read, 'getUsers')
        assert "CSV does not contain column principalId" in SystemExit.err
             
def testOperationCreateUsersMissingColumn():
    item_file = "barcode\n2200998"
    csv_read = handle_files.loadCSV(item_file)
    with pytest.raises(SystemExit):
        processSheet.validateOperation(csv_read, 'createUsers')
        assert "CSV does not contain column name" in SystemExit.err
        
def testOperationDeleteUsersMissingColumn():
    item_file = "barcode\n2200998"
    csv_read = handle_files.loadCSV(item_file)
    with pytest.raises(SystemExit):
        processSheet.validateOperation(csv_read, 'deleteUsers') 
        assert "CSV does not contain column principalId" in SystemExit.err

def testOperationFindUsersMissingColumn():
    item_file = "principalId\n1671151d-ac48-4b4d-a204-c858c3bf5d86"
    csv_read = handle_files.loadCSV(item_file)
    with pytest.raises(SystemExit):
        processSheet.validateOperation(csv_read, 'findUsers')
        assert "CSV does not contain column barcode" in SystemExit.err 

def testOperationFindUserCorrelationInfoMissingBarcodeColumn():
    item_file = "sourceSystem\n2200998"
    csv_read = handle_files.loadCSV(item_file)
    with pytest.raises(SystemExit):
        processSheet.validateOperation(csv_read, 'findUserCorrelationInfo')
        assert "CSV does not contain columns barcode and sourceSystem" in SystemExit.err 

def testOperationFindUserCorrelationInfoMissingSourceSystemColumn():
    item_file = "barcode\n2200998"
    csv_read = handle_files.loadCSV(item_file)
    with pytest.raises(SystemExit):
        processSheet.validateOperation(csv_read, 'findUserCorrelationInfo')
        assert "CSV does not contain columns barcode and sourceSystem" in SystemExit.err  
        
def testOperationAddCorrelationInfoToUsersMissingPrincipalIdColumn():
    item_file = "barcode\n2200998"
    csv_read = handle_files.loadCSV(item_file)
    with pytest.raises(SystemExit):
        processSheet.validateOperation(csv_read, 'addCorrelationInfoToUsers')
        assert "CSV does not contain columns principalId, sourceSystem, sourceSystemId" in SystemExit.err    

def testOperationAddCorrelationInfoToUsersSourceSystemColumn():
    item_file = "principalId,sourceSystemId\n1671151d-ac48-4b4d-a204-c858c3bf5d86,foo"
    csv_read = handle_files.loadCSV(item_file)
    with pytest.raises(SystemExit):
        processSheet.validateOperation(csv_read, 'addCorrelationInfoToUsers')  
        assert "CSV does not contain columns principalId, sourceSystem, sourceSystemId" in SystemExit.err        

def testOperationAddCorrelationInfoToUsersSourceSystemIdColumn():
    item_file = "principalId,sourceSystem\n1671151d-ac48-4b4d-a204-c858c3bf5d86,foo"
    csv_read = handle_files.loadCSV(item_file)
    with pytest.raises(SystemExit):
        processSheet.validateOperation(csv_read, 'addCorrelationInfoToUsers')
        assert "CSV does not contain columns principalId, sourceSystem, sourceSystemId" in SystemExit.err                                                        