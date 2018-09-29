import boto3
import botocore
import paramiko

key = paramiko.RSAKey.from_private_key_file("./hybrid.pem")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ips = []
ec2 = boto3.resource('ec2')
for instance in ec2.instances.all():
    name = ''
    tags = {}
    for tag in instance.tags:
        if tag['Key'] == 'Type' and tag['Value'] == 'Hybrid':
        	ips.append(instance.public_ip_address)

i = 0
for ip in ips:
	# Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
	client.connect(hostname=ip, username="ubuntu", pkey=key)

	
	print ip
	stdin, stdout, stderr = client.exec_command('pkill -f bft')
	print stdout.read()
	# Execute a command(cmd) after connecting/ssh to an instance
	cmd = 'cd /home/ubuntu/library && (nohup ./runscripts/smartrun.sh bftsmart.demo.counter.CounterServer ' + str(i) + ' > /dev/null 2>&1 &)'
	print cmd
	stdin, stdout, stderr = client.exec_command(cmd)
	print stdout.read()
	print stderr.read()
	i += 1

	# close the client connection once the job is done
	client.close()

