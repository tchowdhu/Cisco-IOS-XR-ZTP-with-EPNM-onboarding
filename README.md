# Cisco-IOS-XR-ZTP-with-EPNM-onboarding

This exercise provides an example of performing ZTP (classical) on a Cisco IOS XR router (here, the platform used was NCS540l) with an additional capabiliy of onboarding the ztp candidate router in Cisco Evolved Programmable Networ Manager (EPNM). The EPNM platform does not provide the ZTP capability to upload ZTP config and check the ZTP status from the system. However, EPNM provides a rich set of RESTConf and REST APIs. One of the available REST APIs is to add devices in EPNM which can be leveraged by ZTP script. 

</br></p>

The idea of this exercise is to automatically onboard router to the Cisco EMS/NMS software system, even though the system does not support ZTP natively. But, using the EPNM API and ZTP process supported in the XR platform user can auotmate the onboarding.

</br></p>

Cisco IOS XR Platform can take plain text config, shell script or python script as ZTP config file to pull from the DHCP/TFTP server and apply the config directly or configure the router based on the logics defined in the script.
In this example, we utilized python ztp script. The python script will be pulled from the remote DHCP/TFTP server and run on the XR platform (Onbox programming capability). 
The work flow is summarized below:


## DHCP Entry as Pre-requisite:

## Steps:

</br>1. Fresh Cisco IOS XR Platform, or mimicing it by cleaning the config using "commit replace" command in the config mode through console.
</br>2. Follow any of the following method to initiate ZTP:
</br>&nbsp;&nbsp;&nbsp;&nbsp;a. Boot a fresh router.
</br>&nbsp;&nbsp;&nbsp;&nbsp;b. Click the physical ZTP Button the XR Chassis (if any).
</br>&nbsp;&nbsp;&nbsp;&nbsp;c. After "commit replace" to clean the config, exit the config mode and run, "ztp initiate verbose".
</br>3. IP address will be pulled from the DHCP server.
</br>4. XR box will recongnize the config/script file location and it will pull the file in the XR box and run the script.
</br>5. The script will pull the config template and input data.json file from the DHCP/TFTP server location specified in the script. 
</br>6. The script will create the actual config using the template and the data.json inputs and apply it to the router.
</br>7. At the last part of the script, EPNM REST API is used to onboard the router to the EPNM server. 
