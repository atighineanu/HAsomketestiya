# HAsomketestiya
## A script which: 
----------------------------------------------------
Actions:
   - it runs crm status
   - sees if stonith running -> if running then:
   - sees if all nodes registered -> if not all reged:
   - it registers the missing one(s)
   - checks if haproxy and apache2 are installed -> if not:
   - instals above mentioned packages
   - loads config for haproxy, csync2 and apache, sends a message if success
   - checks if apache runs on all nodes
   - creates a primitive haproxy systemd::haproxy
   - creates a clone-group clone-ip (from vip, or admin-ip)
   - checks if haproxy runs properly
   - check if load balancer is evenly distributed across the cluster 
   --------------------------------------------------
   * Additional info:
      - for this script to run you need sshpass
      - you need to indicate in the code the IP of any node
      - running is just "python haproxy.py"  (works with python2.7)
      - you need to have the same password for all cluster nodes and put it into the code.    
    -------------------------------------------------
    * Description of files:
            - haproxy.py - main program
            - clustersetuptest.py - the script which tests the loadbalancer(with curl)
            - apachetempl - template of apache2 index.html
            - haproxytempl - template for haproxy.cfg (for csync2.cfg changes were short enough to add it just with a str)
            - templ.py - functions for rendering the templates for apache2 and haproxy
