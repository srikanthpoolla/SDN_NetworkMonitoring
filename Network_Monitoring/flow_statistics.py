import json
from odl_rest_connector import OdlRestConnector
import networkx as nx
import matplotlib.pyplot as plt
#from flask import Flask, render_template, request, json, redirect

#app = Flask(__name__)


class NetworkMonitor:

    def __init__(self):
        self.netw_conn = OdlRestConnector()
        self.graph = nx.Graph()
        self.nodes = None

    def draw_network_topology_from_edges(self):
        try:
            print 'The Network Edges are: '
            content = self.netw_conn.get_edges()
            edge_properties = json.loads(content)
            odl_edges = edge_properties['edgeProperties']
            for edge in odl_edges:
                e = (edge['edge']['headNodeConnector']['node']['id'], edge['edge']['tailNodeConnector']['node']['id'])
                self.graph.add_edge(*e)
            nx.draw(self.graph, with_labels=True)
            plt.savefig("templates/network_topology.png")
            #import os.path
            #is_topology_exists = os.path.exists("/templates/network_topology.png")
            #if not is_topology_exists:
            #    plt.savefig("templates/network_topology.png")
            #else:
                #print 'Topology Diagram Already Exist'
                #return
            #plt.show()
            # print self.graph
        except Exception as e:
            print e

    def active_hosts(self):
        try:
            print 'The Active Hosts are: '
            active_hosts = self.netw_conn.get_active_hosts()
            return active_hosts
        except Exception as e:
            print e

    def active_switches(self):
        try:
            print 'The Active Switches are: '
            content = self.netw_conn.get_switches()
            return json.loads(content)
        except Exception as e:
            print e

    def packet_metrics(self, flow_id):
        try:
            print 'The Packet Metrics are: '
            content = self.netw_conn.request_flow(flow_id)
            return json.loads(content)
        except Exception as e:
            print e

    def flow_details(self):
        try:
            print 'The Flow Details are: '
            content = self.netw_conn.get_flow_details()
            return json.loads(content)
        except Exception as e:
            print e

    def flow_details_by_switch_id(self, switch_id):
        try:
            print 'The Flow Details are: '
            content = self.netw_conn.get_flow_details_by_switch_id(switch_id)
            return json.loads(content)
        except Exception as e:
            print e

    def each_flow_of_switch(self, switch_id, flow_name):
        try:
            print 'The Flow Details are: '
            content = self.netw_conn.get_each_flow_of_switch(switch_id, flow_name)
            return json.loads(content)
        except Exception as e:
            print e


