#!/usr/bin/env python
#
#   Copyright 2014 Hewlett-Packard Development Company, L.P.
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
#   created by Dave Tucker - 2014 with version 2.1 of the HP SDN controller
#   modified by Bruno Hareng -2016 with version 2.7 of the HP SDN controller
#   controller stats APIs not implemented, nor the classe put and del APIs

import json
# Python3 compatibility
try:
    import urllib.parse as urllib
except ImportError:
    import urllib

from hpsdnclient.api import ApiBase
import hpsdnclient.datatypes as datatypes
from hpsdnclient.error import raise_errors, DatatypeError


class OfMixin(ApiBase):
    """OpenFlow REST API Methods

    This class contains methods that call the OpenFlow
    REST API on the HP VAN SDN Controller

    - Topology Service
    - Node Service
    - Link Service
    - Path Planner
    - Path Diagnostics Service

    """
    def __init__(self, controller, restclient):
        super(OfMixin, self).__init__(controller, restclient)
        self._of_base_url = ("https://{0}:8443".format(self.controller) +
                             "/sdn/v2.0/of/")

    #bhg38 created based on 2.7 API spec
    def get_classes(self):
        """Lists the set of flow classes that are registered on the controller.

        :return: A list of classes
        :rtype: list

        """
        url = self._of_base_url + 'classes'
        return self.restclient.get(url)

    #bhg38 created based on 2.7 API spec
    def get_class_details(self, id):
        """Lists the flow classes that is registered with the specified ID.

        :return: class details
        :rtype: hpsdnclient.datatypes.Class


        """
        url = (self._of_base_url + 'classes/{0}'.format(id))
        return self.restclient.get(url)

 
    def get_datapaths(self):
        """List all datapaths that are managed by this controller.

        :return: A list of Datapaths
        :rtype: list

        """
        url = self._of_base_url + 'datapaths'
        return self.restclient.get(url)

    def get_datapath_detail(self, dpid):
        """Get detailed information for a datapath.

        :param str dpid: The datapath ID
        :return: Datapath details
        :rtype: hpsdnclient.datatypes.Datapath

        """
        url = (self._of_base_url + 'datapaths/{0}'.format(urllib.quote(dpid)))
        return self.restclient.get(url)



    def get_meters_features(self, dpid):
        """Lists meter features for the given datapath

        :param str dpid: The datapath ID
        :returns: A list of meter features
        :rtype:  hpsdnclient.datatypes.Meterfeatures

        """
        url = (self._of_base_url +
               'datapaths/{0}/features/meter'.format(urllib.quote(dpid)))
        return self.restclient.get(url)


    #bhg38: created based on 2.7 API spec
    def get_groups_features(self, dpid):
        """Get datapath group features

        :param str dpid: The Datapath ID
        :return: Group Features
        :rtype: hpsdnclient.datatypes.GroupFeatures

        """
        url = (self._of_base_url +
               'datapaths/{0}/features/group'.format(urllib.quote(dpid)))
        return self.restclient.get(url)


    # bhg38: added support for optional table id
    def get_flows(self, dpid, table_id=None):
        """Gets a list of flows on the supplied DPID


        :param str dpid: The datapath ID
        :param str table_id: optional table_id
        :return: List of flows
        :rtype: list

        """
        url = (self._of_base_url +
               'datapaths/{0}/flows'.format(urllib.quote(dpid)))
        if table_id:
            url = url + '?table_id={0}'.format(table_id)
        return self.restclient.get(url)

    def _assemble_flows(self, flows):
        if isinstance(flows, list):
            tmp = []
            for f in flows:
                if isinstance(f, datatypes.Flow):
                    tmp.append(f.to_dict())
                else:
                    raise DatatypeError(datatypes.Flow, f.__class__())
            data = {"flows": tmp}
        elif isinstance(flows, datatypes.Flow):
            data = {"flow": flows.to_dict()}
        else:
            raise DatatypeError([datatypes.Flow, list], f.__class__())
        return data

    def add_flows(self, dpid, flows):
        """Add a flow, or flows to the selected DPID

        :param str dpid: The datapath ID
        :param list, hpsdnclient.datatypes.Flow flows: The flow or flows to add

        """
        url = (self._of_base_url +
               'datapaths/{0}/flows'.format(urllib.quote(dpid)))
        data = self._assemble_flows(flows)
        r = self.restclient.post(url, json.dumps(data))
        raise_errors(r)

    def update_flows(self, dpid, flows):
        """Update a flow, or flows at the selected DPID

        :param str dpid: The datapath ID
        :param list, hpsdnclient.datatypes.Flow flows:
            The flow or flows to update

        """
        url = (self._of_base_url +
               'datapaths/{0}/flows'.format(urllib.quote(dpid)))
        data = self._assemble_flows(flows)
        r = self.restclient.put(url, json.dumps(data))
        raise_errors(r)

    def delete_flows(self, dpid, flows):
        """ Delete flow, or flows from the specified DPID

        :param str dpid: The datapath ID
        :param list, hpsdnclient.datatypes.Flow flows:
            The flow or flows to delete

        """
        url = (self._of_base_url +
               'datapaths/{0}/flows'.format(urllib.quote(dpid)))
        data = self._assemble_flows(flows)
        r = self.restclient.delete(url, json.dumps(data))
        raise_errors(r)

   #Groups section
    def get_groups(self, dpid):
        """Get a list of groups created on the DPID

        :param str dpid: The datapath ID
        :return: List of groups
        :rtype: list

        """
        url = (self._of_base_url +
               'datapaths/{0}/groups'.format(urllib.quote(dpid)))

        return self.restclient.get(url)

    def add_group(self, dpid, group):
        """Create a group

        :param str dpid: The datapath ID
        :param group: The group to add that can be in hpsdnclient.datatypes.Group format or in Json

        """
        url = (self._of_base_url +
               'datapaths/{0}/groups'.format(urllib.quote(dpid)))
        if isinstance(group, datatypes.Group):
            data = {"version": "1.3.0","group": group.to_dict()}
        else:
            data = {"version": "1.3.0","group": group}
        r = self.restclient.post(url, json.dumps(data))
        raise_errors(r)

    def get_group_details(self, dpid, group_id):
        """Get group details

        :param str dpid: The datapath ID
        :param str group_id: The group ID
        :return: Group details
        :rtype: hpsdnclient.datatypes.Group

        """
        url = (self._of_base_url +
               'datapaths/{0}/groups/{1}'.format(urllib.quote(dpid), group_id))
        return self.restclient.get(url)

    #bhg38: changed from post to put as documented in the 2.7 spec
    def update_group(self, dpid, group_id, group):
        """Update a group

        :param str dpid: The datapath ID
        :param group: The group to update that can be in hpsdnclient.datatypes.Group format or in Json

        """
        url = (self._of_base_url +
               'datapaths/{0}/groups/{1}'.format(urllib.quote(dpid), group_id))
        if isinstance(group, datatypes.Group):
            data = {"version": "1.3.0","group": group.to_dict()}
        else:
            data = {"version": "1.3.0","group": group}        
        r = self.restclient.put(url, json.dumps(data))
        raise_errors(r)

    def delete_groups(self, dpid, group_id):
        """Delete a group

        :param str dpid: The datapath ID
        :param str group_id: The group ID to delete

        """
        url = (self._of_base_url +
               'datapaths/{0}/groups/{1}'.format(urllib.quote(dpid), group_id))
        r = self.restclient.delete(url)
        raise_errors(r)


    #Meters section
    def get_meters(self, dpid):
        """List all meters configured on the supplied DPID

        :param str dpid: The datapath ID
        :returns: A list of meters
        :rtype: list

        """
        url = (self._of_base_url +
               'datapaths/{0}/meters'.format(urllib.quote(dpid)))
        return self.restclient.get(url)

    def add_meter(self, dpid, meter):
        """Add a new meter to the supplied DPID

        :param str dpid:
        :param meter: The meter can be in hpsdnclient.datatypes.Meter format or in Json

        """
        url = (self._of_base_url +
               'datapaths/{0}/meters'.format(urllib.quote(dpid)))
        if isinstance(meter, datatypes.Meter):
            data = {"version": "1.3.0","meter": meter.to_dict()}
        else:
            data = {"version": "1.3.0","meter": meter}

        r = self.restclient.post(url, json.dumps(data))
        raise_errors(r)

    def get_meter_details(self, dpid, meter_id):
        """Get detailed meter information

        :param str dpid: The datapath ID
        :param str meter_id: The meter ID
        :return: Meter details
        :rtype: hpsdnclient.datatypes.Meter

        """
        url = (self._of_base_url +
               'datapaths/{0}/meters/{1}'.format(urllib.quote(dpid), meter_id))
        return self.restclient.get(url)

    def update_meter(self, dpid, meter_id, meter):
        """ Update the specified meter

        :param str dpid: The datapath ID
        :param str meter_id: The meter ID
        :param meter: The meter can be in hpsdnclient.datatypes.Meter format or in Json

        """
        url = (self._of_base_url +
               'datapaths/{0}/meters/{1}'.format(urllib.quote(dpid), meter_id))
        if isinstance(meter, datatypes.Meter):
            data = {"version": "1.3.0","meter": meter.to_dict()}
        else:
            data = {"version": "1.3.0","meter": meter}

        r = self.restclient.put(url, json.dumps(data))
        raise_errors(r)

    def delete_meter(self, dpid, meter_id):
        """Delete a meter

        :param str dpid: The datapath ID
        :param str meter_id: The meter ID to be deleted

        """
        url = (self._of_base_url +
               'datapaths/{0}/meters/{1}'.format(urllib.quote(dpid), meter_id))
        r = self.restclient.delete(url)
        raise_errors(r)

    #Ports
    def get_ports(self, dpid):
        """ Gets a list of ports from the specified DPID

        :param str dpid: The datapath ID
        :return: List of ports
        :rtype: list

        """
        url = (self._of_base_url +
               'datapaths/{0}/ports'.format(urllib.quote(dpid)))
        return self.restclient.get(url)

    def get_port_detail(self, dpid, port_id):
        """ Gets detailed port information for the specified port

        :param str dpid: The datapath ID
        :param str port_id: The port ID
        :return: Port details
        :rtype: hpsdnclient.datatypes.Port

        """
        url = (self._of_base_url +
               'datapaths/{0}/ports/{1}'.format(urllib.quote(dpid), port_id))
        return self.restclient.get(url)

   #bhg38: added as specified in 2.7 API spec
    def toogle_port(self, dpid, port_id, action):
        """Enables or disables the specified datapath and port. This API is asynchronous

        :param str dpid: datapath id
        :param str port_id: port id - must be a physical port
        :param str action : 'enable' or 'disable' 

        """

        url = (self._of_base_url +
               'datapaths/{0}/ports/{1}/action'.format(urllib.quote(dpid), port_id))
        r = self.restclient.post(url, action)
        raise_errors(r)


    #bhg38: created based on 2.7 API spec
    def get_seq(self):
        """Lists information about the packet listeners that are registered on the controller

        :return: List of information about the packet listeners
        """
        url = self._of_base_url + 'sequencer'
        return self.restclient.get(url)


    def get_stats(self):
        """List controller statistics for all controllers that are
        part of this controller's team.

        :return: List of statistics
        :rtype: hpsdnclient.datatypes.Stats"""
        url = self._of_base_url + 'stats'
        return self.restclient.get(url)

    #bhg38: modified to make sure the port is a physical port
    def get_port_stats(self, dpid, port_id=None):
        """List all port statistics for a given datapath or for a
        given datapath and port number

        :param str dpid: Filter by Datapath ID
        :param str port_id: Filter by Port ID
        :returns: Statistics for Port
        :rtype: hpsdnclient.datatypes.Stats

        """
        url = (self._of_base_url +
               'stats/ports?dpid={0}'.format(urllib.quote(dpid)))
        if port_id.isdigit():
           url = url + '&port_id={0}'.format(port_id)
        else: 
           return
        return self.restclient.get(url)

    def get_group_stats(self, dpid, group_id=None):
        """List group statistics

        :param str dpid: Filter by Datapath ID
        :param group_id: Filter by Group ID
        :return: Group statistics
        :rtype: hpsdnclient.datatypes.Stats

        """
        url = (self._of_base_url +
               'stats/groups?dpid={0}'.format(urllib.quote(dpid)))
        if group_id:
            url = url + '&group_id={0}'.format(group_id)
        return self.restclient.get(url)

    def get_meter_stats(self, dpid, meter_id):
        """List meter statistics for

        :param str dpid: The Datapath ID
        :param str meter_id: The Meter ID
        :return: Meter statistics
        :rtype: hpsdnclient.datatypes.Stats

        """
        url = (self._of_base_url +
               'stats/meters?dpid={0}&meter={1}'.format(urllib.quote(dpid),
                                                        meter_id))
        return self.restclient.get(url)

    #bhg38 created based on 2.7 API spec
    def get_datapath_dstmacgrps(self, dpid):
        """Lists the destination MAC groups that are configured
         on the specified datapath.
         Not supported on all switches. No error is returned 
         if the switch does not support this feature

        :param str dpid: The Datapath ID
        :return: a list of mac-groups
        :rtype: hpsdnclient.datatypes.Macgroups

        """
        url = (self._of_base_url + 
               'datapaths/{0}/dstmacgrps'.format(urllib.quote(dpid)))
        return self.restclient.get(url)

    #bhg38: created based on 2.7 API spec
    def delete_datapath_dstmacgrps(self, dpid, grp_id):
        """Deletes all MAC addresses from the specified destination MAC group ID on the specified datapath.
           Not supported on all switches. No error is returned if the switch does not support this feature.

        :param str dpid: The datapath ID
        :param str grp_id: The mac group ID to be deleted

        """
        url = (self._of_base_url +
               'datapaths/{0}/dstmacgrps/{1}'.format(urllib.quote(dpid), grp_id))
        r = self.restclient.delete(url)
        raise_errors(r)


    #bhg38: created based on 2.7 API spec
    def get_datapath_dstmacgrps_mac(self, dpid, grp_id):
        """Lists the MAC addresses that are configured for the specified destination MAC group ID on the specified datapath.
           Not supported on all switches. No error is returned if the switch does not support this feature.

        :param str dpid: The datapath ID
        :param str grp_id: The mac group ID to be deleted

        """
        url = (self._of_base_url +
               'datapaths/{0}/dstmacgrps/{1}/macs'.format(urllib.quote(dpid), grp_id))
        return self.restclient.get(url)

 
    #bhg38: created based on 2.7 API spec
    def add_datapath_dstmacgrps_mac(self, dpid, grp_id, macs):
        """Adds MAC addresses to the specified destination MAC group ID on the specified datapath.
           Not supported on all switches. No error is returned if the switch does not support this feature.

        :param str dpid: The datapath ID
        :param str grp_id: The mac group ID to be deleted
        :param macs : List of mac @ to add 

        """
        url = (self._of_base_url +
               'datapaths/{0}/dstmacgrps/{1}/macs'.format(urllib.quote(dpid), grp_id))
        data = {"macs": macs}
        r = self.restclient.post(url, json.dumps(data))
        raise_errors(r)


    
    #bhg38 created based on 2.7 API spec
    def get_datapath_srcmacgrps(self, dpid):
        """Lists the source MAC groups that are configured on the specified datapath.
        Not supported on all switches. No error is returned if the switch does not support this feature

        :param str dpid: The Datapath ID
        :return: a list of mac-groups
        :rtype: hpsdnclient.datatypes.Macgroups

        """

        url = (self._of_base_url + 'datapaths/{0}/srcmacgrps'.format(urllib.quote(dpid)))
        return self.restclient.get(url)

    #bhg38: created based on 2.7 API spec
    def delete_datapath_srcmacgrps(self, dpid, grp_id):
        """Deletes all MAC addresses from the specified source MAC group ID on the specified datapath.
           Not supported on all switches. No error is returned if the switch does not support this feature.

        :param str dpid: The datapath ID
        :param str grp_id: The mac group ID to be deleted

        """
        url = (self._of_base_url +
               'datapaths/{0}/srcmacgrps/{1}'.format(urllib.quote(dpid), grp_id))
        r = self.restclient.delete(url)
        raise_errors(r)


    #bhg38: created based on 2.7 API spec
    def get_datapath_srcmacgrps_mac(self, dpid, grp_id):
        """Lists the MAC addresses that are configured for the specified source MAC group ID on the specified datapath.
           Not supported on all switches. No error is returned if the switch does not support this feature.

        :param str dpid: The datapath ID
        :param str grp_id: The mac group ID to be deleted
        :rtype: List of Mac adresses

        """
        url = (self._of_base_url +
               'datapaths/{0}/srcmacgrps/{1}/macs'.format(urllib.quote(dpid), grp_id))
        return self.restclient.get(url)


