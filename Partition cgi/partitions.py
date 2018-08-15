#!/usr/bin/python36

#header
print("content-type: text/html")
print("\n")

#importing libraries
import os,subprocess,cgi

#taking primary inputs
cmd=cgi.FieldStorage()
ip=cmd.getvalue("ip")
pswd=cmd.getvalue("pswd")
drive="/dev/"+cmd.getvalue("drive")
command=cmd.getvalue("command")

#auxillary variables
front_line="sudo sshpass -p "+pswd+" ssh -l root "+ip
part_type=""
part_no=""
no_enter=""
start_sec=""
fin_sec=""

print("<pre>")
#checking if drive exists
if subprocess.getoutput(front_line+" fdisk -l | "+front_line+" grep "+drive)=="":
	print("Drive doesnt exist")
#if drive doesnt exist
else:
#STEP1 : FORMING/DELETING/VIEWING THE PARTITIONS AND SAVING CHANGES
	if command=="p":
		pass
	elif command=="n":
		logical="\\n"
		part_type=cmd.getvalue("part_type")
		if subprocess.getoutput("sudo echo -e 'n \\n' | "+front_line+" fdisk "+drive+" | grep logical")!="":
			logical=""
			if part_type=="e":
				part_type="l"
			part_type=part_type+"\\n"
		if subprocess.getoutput("sudo echo -e 'n \\n"+part_type+"' | "+front_line+" fdisk "+drive+" | grep 'are in use'")!="": 
			part_type=logical
			logical=""
		part_no=logical#default partition number
		start_sec="\\n"#default start sector
		fin_sec="+"+cmd.getvalue("fin_sec")+"\\n"
	elif command=="d":
		part_no=cmd.getvalue("part_no")
		no_enter="\\n"
		subprocess.getoutput(front_line+" umount "+drive+part_no)

	print(subprocess.getoutput("sudo echo -e '"+command+"\\n"+part_type+part_no+no_enter+start_sec+fin_sec+"w \\n' | "+front_line+" fdisk "+drive))
	print(subprocess.getoutput(front_line+" partprobe "+drive))
print("</pre>")
print("<br /><a href=../partitions.html>Click here to insert/view/delete partitions</a>")
print("<br /><a href=../format_mount.html>Click here to format and/or mount partitions</a>")
