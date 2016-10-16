#/usr/bin/python
 
import boto.ec2
import time 
import os

SG = 'sg-abcdef'
data = 'ansible_ssh_user=ubuntu ansible_become=yes ansible_ssh_private_key_file=xyz.pem mongod_port=27017'
conn = boto.ec2.connect_to_region("us-west-2")


reservation = conn.run_instances(
    'ami-d732f0b7',
    key_name='xyz',
    instance_type='t2.micro',
    min_count=3,
    max_count=3, 
    security_group_ids=[SG]

)

print "Success"

for i in range(0,3):
	while reservation.instances[i].update() != "running":
		time.sleep(5)

for i in range(0,3):
	if i == 0:
		tag_name="mongo.primary.com"
		reservation.instances[i].add_tag("Name",tag_name)
		ipv4 = reservation.instances[i].private_ip_address
		print ipv4
		with open('variables','a') as f1:
			f1.write("%s   %s \n" % (ipv4, tag_name))
	else: 
		if i==1:
			tag_name="mongo.secondary1.com"
			sec1=reservation.instances[1].private_dns_name
		else:
			tag_name="mongo.secondary2.com"
			sec2=reservation.instances[2].private_dns_name
		reservation.instances[i].add_tag("Name",tag_name)
		ipv4 = reservation.instances[i].private_ip_address
		print ipv4
		with open('variables','a') as f1:
			f1.write("%s   %s \n" % (ipv4, tag_name))

	ip = reservation.instances[i].ip_address
	print ip
	with open('inventory','a') as f:
		if i==0: 
			f.write("[primary]")
			f.write("\n")
		elif i==1:
		    f.write("[secondary]")
		    f.write("\n") 

		f.write(ip + " " + data)
		f.write("\n")

filepath = os.path.join('/Users/Kriti_Bhandari/HPCS/HW/HW5/HW5_Roles/roles/primary/templates', 'repset_init.j2')
with open(filepath, 'a') as f1: 
	f1.write("rs.initiate();")
	f1.write("\n")
	f1.write('rs.add("{}:27017");'.format(sec1))
	f1.write("\n")
	f1.write('rs.add("{}:27017");'.format(sec2))



#To get the details of all the running instances at any given time
#reservations=conn.get_all_instances()

#for reservation in reservations:
#	for instances in reservation.instances:
#		print instances.ip_address

