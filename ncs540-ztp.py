#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Copyright (c) 2023 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''

from __future__ import absolute_import, division, print_function

_author__ = "Tahsin Chowdhury <tchowdhu@cisco.com>"
__copyright__ = "Copyright (c) 2020 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import  os
import sys
import ssl
import json
import httplib
from pprint import pprint
from base64 import b64encode

sys.path.append("/pkg/bin")
from ztp_helper import ZtpHelpers


DHCP_SERVER_IP = "xx.xx.xx.xx"
CONFIG_DIR = "<folder_name>"
CONFIG_FILE = "<config-file>"
DEVICE_DATA_FILE = "<data-file-in-json>"
DESTINATION_FOLDER="/disk0:/ztp/tmp"

DATA_FILE_URL = "http://{}/{}/{}".format(DHCP_SERVER_IP, CONFIG_DIR, DEVICE_DATA_FILE)
CONFIG_FILE_URL = "http://{}/{}/{}".format(DHCP_SERVER_IP, CONFIG_DIR, CONFIG_FILE)

ztp_script = ZtpHelpers(syslog_file="/root/ztp_python.log", syslog_server="localhost", syslog_port=514)
ztp_script.toggle_debug(1)

print "\n###### Executing a show command before ZTP ######\n"
#pprint(ztp_script.xrcmd({"exec_cmd" :  "show running-config"}))
ztp_script.syslogger.info(ztp_script.xrcmd({"exec_cmd" : "show running-config"}))

print "\n###### Downloading a DATA FILE ######\n"
ztp_script.syslogger.info("\n###### Downloading a DATA FILE ######\n")
ztp_script.download_file(DATA_FILE_URL, DESTINATION_FOLDER)

with open(DESTINATION_FOLDER+"/"+DEVICE_DATA_FILE) as f:
    data = json.load(f)

print "Exposed DATA VARIABLE {}".format( data.keys() )
ztp_script.syslogger.info("Exposed DATA VARIABLE {}".format( data.keys() ))

print "\n###### Downloading a Config Template ######\n"
ztp_script.syslogger.info("\n###### Downloading a Config Template ######\n")
ztp_script.download_file(CONFIG_FILE_URL, DESTINATION_FOLDER)

with open(DESTINATION_FOLDER+"/"+CONFIG_FILE) as f:
    config_template = f.read()

config = config_template.format(EPNM_IP=data["EPNM_IP"],
                                DEVICE_USER=data["DEVICE_USER"],
                                DEVICE_PASS=data["DEVICE_PASS"])

print "\n###### Applying Config ######\n"
ztp_script.syslogger.info("\n###### Applying Config ######\n")

config_apply_response = ztp_script.xrapply_string(config)
ztp_script.syslogger.info(config_apply_response)

mgmt_intf = ztp_script.xrcmd({"exec_cmd" : "show running-config interface MgmtEth0/RP0/CPU0/0"})
ip_address = str(mgmt_intf['output'][1].split(' ')[2])
ztp_script.syslogger.info(ip_address)

ztp_script.xrapply_string('hostname NCS540-ZTP-{}'.format(ip_address.split('.')[3]))

print "\n###### Adding Device to EPNM ######\n"
ztp_script.syslogger.info("\n###### Adding Device to EPNM ######\n")

payload = json.dumps({
  "devicesImport": {
    "devices": {
      "device": [
        {
          "cliPassword": data["DEVICE_PASS"],
          "cliTimeout": "10",
          "cliTransport": "ssh2",
          "cliUsername": data["DEVICE_USER"],
          "cli_port": "22",
          "httpPort": "80",
          "httpServer": "http",
          "ipAddress": ip_address,
          "protocol": "ssh2",
          "snmpPort": "161",
          "snmpReadCommunity": "public",
          "snmpWriteCommunity": "private",
          "snmpRetries": "2",
          "snmpTimeout": "10",
          "snmpVersion": "2c"
        }
      ]
    }
  }
})


headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Authorization': 'Basic %s' % b64encode("{}:{}".format(data['EPNM_USER'], data['EPNM_PASS']))
}

conn = httplib.HTTPSConnection(data['EPNM_IP'], context = ssl._create_unverified_context())
conn.request("PUT", "/webacs/api/v4/op/devices/bulkImport", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
ztp_script.syslogger.info(data.decode("utf-8"))
