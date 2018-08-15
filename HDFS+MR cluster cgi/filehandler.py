#!/usr/bin/python36

print("content-type: text/html")
print("\n")

import cgi,subprocess,os

cmd=cgi.FieldStorage()
ip=cmd.getvalue("ip")
pswd=cmd.getvalue("pswd")
choice=cmd.getvalue("choice")
filename=cmd.getvalue("filename")
front_line="sudo sshpass -p "+pswd+" ssh -o StrictHostKeyChecking=no -l root "+ip

if choice=="ins":
	print(subprocess.getoutput(front_line+" hadoop fs -put "+filename+" /"))
elif choice=="del":
	print(subprocess.getoutput(front_line+" hadoop fs -rm -rvf "+filename+" /"))
else:
	print(subprocess.getoutput(front_line+" hadoop fs -cat "+filename+" /"))

print("<a href=http://"+ip+":50070>Web UI</a><br />")
print("<a href=../cluster.html>Add another slave/create new cluster</a><br />")
print("<a href=../filehandler.html>Click here to upload/delete/view files</a><br />")
