import boto3
import botocore
import paramiko

key = paramiko.RSAKey.from_private_key_file("./hybrid.pem")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ip_dict = {}
ec2 = boto3.resource('ec2')

i = 0
for instance in ec2.instances.all():
    name = ''
    tags = {}
    for tag in instance.tags:
        if tag['Key'] == 'Type' and tag['Value'] == 'Hybrid':
        	ip_dict[i] = {}
        	ip_dict[i]['public_ip'] = instance.public_ip_address
        	ip_dict[i]['private_ip'] = instance.private_ip_address
        	i += 1


config = {}
f = open('/home/sujaya/Desktop/library/config/hosts.config', "r")
lines = f.readlines()
for l in lines:
	if not l.startswith('#') and not l.startswith('\n'):
		i, private_ip = l.split(' ')[0], l.split(' ')[1]
		config[private_ip] = i


for i in ip_dict:
	# Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
	ip = ip_dict[i]['public_ip']
	client.connect(hostname=ip, username="ubuntu", pkey=key)
	
	print ip
	stdin, stdout, stderr = client.exec_command('pkill -f bft')
	print stdout.read()
	# Execute a command(cmd) after connecting/ssh to an instance
	private_ip = ip_dict[i]['private_ip']
	i = config[private_ip]
	cmd = 'cd /home/ubuntu/library && (nohup ./runscripts/smartrun.sh bftsmart.demo.microbenchmarks.ThroughputLatencyServer ' + str(i) + ' 20000 4 5 false > output.out 2>&1 &)'
	#cmd = 'cd /home/ubuntu/library && (nohup ./runscripts/smartrun.sh bftsmart.demo.counter.CounterServer ' + str(i) + ' > output.out 2>&1 &)'
	print cmd
	stdin, stdout, stderr = client.exec_command(cmd)
	print stdout.read()
	print stderr.read()

	# close the client connection once the job is done
	client.close()

# for i in ip_dict:
# 	# Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
# 	ip = ip_dict[i]['public_ip']
# 	client.connect(hostname=ip, username="ubuntu", pkey=key)
	
# 	print ip
# 	stdin, stdout, stderr = client.exec_command('pkill -f bft')
# 	stdin, stdout, stderr = client.exec_command('cd /home/ubuntu/library/config && rm currentView')
# 	print stdout.read()
# 	# Execute a command(cmd) after connecting/ssh to an instance
# 	stdin, stdout, stderr = client.exec_command('cd /home/ubuntu/library && git pull')
# 	print stdout.read()
# 	print stderr.read()

# 	# close the client connection once the job is done
# 	client.close()
