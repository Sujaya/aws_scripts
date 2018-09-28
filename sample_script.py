import boto3
import botocore
import paramiko

key = paramiko.RSAKey.from_private_key_file("./hybrid.pem")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect/ssh to an instance
ips = ["54.67.0.121", "13.57.12.236", "13.57.185.134"]

for ip in ips:
	# Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
	client.connect(hostname=ip, username="ubuntu", pkey=key)

	# Execute a command(cmd) after connecting/ssh to an instance
	stdin, stdout, stderr = client.exec_command('echo "hello world"')
	print stdout.read()

	# close the client connection once the job is done
	client.close()

