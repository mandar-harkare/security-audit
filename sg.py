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
ws = wb.worksheets[0]
data = []

# c1: account
# c2: region
# c3: sg
# c4: rule = Inbound / Outbound
# c5: cidr
# c6: ec2


for region in exclude_regions:
    print ("Excluding region: " + region)
    aws_regions.remove(region)

for region in aws_regions:
    
    boto3.client('ec2', region_name=region)
    print (account_id)
    print("=============START for " + region + " ==========================")
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_security_groups()
    for sg in response['SecurityGroups']:
        print(sg['GroupName'])
        sg_associations = ec2.describe_network_interfaces(
            Filters=[
                {
                    'Name': 'group-id',
                    'Values': [sg['GroupId']]
                },
            ]
        )
        # print(bool(sg_associations['NetworkInterfaces']))
        for ib_rule in sg['IpPermissions']:
            if ib_rule['IpRanges']:
                for cidr in ib_rule['IpRanges']:
                    if ('FromPort' in ib_rule and ib_rule['FromPort'] == 22 and cidr['CidrIp'] != '10.0.0.0/8') or (cidr['CidrIp'] == '0.0.0.0/0' and 'FromPort' in ib_rule and (ib_rule['FromPort'] != 80 and ib_rule['FromPort'] != 443)) or not sg_associations['NetworkInterfaces']:
                        row = []
                        row.append(account_id)
                        row.append(region)
                        row.append(sg['GroupName'] + " (" + sg['GroupId'] + ")")
                        row.append('Inbound')
                        if 'FromPort' in ib_rule:
                            row.append(ib_rule['FromPort'])
                        else:
                            row.append('')
                        
                        row.append(cidr['CidrIp'])
                        row.append(bool(sg_associations['NetworkInterfaces']))
                        data.append(row)
                        ws.append(row)
            elif not ib_rule['UserIdGroupPairs']:
                row = []
                row.append(account_id)
                row.append(region)
                row.append(sg['GroupName'] + " (" + sg['GroupId'] + ")")
                row.append('Inbound')
                row.append('')
                                
                row.append('[]')
                row.append(bool(sg_associations['NetworkInterfaces']))
                data.append(row)
                ws.append(row)
    print("=============END==========================")

wb.save("test.xlsx")
