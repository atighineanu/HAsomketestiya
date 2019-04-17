from string import Template

ipbind = '192.168.100.27'
node1 = 'beta'
node2 = 'gamma'
ipnode1 = 'xxxx'
ipnode2 = 'yyyy'

def HaprxyTemplHandler(haproxytempl, ipbind, node1, node2, ipnode1, ipnode2) :
    readingtemplate = open( haproxytempl )
    realsrc = Template(readingtemplate.read())
    
    ##variabila = ['unspe', 'doispe', 'treispe', 'paispe']
    ##d = {'variabila':'\n'.join(variabila)}
    d = {'ipbind':ipbind, 'node1' :node1, 'node2' :node2, 'ipnode1' :ipnode1, 'ipnode2' :ipnode2}

    return realsrc.substitute(d)



def ApacheTemplHandler(apachetempl, node):
    readingtemplate = open( apachetempl )
    realsrc = Template(readingtemplate.read())
    
    ##variabila = ['unspe', 'doispe', 'treispe', 'paispe']
    ##d = {'variabila':'\n'.join(variabila)}
    d = {'node':node }
    return realsrc.substitute(d)

###HaprxyTemplHandler('template.txt', '192.168.100.27', 'beta' , 'gamma', 'xxxx', 'yyyy')
###ApacheTemplHandler( 'apachetempl.txt','gamma')