# @app.route('/')
# def start_point():
#     #return render_template('signup.html')
#     return redirect("http://localhost:4200/index.html")
#     #return redirect("http://localhost:5000/switches")
#
#
# @app.route('/network_monitoring', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         user = request.form['User']
#         password = request.form['Password']
#         return json.dumps({'status': 'OK', 'user': user, 'pass': password})
#         # change return statement and post to UI page after loading with IP, User and Pwd
#
#
# @app.route('/switches')#, methods=['POST', 'GET'])
# def switches():
#     switch_id_list = []
#     net_mon = NetworkMonitor()
#     if request.method == 'POST':
#         # Get all list of switches and return to form
#         active_switches = net_mon.active_switches()
#         for switch in active_switches['nodeProperties']:
#             switch_id_list.append(switch['node']['id'])
#         return json.dumps({'status': 'OK', 'Active_Switches': switch_id_list})
#
#
# @app.route('/flows', methods=['POST', 'GET'])
# def flows():
#     flow_list = []
#     net_mon = NetworkMonitor()
#     if request.method == 'POST':
#         # Get all list of nodes and return to form
#         active_flows = net_mon.flow_details_by_switch_id('00:00:00:00:00:00:00:02')
#         for flow in active_flows['flowConfig']:
#             flow_list.append(flow['name'])
#         return json.dumps({'status': 'OK', 'Active_Flows': flow_list})
#
#
# @app.route('/flow_details', methods=['POST', 'GET'])
# def flow_details():
#     flows_map = {}
#     net_mon = NetworkMonitor()
#     if request.method == 'POST':
#         # Get all list of nodes and return to form
#         flow_details = net_mon.each_flow_of_switch('00:00:00:00:00:00:00:02', 'flow1_switch2')
#         flows_map['Switch ID'] = flow_details['node']['id']
#         flows_map['Ethernet Source'] = flow_details['dlSrc']
#         flows_map['Ethernet Dest'] = flow_details['dlDst']
#         flows_map['Ethernet Type'] = flow_details['etherType']
#         flows_map['Controller Action'] = flow_details['actions']
#         flows_map['IP Source'] = flow_details['nwSrc']
#         flows_map['IP Dest'] = flow_details['nwDst']
#         flows_map['In Port'] = flow_details['ingressPort']
#         return json.dumps({'status': 'OK', 'Flow Details': flows_map})
#
#
# @app.route('/flow_metrics', methods=['POST', 'GET'])
# def flow_metrics():
#     net_mon = NetworkMonitor()
#     if request.method == 'POST':
#         flow_statistics = net_mon.packet_metrics('00:00:00:00:00:00:00:07')
#         action_map = {}
#         metrics_map = {}
#         #packet_count, byte_count, duration_sec, duration_nano_sec = 0, 0, 0, 0
#         #drop_count, drop_byte_count, drop_duration_sec, drop_duration_nano_sec = 0, 0, 0, 0
#         for flow in flow_statistics['flowStatistic']:
#             actions = flow['flow']['actions']
#             interim_map = {}
#             interim_set = []
#             for action in actions:
#                 if isinstance(type(actions), type(list)):
#                     if 'type' in action:
#                         interim_set.append(action['type'])
#                 else:
#                     interim_set.append(action['type'])
#                 interim_map['Action_Type'] = interim_set
#             if 'OUTPUT' in interim_map['Action_Type']:
#                 metrics_map['Packet_Count'] = metrics_map.get('Packet_Count', 0) + flow['packetCount']
#                 metrics_map['Byte_Count'] = metrics_map.get('Byte_Count', 0) + flow['byteCount']
#                 metrics_map['Duration_Seconds'] = metrics_map.get('Duration_Seconds', 0) + flow['durationSeconds']
#                 metrics_map['Duration_Nano_Seconds'] = metrics_map.get('Duration_Nano_Seconds', 0) + flow[
#                     'durationNanoseconds']
#                 action_map['OUTPUT_METRICS'] = metrics_map
#             if 'DROP' in interim_map['Action_Type']:
#                 metrics_map['Drop_Packet_Count'] = metrics_map.get('Drop_Packet_Count', 0) + (flow['packetCount'])
#                 metrics_map['Drop_Byte_Count'] = metrics_map.get('Drop_Byte_Count', 0) + flow['byteCount']
#                 metrics_map['Drop_Duration_Seconds'] = metrics_map.get('Drop_Duration_Seconds', 0) + flow[
#                     'durationSeconds']
#                 metrics_map['Drop_Duration_Nano_Seconds'] = metrics_map.get('Drop_Duration_Nano_Seconds', 0) + flow[
#                     'durationNanoseconds']
#                 action_map['DROP_METRICS'] = metrics_map
#
#         return json.dumps({'status': 'OK', 'Flow Metrics': action_map})
#
#
# if __name__ == '__main__':
#     pass
#     #app.run()
#     #n = NetworkMonitor()
#     #n.flow_details_by_switch_id('00:00:00:00:00:00:00:02')
#     #n.draw_network_topology_from_edges()
#     #print n.flow_details()
#     #n.process_nodes_and_flows()
#     #n.packet_metrics('00:00:00:00:00:00:00:02')
#     #n.active_hosts()
#     #n.get_switches()
#
# #n = NetworkMonitor()
# #n.process_traffic()
# #n.process_nodes_and_flows()
# #n.active_hosts()
# #n.draw_network_topology_from_edges()
# #n.flow_details()
# #n.test_my_method()
#
#     # def process_nodes_and_flows(self):
#     #     try:
#     #         node_map = {}
#     #         node_list = []
#     #         #print 'The Node Details are: '
#     #         # Fetch all nodes and push into a dictionary
#     #         content = self.netw_conn.get_switches()
#     #         json_content = json.loads(content)
#     #         node_details = json_content['nodeProperties']
#     #         #self.nodes = node_details
#     #         for each_node in node_details:
#     #             node_list.append(each_node['node']['id'])
#     #         node_map['nodes'] = node_list
#     #         for each_node in node_map['nodes']:
#     #             pass
#     #             #print 'Node Id: ' + each_node
#     #
#     #         # Fetch flow details for each node
#     #         #print 'X-------------------------X-----------------------X'
#     #         #print 'The Flow Details are: '
#     #         flow_details = []
#     #         for node in node_map['nodes']:
#     #             flow_details.append(json.loads(self.netw_conn.get_flow_details_by_id(node)))
#     #         ########
#     #         return node_map['nodes'], flow_details
#     #         ###########
#     #         if len(flow_details) > 0:
#     #             for flow_detail in flow_details:
#     #                 if len(flow_detail['flowConfig']) > 0:
#     #                     print 'Switch DP ID is: ' + flow_detail['flowConfig'][0]['node']['id']
#     #                     print 'Switch Flow Name is: ' + flow_detail['flowConfig'][0]['name']
#     #                     print 'Switch Ether Type is: ' + flow_detail['flowConfig'][0]['etherType']
#     #                     if 'nwSrc' in flow_detail['flowConfig'][0]:
#     #                         print 'Source IP is: ' + flow_detail['flowConfig'][0]['nwSrc']
#     #                     if 'nwDst' in flow_detail['flowConfig'][0]:
#     #                         print 'Destination IP is: ' + flow_detail['flowConfig'][0]['nwDst']
#     #                     print 'Flow Priority is: ' + flow_detail['flowConfig'][0]['priority']
#     #                     if 'ingressPort' in flow_detail['flowConfig'][0]:
#     #                         print 'Ingress Port is: ' + flow_detail['flowConfig'][0]['ingressPort']
#     #                     print 'X-------------------------X-----------------------X'
#     #     except Exception as e:
#     #         print e





