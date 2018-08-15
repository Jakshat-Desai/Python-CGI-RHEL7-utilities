#!/usr/bin/python36

#header
print("content-type: text/html")
print("\n")

#importing libraries
import subprocess,cgi,os

#taking inputs
cmd=cgi.FieldStorage()
ip=cmd.getvalue("ip")
pswd=cmd.getvalue("pswd")
part=cmd.getvalue("part")
formt=cmd.getvalue("format")
loc=cmd.getvalue("loc")
opt=cmd.getvalue("opt")
addr="/media/"
if loc=="addr":
	addr=cmd.getvalue("addr")
drive=addr+cmd.getvalue("drive")

#auxillary variables
front_line="sudo sshpass -p "+pswd+" ssh -l root "+ip

print("<pre>")

if opt=="mount":
	#formatting the drive
	if formt!="none":
		os.system(front_line+" mkdir "+drive)
		print(subprocess.getoutput(front_line+" mkfs."+formt+" /dev/"+part))

	#mounting the drive
	if loc!="none":
		print(subprocess.getoutput(front_line+" mount /dev/"+part+" "+drive))
else:
	print(subprocess.getoutput(front_line+" umount /dev/"+part))

#links to other pages
print("</pre>")
print("<br /><a href=../partitions.html>Click here to insert/view/delete partitions</a>")
print("<br /><a href=../format_mount.html>Click here to format and/or mount partitions</a>")
