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
from hpsdnclient.datatypes import Flow, Match, Action, Bucket, Group, Meters, Meter, MeterBand
from hpsdnclient.error import raise_errors, DatatypeError


#initialize the api
controller = "10.0.0.10"

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

print "test get_flow"
for datapath in datapaths:
    flows = api.get_flows(datapath.dpid)
    for flow in flows:
        print flow

print "test-add-flow"
match = Match(eth_type="ipv4", ipv4_src="10.0.0.20")
instruction0 = [{"apply_actions":[{"output": 0}],"write_actions": []}]
flow = Flow(priority=30000, match=match, instructions=instruction0, hard_timeout=30, table_id=200)
datapaths = api.get_datapaths()
print flow
#for d in datapaths:
#    api.add_flows(d.dpid, flow)

print "get_devices"
devices = api.get_devices()
for device in devices:
    print device
    print device.device_status
    if device.device_status is "Online":
        interfaces = api.get_device_interfaces(device.uid)
        for interface in interfaces:
            print interface

print "test get_flow with table_id 200"
for datapath in datapaths:
    flows = api.get_flows(datapath.dpid,"200")
    for flow in flows:
        print flow


print "test get_meters_features"
for datapath in datapaths:
    print datapath.dpid
    meters_features = api.get_meters_features(datapath.dpid)
    print meters_features


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

    bucket= hp.datatypes.Bucket(weight= 0,watch_group="ANY",watch_port= "ANY", actions= [{"output": 0}])
    #newgroup= hp.datatypes.Group(id=1, type="all", command="add", buckets=bucket)
    #newgroup = {"id": 1,"type": "all","command": "add","buckets": [{"actions":[{"output": 1}]}]}

    #newgroup= hp.datatypes.Group(id=1,type="all",command="add",buckets=[])
    #newgroup= hp.datatypes.Group(id=1,type="all",command="add",buckets=[{"weight": 0,"watch_group": "ANY","watch_port": "ANY","actions":[{"output": 0}]}])
    newgroup = {"id": 1,"type": "all","command": "add","buckets": []}

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


# Need to detect error 500 if not supported by the switch
print "test datapath_srcmacgrps and dstmacgrps"
for datapath in datapaths:
    api.add_datapath_srcmacgrps_mac(datapath.dpid,1, ["00:00:5E:00:53:04", "00:00:5E:00:53:05"])
    api.add_datapath_dstmacgrps_mac(datapath.dpid,1, ["00:00:5E:00:53:06", "00:00:5E:00:53:07"])
    srcmacgrps = api.get_datapath_srcmacgrps(datapath.dpid)
    dstmacgrps = api.get_datapath_dstmacgrps(datapath.dpid)
    for srcmacgrp in srcmacgrps:
        print srcmacgrp
        print srcmacgrp.group_id
        macs = api.get_datapath_srcmacgrps_mac(datapath.dpid,srcmacgrp.group_id)
        print macs 
        api.delete_datapath_srcmacgrps(datapath.dpid,srcmacgrp.group_id)
    for dstmacgrp in dstmacgrps:
        print dstmacgrp
        print dstmacgrp.group_id
        macs = api.get_datapath_dstmacgrps_mac(datapath.dpid,dstmacgrp.group_id)
        print macs 
        api.delete_datapath_dstmacgrps(datapath.dpid,dstmacgrp.group_id)

print "test get_meters_features"
for datapath in datapaths:
    print datapath.dpid
    meters_features = api.get_meters_features(datapath.dpid)
    print meters_features


print "test meters api calls"

band= hp.datatypes.MeterBand(burst_size=200,rate=250,mtype="drop")
newmeter= hp.datatypes.Meter(id=1,command="modify", flags=["kbps"], bands=[{ "burst_size": 200,"rate": 250, "mtype": "drop"}])
api.update_meter(datapath.dpid, 1, newmeter)

for datapath in datapaths:
    meters = api.get_meters(datapath.dpid)
    for meter in meters:
        print meter
        print meter.id
        api.delete_meter(datapath.dpid, meter.id)


    #newmeter= hp.datatypes.Meter(id=1,command="add", flags=["kbps"], bands=[{ "burst_size": 100,"rate": 150, "mtype": "drop"}])

    newmeter = { "id": 1, "command": "add", "flags": ["kbps"], "bands": [{ "burst_size": 100,"rate": 150, "mtype": "drop"}]}
    print newmeter
    api.add_meter(datapath.dpid, newmeter)
    print "meter 1 added"
    newmeter = { "id": 1, "command": "modify", "flags": ["kbps"], "bands": [{ "burst_size": 200,"rate": 250, "mtype": "drop"}]}
    api.update_meter(datapath.dpid, 1, newmeter)
    print "meter 1 updated"
    meters = api.get_meters(datapath.dpid)
    for meter in meters:
        print meter
        meter_details=api.get_meter_details(datapath.dpid, meter.id)
        print meter_details
        api.delete_meter(datapath.dpid, meter.id)



#    discoveryVlan = api.get_link_discovery_vlan(device.uid)
#    print discoveryVlan
    


#still issue with the devices rest API return as no keywork
#print "get_devices_details"
#print "still issue with the devices rest API return as no keywork"
#for datapath in datapaths:
#    device = api.get_device_details(datapath.dpid)
#    print device