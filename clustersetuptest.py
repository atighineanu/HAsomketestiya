import os, subprocess, time
sshpwd='test'
ip='192.168.100.222'
ipbind='192.168.100.231'
nodes=['alpha', 'beta', 'gamma']
loadcheck=[0, 0, 0]

###to delete haproxy and clone-ip
def Haprx_Cloneip_Deleter(ip):
    os.system("sshpass -p "+sshpwd+" ssh -Y root@"+ip+" 'crm resource stop clone-ip; crm resource stop haproxy'")

    time.sleep(3)
    deletecommand='crm configure \
    delete haproxy clone-ip'

    os.system("sshpass -p "+sshpwd+" ssh root@"+ip+" '"+str(deletecommand)+"'")

    proc = subprocess.Popen(["sshpass -p "+sshpwd+" ssh -Y root@"+ip+" 'crm status'"], stdout=subprocess.PIPE, shell=True)
    (output2, err) = proc.communicate()
    if not 'haproxy' in output2 and not 'clone-ip' in output2:
        print '4.c) Successfully deleted haproxy and clone-ip!'


###creates haproxy and clone-ip
def ClusterConfigurer(ip):
    global Haproxyrunnode
    proc = subprocess.Popen(["sshpass -p "+sshpwd+" ssh -Y root@"+ip+" 'crm status'"], stdout=subprocess.PIPE, shell=True)
    (output2, err) = proc.communicate()
    temp = output2.split("\n")
    haproxyflag=False
    cloneipflag=False
    for i in range(0, len(temp)):
        if 'haproxy' in temp[i] and 'tarted' in temp[i]:
            output = temp[i].split()
            Haproxyrunnode = output[len(output)-1]
            print '4.a) haproxy runs on node: '+Haproxyrunnode
            haproxyflag=True  
        if 'clone-ip' and 'admin-ip' in temp[i] and 'tarted' in temp[i+1]:
            output = temp[i+1].split()
            count=0
            for j in range(0, len(output)):
                if nodes[0] or nodes[1] or [nodes2] in output[j]:
                    count+=1     
            if count>=3:
                print '4.b) Clone-Set of admin-ip runs on (at least) three nodes. Success.'
            cloneipflag=True     
    if haproxyflag==False:
        haproxycfgcommand='crm configure \
        primitive haproxy systemd:haproxy \
        meta target-role=Started'
        os.system("sshpass -p "+sshpwd+" ssh root@"+ip+" '"+str(haproxycfgcommand)+"'")
        print '4.a.1) Successfully created primitive haproxy!'
        ClusterConfigurer(ip)

    if cloneipflag==False:
        cloneipcommand='crm configure \
        clone clone-ip admin-ip'
        os.system("sshpass -p "+sshpwd+" ssh root@"+ip+" '"+str(cloneipcommand)+"'")
        print '4.b.1) Successfully created clone-set "clone-ip"!'
        ClusterConfigurer(ip)
    

def ClusterTester(ipbind):
 print '5.a) Starting the load balancer test...'
 for j in range(0, 30):
    time.sleep(3)
    proc = subprocess.Popen(["curl -s "+ipbind], stdout=subprocess.PIPE, shell=True)
    (output3, err) = proc.communicate()
    if 'class' in output3 and 'rontend' in output3:
        print 'it\'s the node on which haproxy runs...'+str(Haproxyrunnode)
        for k in range(0, len(nodes)):
            if str(nodes[k]) in str(Haproxyrunnode):
                loadcheck[k]+=1
    else:
        for i in range(0, len(nodes)):
            if nodes[i] in output3:
                print 'it\'s the node: '+ nodes[i] 
                loadcheck[i]+=1
    proc.kill
    print loadcheck




