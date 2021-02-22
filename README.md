# Triggered Lambda

Custom application looks for new files in particular folders an S3 bucket and interacts with the WorldShare Identity Management API based on the data in the delimited file

## Installing Locally

### Step 1: Clone the repository
Clone this repository

```bash
$ git clone {url}
```
or download directly from GitHub.

Change into the application directory

### Step 2: Setup Virtual Environment

```bash
$ python -m venv venv
$ . venv/bin/activate
```

### Step 3: Install python dependencies

```bash
$ pip install -r requirements.txt
```

### Step 4: Run local tests

```bash
$ python -m pytest
```
### Step 5: Run code locally
```bash
usage: processSheet.py [-h] --itemFile ITEMFILE --operation
                  {getUsers,createUsers,deleteUsers,findUsers,addCorrelationInfoToUsers,findUserCorrelationInfo}
                  --outputDir OUTPUTDIR

optional arguments:
  -h, --help            show this help message and exit
  --itemFile ITEMFILE   File you want to process
  --operation {getUsers,createUsers,deleteUsers,findUsers,addCorrelationInfoToUsers,findUserCorrelationInfo}
                        Operation to run: getUsers,
                        createUsers, deleteUsers,
                        addCorrelationInfoToUsers,
                        findUserCorrelationInfo
  --outputDir OUTPUTDIR
                        Directory to save output to                                                                       
                        
```

#### Example
```bash
$ python processSheet.py --itemFile samples/barcodes.csv --operation findUsers --outputDir samples/principalIDs.csv
```

## Running in AWS Lambda

### Step 1: AWS Setup

1. Install AWS Commandline tools
- https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
I reccomend using pip.
2. Create an AWS user in IAM console. Give it appropriate permissions. Copy the key and secret for this user to use in the CLI. 
3. Configure the commandline tools - https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

- Make sure you add 
-- key/secret
-- region
    
### Step 2: Create an S3 Bucket for the files
1. Use the AWS Console to create a bucket. Note your bucket name!!!
2. Create folder idm_events/
3. Add a sample csv file of user identifier data
4. Add a sample csv file of user barcode data


### Step 3: Test application
1. Alter s3_event.json to point to your bucket and your sample txt file.

2. Use serverless to test locally

```bash
serverless invoke local --function findUsers --path s3-findUsers-event.json
```

3. Alter s3-getUsers-event.json to point to your bucket and your sample csv file.

4. Use serverless to test locally

```bash
serverless invoke local --function getUsers --path s3-getUsers-event.json
```

## Installing in AWS Lambda

1. Download and setup the application, see Installing locally
2. Deploy the code using serverless

```bash
$ serverless deploy
```
