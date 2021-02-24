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
        