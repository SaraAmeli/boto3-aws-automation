import boto3
import requests
import time
from itertools import combinations
from botocore.exceptions import ClientError

# --- Setup ---
session = boto3.session.Session()
region = session.region_name
ec2 = session.client('ec2', region_name=region)
rds = session.client('rds', region_name=region)

# --- Step 1: Get Available AZs ---
azs = ec2.describe_availability_zones(Filters=[{'Name': 'region-name', 'Values': [region]}])
az_list = [az['ZoneName'] for az in azs['AvailabilityZones'] if az['State'] == 'available']
print(f"✅ Available AZs: {az_list}")

# --- Step 2: Get VPC and SG (assume existing) ---
vpcs = ec2.describe_vpcs(Filters=[{'Name': 'isDefault', 'Values': ['false']}])
vpc_id = vpcs['Vpcs'][0]['VpcId']
sg_id = ec2.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['SecurityGroups'][0]['GroupId']

# --- Step 3: Loop through AZ pairs and try RDS ---
db_name = 'mydb'
db_id = 'mydbinstance'
password = 'YourSecurePassword123!'
engine = 'mysql'
instance_class = 'db.t4g.micro'  # ✅ Better availability

pair_found = False

for az1, az2 in combinations(az_list, 2):
    print(f"\n🔄 Trying AZ pair: {az1}, {az2}")
    try:
        # Create 2 subnets
        subnet1 = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.10.0/24', AvailabilityZone=az1)
        subnet2 = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.11.0/24', AvailabilityZone=az2)
        subnet_ids = [subnet1['Subnet']['SubnetId'], subnet2['Subnet']['SubnetId']]

        # Create subnet group
        group_name = f"dynamic-subnet-group-{az1[-1]}{az2[-1]}"
        try:
            rds.create_db_subnet_group(
                DBSubnetGroupName=group_name,
                DBSubnetGroupDescription='Dynamic RDS group',
                SubnetIds=subnet_ids
            )
        except rds.exceptions.DBSubnetGroupAlreadyExistsFault:
            print("ℹ️ Subnet group already exists, reusing")

        # Attempt to launch RDS
        rds.create_db_instance(
            DBName=db_name,
            DBInstanceIdentifier=db_id,
            AllocatedStorage=20,
            DBInstanceClass=instance_class,
            Engine=engine,
            MasterUsername='admin',
            MasterUserPassword=password,
            VpcSecurityGroupIds=[sg_id],
            DBSubnetGroupName=group_name,
            PubliclyAccessible=False,
            MultiAZ=False
        )
        print(f"✅ RDS instance launch requested in {az1} + {az2}")
        pair_found = True
        break

    except ClientError as e:
        print(f"❌ Failed in {az1}, {az2}: {e.response['Error']['Message']}")
        # Clean up subnet group if failed
        try:
            rds.delete_db_subnet_group(DBSubnetGroupName=group_name)
        except:
            pass
        # Continue to next pair

if not pair_found:
    print("❌ Could not launch RDS in any AZ pair. Try again later.")
