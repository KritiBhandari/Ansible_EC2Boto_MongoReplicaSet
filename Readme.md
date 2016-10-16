Automated Deployment with Ansible
==================================

Part1: Create EC2 Instances using Python Boto
---------------------------------------------
###*Amazon EC2 Instance Creation*

###Create a Security(sg-abcdef) group in your AWS Account
	(1)Inbound Rules: 
		(a)Allows SSH from 0.0.0.0/0 (or your company subnet)
		(b)Allows TCP port 27017 from sg-abcdef (or 0.0.0.0/0)
	(2) Outbound Rules: 
		(a) Allow all traffic (Default)

###Run the script boto_aws.py
>	python boto_aws.py

###What does this script do? 
	(1) It creates three Ubuntu EC2 instances and attaches the SG (sg-abcdef) 
		to them
	(2) Names the instances appropriately
	(3) Attains their public IP Address and populates the 'inventory' file 
	(4) Attains their private DNS names and populates the 'repset_init.j2' 
		file withing the template of the Primary role. 



Part2: Ansible installs MongoDB and Sets up the Replica-Set
-----------------------------------------------------------

###Instance State
    (1) After some time, the instances come up and are in the completely 		healthy state
    (2) SSH into each of these instances to make sure that they are all 			reachable using SSH, as Ansible uses SSH 

###Run the ansible command 
>	ansible-playbook main.yml -i inventory -vvv

###How is Ansible Set up
	(1) The 'allrole' role is responsible for installing MongoDB on all of the 	   instances, creates the mongodb user and creates the required 			directories for Mongo
	(2) The 'primary' role initiates the Replica set and adds the Secondary 	instances as the slaves to its Replica Set
	(3) The 'secondary' role makes the secondary mongo instances join the 		Replica set as slaves

###Verify the Replica Set
	SSH into all the instances and run:
>		mongo

>		rs.conf()

>		rs.status()


NOTE: 
The files 'inventory' and 'repset_init.j2' are created by boto_aws.py
