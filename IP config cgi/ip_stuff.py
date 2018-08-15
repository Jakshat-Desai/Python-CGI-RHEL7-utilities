#!/usr/bin/python36

#header
print("content-type: text/html")
print("\n")

#importing libraries
import subprocess,os,cgi

#functions
def forwarding(forward):
	#checking whether to enable or disable ip forwarding
	state=0
	if forward=="on":
		state=1
	#creating the file
	subprocess.getoutput("sudo touch /sysctl.conf")
	subprocess.getoutput("sudo chown apache /sysctl.conf")
	#configuring the sysctl file
	f=open("/sysctl.conf","w+")
	f.write("""# sysctl settings are defined through files in
# /usr/lib/sysctl.d/, /run/sysctl.d/, and /etc/sysctl.d/.
#
# Vendors settings live in /usr/lib/sysctl.d/.
# To override a whole file, create a new file with the same in
# /etc/sysctl.d/ and put new settings there. To override
# only specific settings, add a file with a lexically later
# name in /etc/sysctl.d/ and put new settings there.
#
# For more information, see sysctl.conf(5) and sysctl.d(5).
net.ipv4.ip_forward="""+str(state))
	f.close()

#taking inputs
cmd=cgi.FieldStorage()
ip=cmd.getvalue("ip")
pswd=cmd.getvalue("pswd")
choice=cmd.getvalue("choice")
forward=cmd.getvalue("forward")
onboot="no"
if choice=="static":
	onboot="yes"

print("<pre>")
#auxillary variables
truth=(ip==subprocess.getoutput("sudo hostname -I").split()[0])
front_line="sudo"
if truth==False:
	front_line="sudo sshpass -p "+pswd+" ssh -o StrictHostKeyChecking=no -l root "+ip

#ip forwarding
forwarding(forward)
#copying the sysctl file to the required system
if truth==False:
	print(subprocess.getoutput("sudo sshpass -p "+pswd+" scp -o StrictHostKeyChecking=no /sysctl.conf "+ip+":/etc/"))
else:
	print(subprocess.getoutput("sudo cp /sysctl.conf /etc/"))
#updating changes
subprocess.getoutput(front_line+" sysctl -p")

#configuring static or dynamic ip

#common settings to both static and dynamic ip
dynamic="""TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO="""+choice+"""
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=enp0s3
UUID=d124b673-863a-4fda-8441-bcb9bbc0e971
DEVICE=enp0s3
ONBOOT="""+onboot

stat=""

#extra settings for static ip
if choice=="static":
	stat="""
IPADDR="""+cmd.getvalue("stat")+"""
NETMASK="""+cmd.getvalue("net")+"""
GATEWAY="""+cmd.getvalue("gate")
	for i in (1,2,3):
		if cmd.getvalue("dns"+str(i))!=None:
			stat+=("\nDNS"+str(i)+"="+cmd.getvalue("dns"+str(i)))

print(subprocess.getoutput("sudo touch /ifcfg-enp0s3"))
print(subprocess.getoutput("sudo chown apache /ifcfg-enp0s3"))
f=open("/ifcfg-enp0s3","w+")
#writing the ifcfg-enp0s3 file
f.write(dynamic+stat)
f.close()

#copying the ifcfg-enp0s3 file to the required system
if truth==False:
	print(subprocess.getoutput("sudo sshpass -p "+pswd+" scp -o StrictHostKeyChecking=no /ifcfg-enp0s3 "+ip+":/etc/sysconfig/network-scripts/"))
else:
	print(subprocess.getoutput("sudo cp /ifcfg-enp0s3 /etc/sysconfig/network-scripts/ifcfg-enp0s3"))
#updating changes
print(subprocess.getoutput(front_line+" systemctl restart network"))
print("</pre>")
