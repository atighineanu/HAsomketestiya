from string import Template

##ipbind = '192.168.100.27'
##node1 = 'beta'
##node2 = 'gamma'
##ipnode1 = 'xxxx'
##ipnode2 = 'yyyy'

def HaprxyTemplHandler(haproxytempl, ipbind, IPs, nodes) :
    readingtemplate = open( haproxytempl )
    realsrc = Template(readingtemplate.read())
    
    ##variabila = ['unspe', 'doispe', 'treispe', 'paispe']
    ##d = {'variabila':'\n'.join(variabila)}     // pentru liste cu fiecare element din rand nou
    d = {'ipbind':ipbind, 
         'node1' :nodes[0], 'node2' :nodes[1], 'node3'   :nodes[2],
         'ipnode1' :IPs[0], 'ipnode2' :IPs[1], 'ipnode3'   :IPs[2]}

    return realsrc.substitute(d)



def ApacheTemplHandler(apachetempl, node, ip):
    readingtemplate = open( apachetempl )
    realsrc = Template(readingtemplate.read())
    d = {'node':node, 'ip':ip}
    return realsrc.substitute(d)

###HaprxyTemplHandler('template.txt', '192.168.100.27', 'beta' , 'gamma', 'xxxx', 'yyyy')
###ApacheTemplHandler( 'apachetempl.txt','gamma')