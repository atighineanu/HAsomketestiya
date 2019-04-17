# HAsomketestiya
## A script which: 
* checks if cluster is fine (crm)
* if all resources run properly
* verifies if all nodes registered on sbd
* loads the config files for

            - csync2
            - haproxy
            - apache2 (you can pick another service for testing if you want)

* creates/deletes the resources haproxy and clone-ip (for the vip)
* tests with simple curl(s) to check if the balance is more or less ok (so far, just the default, round-robin, see haproxy template)
