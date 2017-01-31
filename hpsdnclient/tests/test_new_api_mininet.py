#!/usr/bin/env python
#
#   Copyright 2013 Hewlett-Packard Development Company, L.P.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#   by Bruno Hareng
#   Test new apis of 2.7 controllers
#   

import hpsdnclient as hp
import os
from hpsdnclient.api import ApiBase
import hpsdnclient.datatypes as datatypes
from hpsdnclient.datatypes import Flow, Match, Action, Bucket, Group
from hpsdnclient.error import raise_errors, DatatypeError


#initialize the api
controller = os.getenv('SCA')
auth = hp.XAuthToken(user='sdn',password='skyline', server=controller)
api = hp.Api(controller=controller, auth=auth)

print "test get classes API"
classes = api.get_classes()
for classe in classes :
    print classe
    class_details = api.get_class_details (classe.id)
    print "class details"
    print class_details


datapaths = api.get_datapaths()


#print " test toogle port" 
#api.toggle_port("00:00:00:00:00:00:00:01","1","disable")

print " test get_sequencer "
sequencers = api.get_seq()
for sequence in sequencers:
    print sequence


print "test get_groups_features"
for datapath in datapaths:
    print datapath.dpid
    groups_features = api.get_groups_features(datapath.dpid)
    print groups_features


print "test groups api calls"
for datapath in datapaths:
    groups = api.get_groups(datapath.dpid)
    for group in groups:
        print group
        api.delete_groups(datapath.dpid, group.id)
    newgroup= hp.datatypes.Group(id=1, type="all", command="add", buckets=[])
    #newgroup = {"id": 1,"type": "all","command": "add","buckets": []}
    print newgroup
    api.add_group(datapath.dpid, newgroup)
    print "group 1 added"
    newgroup = {"id": 1,"type": "select","command": "modify","buckets": []}
    api.update_group(datapath.dpid, 1 , newgroup)
    print "group 1 updated"
    groups = api.get_groups(datapath.dpid)
    for group in groups:
        print group
        print group.id
        group_details=api.get_group_details(datapath.dpid, group.id)
        print group_details
        api.delete_groups(datapath.dpid, group.id)

print "test get_links"
for datapath in datapaths:
    links = api.get_links(datapath.dpid)
    for link in links:
        print links


print "test get_forward_path"
path = api.get_forward_path("00:00:00:00:00:00:00:01","00:00:00:00:00:00:00:0e")
print path

print " test get_nodes "
node = api.get_nodes("10.0.0.22",None,None,None,None)
print node [0]


print "test get_diag_packets"
packets = api.get_diag_packets("TCP")
print packets
packets = api.get_diag_packets("ICMP")
print packets
packets = api.get_diag_packets("UDP")
print packets

print "get_devices"
devices = api.get_devices()
for device in devices:
    print device
    print device.device_status
    if device.device_status is "Online":
        interfaces = api.get_device_interfaces(device.uid)
        for interface in interfaces:
            print interface
#    discoveryVlan = api.get_link_discovery_vlan(device.uid)
#    print discoveryVlan
    


#still issue with the devices rest API return as no keywork
print "get_devices_details"
for datapath in datapaths:
    device = api.get_device_details(datapath.dpid)
    print device