#bhg38: created based on 2.7 API spec
    def delete_datapath_dstmacgrps_mac(self, dpid, grp_id, macs):
        """Deletes the specified MAC addresses from the specified destination MAC group ID on the specified datapath.
           Not supported on all switches. No error is returned if the switch does not support this feature.

        :param str dpid: The datapath ID
        :param str grp_id: The mac group ID to be deleted
        :param macs : List of mac @ to delete 

        """
        url = (self._of_base_url +
               'datapaths/{0}/dstmacgrps/{1}/macs'.format(urllib.quote(dpid), grp_id))
        r = self.restclient.delete(url, macs)
        raise_errors(r)

 
    #bhg38: created based on 2.7 API spec
    def add_datapath_srcmacgrps_mac(self, dpid, grp_id, macs):
        """Adds MAC addresses to the specified source MAC group ID on the specified datapath.
           Not supported on all switches. No error is returned if the switch does not support this feature.

        :param str dpid: The datapath ID
        :param str grp_id: The mac group ID to be deleted
        :param macs : List of mac @ to add 

        """
        url = (self._of_base_url +
               'datapaths/{0}/srcmacgrps/{1}/macs'.format(urllib.quote(dpid), grp_id))
        data = {"macs": macs}
        r = self.restclient.post(url, json.dumps(data))
        raise_errors(r)
 


    #bhg38: created based on 2.7 API spec
    def delete_datapath_srcmacgrps_mac(self, dpid, grp_id, macs):
        """Deletes the specified MAC addresses from the specified destination MAC group ID on the specified datapath.
           Not supported on all switches. No error is returned if the switch does not support this feature.

        :param str dpid: The datapath ID
        :param str grp_id: The mac group ID to be deleted
        :param macs : List of mac @ to delete 

        """
        url = (self._of_base_url +
               'datapaths/{0}/srcmacgrps/{1}/macs'.format(urllib.quote(dpid), grp_id))
        data = {"macs": macs}
        r = self.restclient.delete(url, json.dumps(data))
        raise_errors(r)