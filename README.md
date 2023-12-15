# Cisco-IOS-XR-ZTP-with-EPNM-onboarding

This exercise provides an example of performing ZTP (classical) on a Cisco IOS XR router (here, the platform used was NCS540l) with an additional capabiliy of onboarding the ztp candidate router in Cisco Evolved Programmable Networ Manager (EPNM). The EPNM platform does not provide the ZTP capability to upload ZTP config and check the ZTP status from the system. However, EPNM provides a rich set of RESTConf and REST APIs. One of the available REST APIs is to add devices in EPNM which can be leveraged by ZTP script. 

</br>

Cisco IOS XR Platform can take plain text config, shell script or python script as ZTP config file to pull from the DHCP/TFTP server and apply the config directly or configure the router based on the logics defined in the script.
In this example, we utilized python ztp script. The work flow is summarized below:


## DHCP Entry as Pre-requisite:

## Steps:

</br>1. Fresh Cisco IOS XR Platform, or mimicing it by cleaning the config using "commit replace" command in the config mode.
</br>2. Follow any of the following method to initiate ZTP:
</br><\t>    a. Boot a fresh router.
</br><\t>    b. Click the physical ZTP Button the XR Chassis (if any).
</br><\t>    c. After "commit replace" to clean the config, exit the config mode and run, "ztp initiate verbose".
