import boto3
from boto3.session import Session
from openpyxl import load_workbook

sts = boto3.client('sts')
exclude_regions = [
    'af-south-1',
    'ap-east-1',
    'ap-southeast-3',
    'eu-south-1',
    'me-south-1'
]
s = Session()
aws_regions = s.get_available_regions('dynamodb')
ec2 = boto3.client('ec2', region_name='us-east-1')
account_id = sts.get_caller_identity()["Account"]
wb = load_workbook("test.xlsx")
# Select First Worksheet
ws = wb.worksheets[1]
data = []

# c1: account
# c2: region
# c3: instance name / id
# c4: ami id
# c5: ami name


for region in exclude_regions:
    print ("Excluding region: " + region)
    aws_regions.remove(region)

for region in aws_regions:
    
    boto3.client('ec2', region_name=region)
    print (account_id)
    print("=============START for " + region + " ==========================")
    
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instances()
    
    for item in response['Reservations']:
        for instance in item['Instances']:
            key_name = instance['KeyName'] if 'KeyName' in instance else '' 
            print(key_name)

            row = []
            row.append(account_id)
            row.append(region)
            row.append(key_name + " (" + instance['InstanceId'] + ")")
            row.append(instance['ImageId'])
            img_res = ec2.describe_images(
                ImageIds=[
                    instance['ImageId']
                ]
            )
            if img_res['Images']:
                row.append(img_res['Images'][0]['Name'])
                row.append(img_res['Images'][0]['Public'])
            data.append(row)
            ws.append(row)
    print("=============END==========================")

wb.save("test.xlsx")
