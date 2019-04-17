import os, subprocess
import templ

ip='192.168.100.222'
ipbind='192.168.100.27'

def NodeIPfinder(nodes):
    for i in range(0, len(nodes)):
        proc = subprocess.Popen(["sshpass -p test ssh -Y root@"+ip +" 'ping -c 3 "+nodes[i]+"'"], stdout=subprocess.PIPE, shell=True)
        (outcommand1, err) = proc.communicate()
        temp = outcommand1.split("\n")
        temp2 = temp[2].split()
        for j in range(2,len(temp2)):
            if nodes[i] in temp2[j]:
                IPs.append(temp2[j+1])
                IPs[len(IPs)-1]=IPs[len(IPs)-1].replace('(', '')
                IPs[len(IPs)-1]=IPs[len(IPs)-1].replace(')', '')
                IPs[len(IPs)-1]=IPs[len(IPs)-1].replace(':', '')



def RunningChecker(temp, str) :
 for i in range(0, len(temp)): 
    if temp[i] == str :
        for j in range(i, i+4):
            for k in range(0, len(nodes)):
                if nodes[k] == temp[j]:
                    if 'stonith-sbd' in str:
                        if 'tarted' in temp[j-1]:
                            runnersbd = nodes[k]
                            return runnersbd
                    elif 'admin' in str:
                        if 'tarted' in temp[j-1]:
                            runnerip = nodes[k]
                            return runnerip



def PackageInstaller(IPs, package) :
 for i in range(0, len(IPs)):
    ###checking if haproxy is installed:
    proc = subprocess.Popen(["sshpass -p test ssh -Y root@"+IPs[i]+" 'rpm -qi "+package+"'"], stdout=subprocess.PIPE, shell=True)
    (outcommand4, err) = proc.communicate()

    #remembering the machine's hostname
    proc = subprocess.Popen(["sshpass -p test ssh -Y root@"+IPs[i]+" 'hostname'"], stdout=subprocess.PIPE, shell=True)
    (outcommand3, err) = proc.communicate()

    if 'not installed' in str(outcommand4):
        proc = subprocess.Popen(["sshpass -p test ssh -Y root@"+IPs[i]+" 'zypper -n in "+package+"'"], stdout=subprocess.PIPE, shell=True)
        (outcommand1, err) = proc.communicate()


        temp = outcommand1.split("\n")
        ### last element [e.g. len(temp)-1] for some reason in zypper in output is ''
        ### therefore I aim for the line len(temp)-2, like: "Installing: apache2-prefork-2.4.23-29.40.1.x86_64...[many dots]...done"
        if 'Installing' in str(temp[len(temp)-2]) and '...done' in str(temp[len(temp)-2]) and package in str(temp[len(temp)-2]):
                print 'Successfully installed '+package+' on this node: ' + IPs[i]+' '+ outcommand3
    else:
        print package +' is already installed on '+ IPs[i] + ' ' + outcommand3
    



#a = os.system("sshpass -p test ssh -Y root@192.168.100.222 'crm status'")

proc = subprocess.Popen(["sshpass -p test ssh -Y root@"+ip+" 'crm status'"], stdout=subprocess.PIPE, shell=True)
(outcommand1, err) = proc.communicate()


## So far, just implemented to check two resources WHERE do they run:
## stonith-sbd and admin-ip; feel free to add more stuff when you need
##
temp = outcommand1.split()
#print temp
nodes = []
IPs = []
for i in range(0, len(temp)): 
    if temp[i] == 'Online:':
        for j in range(i+2, i+5): 
            if temp[j] != ']' : 
                nodes.append(temp[j])


runnersbd = RunningChecker(temp, 'stonith-sbd')
runnerip = RunningChecker(temp, 'admin-ip')

print '1.a) stonith-sbd runs on node '+ str(runnersbd)
print '1.b) admin-ip runs on node '+ str(runnerip) 

### checking if three nodes
print '1.c) list of online nodes: ' + str(nodes)
if len(nodes) >= 3 :
    print '1.d) good! more than 2 nodes...'

### checking which device is used by sbd
proc = subprocess.Popen(["sshpass -p test ssh -Y root@"+ip+" 'cat /etc/sysconfig/sbd'"], stdout=subprocess.PIPE, shell=True)
(outcommand2, err) = proc.communicate()
temp = outcommand2.split("\n")

sbddev = ''

for i in range(0, len(temp)):
    if 'SBD_DEVICE' in temp[i]:
        sbddev = temp[i].replace('SBD_DEVICE=', '')

print '2.a) sbd runs on this device: '+sbddev

### checking if all nodes are registered in sbd
proc = subprocess.Popen(["sshpass -p test ssh -Y root@"+ip+" 'sbd -d " + sbddev+ " list'"], stdout=subprocess.PIPE, shell=True)
(outcommand3, err) = proc.communicate()
print '2.b) list of registered nodes on SBD: \n'+outcommand3

temp = outcommand3.split("\n")
alternative = nodes[:]
##print id(alternative)
##print id(nodes)

if len(temp) >= 3:              ###at least three nodes...
    counter=0
    for i in range(0, len(temp)):
        for j in range(0, len(nodes)):
            if str(nodes[j]) in str(temp[i]):
                counter+=1
                alternative.remove(nodes[j]) # removing the registered nodes from alternative list

if counter >= 3:
    print '2.c) all three nodes are well-registered. Success. \n'
elif alternative != None:    #if alternative list of nodes is not empty -> register it with 'sbd -d <device> allocate <node>' command
    for i in range(0, len(alternative)):
        os.system("shpass -p test ssh -Y root@"+ip+" 'sbd -d "+sbddev+" allocate "+alternative[i]+"'")

#### Finding all ips of all nodes in cluster:
NodeIPfinder(nodes)

### Checking if haproxy installed on all nodes:
PackageInstaller(IPs, 'haproxy')

### Checking if apache2 installed on all nodes:
PackageInstaller(IPs, 'apache2')







