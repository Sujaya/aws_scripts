import boto3
# Enter the region your instances are in. Include only the region without specifying Availability Zone; e.g.; 'us-east-1'
region = 'us-west-1'
# Enter your instances here: ex. ['X-XXXXXXXX', 'X-XXXXXXXX']
instances = []
ec2 = boto3.resource('ec2')
for instance in ec2.instances.all():
    name = ''
    tags = {}
    for tag in instance.tags:
        if tag['Key'] == 'Type' and tag['Value'] == 'Hybrid':
        	instances.append(instance.instance_id)

ec2 = boto3.client('ec2', region_name=region)
ec2.start_instances(InstanceIds=instances)
print 'started your instances: ' + str(instances)
