#!/usr/bin/python36

print("content-type: text/html")
print("\n")

import os,subprocess,cgi

cmd=cgi.FieldStorage()
ip=cmd.getvalue('ip')
passwd=cmd.getvalue('passwd')
choice=cmd.getvalue('choice')
print("<pre>")
front_line="sudo sshpass -p "+passwd+" ssh -o StrictHostKeyChecking=no -l root "+ip
if choice=="server":
	fileAdd=cmd.getvalue('fileAdd')
	print(subprocess.getoutput(front_line+" chmod o+rwx "+fileAdd))
	print(subprocess.getoutput("sudo touch newAdds"))
	print(subprocess.getoutput("sudo chown apache newAdds"))
	f=open("newAdds","w+")
	f.write(fileAdd+" *(rw,no_root_squash)\n")
	f.close()
	print(subprocess.getoutput("sudo sshpass -p "+passwd+" scp -o StrictHostKeyChecking=no newAdds "+ip+":/newAdds"))
	print(subprocess.getoutput(front_line+" 'cat /newAdds >> /etc/exports'"))
	print(subprocess.getoutput(front_line+" systemctl restart nfs"))
elif choice=="client":
	serve=cmd.getvalue('serve')
	folder=cmd.getvalue('folder')
	mount=cmd.getvalue('mount')
	os.system(front_line+" mkdir "+mount)
	print(subprocess.getoutput(front_line+" mount "+serve+":"+folder+" "+mount))

print("<a href='../nfs.html'>Click here to setup nfs client/server</a>")
print("</pre>")
