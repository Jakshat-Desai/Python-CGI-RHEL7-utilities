#!/usr/bin/python36

#header
print("content-type: text/html")
print("\n")

#importing the libraries
import os,subprocess,cgi

#auxillary functions
def filewrite(name_,value_):
	return """<?xml version="1.0"?>

<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site specific overrides in this file -->

<configuration>

<property>
<name>"""+name_+"""</name>
<value>"""+value_+"""</value>
</property>

</configuration>"""

def installhadoop(ins):
	#write code for hadoop installation

#fetching all the variables
cmd=cgi.FieldStorage()
ip=cmd.getvalue('ip')
pswd=cmd.getvalue('pswd')
node_type=cmd.getvalue('choice')
mas=ip
jt=ip	
name="dfs.data.dir"
value="/"+cmd.getvalue('fldr')
conf=cmd.getvalue('conf')
formt=cmd.getvalue('formt')
choicemr=cmd.getvalue('choicemr')
confmr=cmd.getvalue('confmr')
# value of this variable is either 'yes' or 'no' depending on whether user wants to install hadoop or not
install=cmd.getvalue('install')
if node_type=="master":
	name="dfs.name.dir"
else:
	mas=cmd.getvalue('mas')

if choicemr !="master":
	jt=cmd.getvalue('jt')

print("<pre>")
#common line with which most commands will start
front_line="sudo sshpass -p "+pswd+" ssh -o StrictHostKeyChecking=no -l root "+ip

#for hdfs
if (conf=="yes" and node_type!=None) or (choicemr=="master" and mas!=None):
	#common settings irrespective of whether node is slave or not
	#editing the core-site.xml file
	subprocess.getoutput("sudo touch /core-site.xml")
	subprocess.getoutput("sudo chown -R apache /core-site.xml")
	f=open("/core-site.xml","w+")
	f.write(filewrite("fs.default.name","hdfs://"+mas+":9001"))
	f.close()
	#end of editing task of core-site.xml
	if node_type!="client" and node_type!=None:
		#editing the local hdfs-site.xml file
		subprocess.getoutput("sudo touch /hdfs-site.xml")
		subprocess.getoutput("sudo chown -R apache /hdfs-site.xml")
		f=open("/hdfs-site.xml","w+")
		f.write(filewrite(name,value))
		f.close()
		#end of editing task of local hdfs-site.xml

#for mapred
if confmr=="yes" and (choicemr!=None or node_type=="client") and jt!=None:
	#common settings irrespective of whether node is slave or not
	#editing the mapred-site.xml file
	subprocess.getoutput("sudo touch /mapred-site.xml")
	subprocess.getoutput("sudo chown -R apache /mapred-site.xml")
	f=open("/mapred-site.xml","w+")
	f.write(filewrite("mapred.job.tracker",jt+":9002"))
	f.close()
	#end of editing task of mapred-site.xml

#creating directory
if formt=="yes" and value!=None:
	os.system(front_line+" rm -r -f "+value)
if value!="None":
	os.system(front_line+" mkdir "+value)

#copying files created in local system to desired location in remote system
if conf=="yes" and node_type!=None:
	os.system("sudo sshpass -p "+pswd+" scp -o StrictHostKeyChecking=no /core-site.xml "+ip+":/etc/hadoop/")
	if node_type!="client":
		os.system("sudo sshpass -p "+pswd+" scp -o StrictHostKeyChecking=no /hdfs-site.xml "+ip+":/etc/hadoop/")
if confmr=="yes" and choicemr!=None:
	os.system("sudo sshpass -p "+pswd+" scp -o StrictHostKeyChecking=no /mapred-site.xml "+ip+":/etc/hadoop/")
print("Files configured")

#shutting firewall
subprocess.getoutput(front_line+" iptables -F")
print("Firewall Closed")

subprocess.getoutput(front_line+" hadoop-daemon.sh stop datanode")
subprocess.getoutput(front_line+" hadoop-daemon.sh stop namenode")
#starting the hdfs node
if node_type=="master":
	if formt=="yes":
		print(subprocess.getoutput(front_line+" echo Y | "+front_line+" hadoop namenode -format --stdin"))
	print(subprocess.getoutput(front_line+" hadoop-daemon.sh start namenode"))
	print(subprocess.getoutput(front_line+" hadoop dfsadmin -safemode leave"))
	if subprocess.getoutput(front_line+" jps | grep "+front_line+" NameNode")!="":
		print("NameNode started")
	else:
		print("NameNode not started")
elif node_type=="slave":
	print(subprocess.getoutput(front_line+" hadoop-daemon.sh start datanode"))
	if subprocess.getoutput(front_line+" jps | grep DataNode")!="":
		print("DataNode started")
	else:
		print("DataNode not started")
#starting MR nodes
if node_type=="client":
	print("Client started")
elif choicemr=="master":
	print(subprocess.getoutput(front_line+" hadoop-daemon.sh start jobtracker"))
	if subprocess.getoutput(front_line+" jps | grep "+front_line+" JobTracker")!="":
		print("JobTracker started")
	else:
		print("JobTracker not started")
elif choicemr=="slave":
	print(subprocess.getoutput(front_line+" hadoop-daemon.sh start tasktracker"))
	if subprocess.getoutput(front_line+" jps | grep "+front_line+" TaskTracker")!="":
		print("TaskTracker started")
	else:
		print("TaskTracker not started")
print("</pre>")

print("<a href=http://"+mas+":50070>Click here for HDFS Web UI</a><br />")
print("<a href=http://"+jt+":50030>Click here for MR Web UI</a><br />")
print("<a href=../filehandler.html>Click here to upload/delete/view files</a><br />")
print("<a href=../cluster.html>Click here to add new slave/create new cluster</a>")
