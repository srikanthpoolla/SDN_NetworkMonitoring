from flow_statistics import NetworkMonitor
import web
import json
import base64


urls = (
    '/network_monitoring', 'HomePage',
    '/network_monitoring/login', 'LoginPage',
    '/switches', 'Switches',
    '/flows/node/(.*)', 'GetFlows',
    '/flow_details/node/(.*)/flow/(.*)', 'GetFlowDetails',
    '/flow_metrics/node/(.*)', 'GetFlowMetrics',
    '/network_monitoring/topology', 'GetNetworkTopology'
)

app = web.application(urls, globals())


class HomePage:

    def __init__(self):
        pass

    def GET(self):
        return web.redirect("http://localhost:4200/index.html")


class LoginPage:

    def __init__(self):
        pass

    def OPTIONS(self):
        #web.header('Access-Control-Allow-Origin', "http://localhost:4200")
        #web.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        #web.header('Access-Control-Allow-Credentials', 'true')
        return self.POST()

    def POST(self):
        web.header('Access-Control-Allow-Origin', "http://localhost:4200")
        web.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        web.header('Access-Control-Allow-Credentials', 'true')
        data = json.loads(web.data())
        username = data["username"]
        password = data["password"]
        if username == 'admin' and password == 'admin':
            print 'inside'
            return json.dumps({'status': 'OK', 'Reason': "Success"})
        else:
            return json.dumps({'status': 'OK', 'Reason': "Username or Password is wrong "})


class Switches:

    def __init__(self):
        pass

    def GET(self):
        #switch_map = {}
        count = 1
        web.header('Access-Control-Allow-Origin', "http://localhost:4200")
        web.header('Access-Control-Allow-Methods', 'GET')
        web.header('Access-Control-Allow-Credentials', 'true')
        switch_list = []
        net_mon = NetworkMonitor()
        # Get all list of switches and return to form
        active_switches = net_mon.active_switches()
        for switch in active_switches['nodeProperties']:
            switch_map = {}
            switch_map['id'] = count
            switch_map['name'] = switch['node']['id']
            switch_list.append(switch_map)
            count += 1

        return json.dumps({'status': 'OK', 'Active_Switches': switch_list})


class GetFlows:

    def __init__(self):
        pass

    def GET(self, switch_id):
        web.header('Access-Control-Allow-Origin', "http://localhost:4200")
        web.header('Access-Control-Allow-Methods', 'GET')
        web.header('Access-Control-Allow-Credentials', 'true')
        flow_list = []
        net_mon = NetworkMonitor()

        # Get list of flows for the passed switch_id #
        active_flows = net_mon.flow_details_by_switch_id(switch_id)
        for flow in active_flows['flowConfig']:
            flow_list.append(flow['name'])
        return json.dumps({'status': 'OK', 'Active_Flows': flow_list})


class GetFlowDetails:

    def __init__(self):
        pass

    def GET(self, switch_id, flow_name):
        web.header('Access-Control-Allow-Origin', "http://localhost:4200")
        web.header('Access-Control-Allow-Methods', 'GET')
        web.header('Access-Control-Allow-Credentials', 'true')
        flows_map = {}
        net_mon = NetworkMonitor()

        # Get the list of flow details #

        flow_details = net_mon.each_flow_of_switch(switch_id, flow_name)
        flows_map['Switch_ID'] = flow_details['node']['id']
        if 'dlSrc' in flow_details:
            flows_map['Ethernet_Source'] = flow_details['dlSrc']
        if 'dlDst' in flow_details:
            flows_map['Ethernet_Dest'] = flow_details['dlDst']
        if 'etherType' in flow_details:
            flows_map['Ethernet_Type'] = flow_details['etherType']
        if 'actions' in flow_details:
            flows_map['Controller_Action'] = flow_details['actions']
        if 'nwSrc' in flow_details:
            flows_map['IP_Source'] = flow_details['nwSrc']
        if 'nwDst' in flow_details:
            flows_map['IP_Dest'] = flow_details['nwDst']
        if 'ingressPort' in flow_details:
            flows_map['In_Port'] = flow_details['ingressPort']
        return json.dumps({'status': 'OK', 'Flow_Details': flows_map})


class GetFlowMetrics:

    def __init__(self):
        pass

    def GET(self, switch_id):
        web.header('Access-Control-Allow-Origin', "http://localhost:4200")
        web.header('Access-Control-Allow-Methods', 'GET')
        web.header('Access-Control-Allow-Credentials', 'true')
        net_mon = NetworkMonitor()
        flow_statistics = net_mon.packet_metrics(switch_id)
        action_map = {}
        flow_metrics_map = {}
        drop_metrics_map = {}

        for flow in flow_statistics['flowStatistic']:
            actions = flow['flow']['actions']
            interim_map = {}
            interim_set = []
            for action in actions:
                if isinstance(type(actions), type(list)):
                    if 'type' in action:
                        interim_set.append(action['type'])
                else:
                    interim_set.append(action['type'])
                interim_map['Action_Type'] = interim_set
            if 'OUTPUT' in interim_map['Action_Type']:
                flow_metrics_map['Packet_Count'] = flow_metrics_map.get('Packet_Count', 0) + flow['packetCount']
                flow_metrics_map['Byte_Count'] = flow_metrics_map.get('Byte_Count', 0) + flow['byteCount']
                flow_metrics_map['Duration_Seconds'] = flow_metrics_map.get('Duration_Seconds', 0) + flow['durationSeconds']
                flow_metrics_map['Duration_Nano_Seconds'] = flow_metrics_map.get('Duration_Nano_Seconds', 0) + flow[
                    'durationNanoseconds']
                action_map['OUTPUT_METRICS'] = flow_metrics_map
            if 'DROP' in interim_map['Action_Type']:
                drop_metrics_map['Drop_Packet_Count'] = drop_metrics_map.get('Drop_Packet_Count', 0) + (flow['packetCount'])
                drop_metrics_map['Drop_Byte_Count'] = drop_metrics_map.get('Drop_Byte_Count', 0) + flow['byteCount']
                drop_metrics_map['Drop_Duration_Seconds'] = drop_metrics_map.get('Drop_Duration_Seconds', 0) + flow[
                    'durationSeconds']
                drop_metrics_map['Drop_Duration_Nano_Seconds'] = drop_metrics_map.get('Drop_Duration_Nano_Seconds', 0) + flow[
                    'durationNanoseconds']
                action_map['DROP_METRICS'] = drop_metrics_map

        return json.dumps({'status': 'OK', 'Flow_Metrics': action_map})


class GetNetworkTopology:

    def __init__(self):
        pass

    def GET(self):
        web.header('Access-Control-Allow-Origin', "http://localhost:4200")
        web.header('Access-Control-Allow-Methods', 'GET')
        web.header('Access-Control-Allow-Credentials', 'true')
        net_mon = NetworkMonitor()
        import os.path
        is_topology_exists = os.path.exists("templates/network_topology.png")
        if not is_topology_exists:
            net_mon.draw_network_topology_from_edges()
        encoded = base64.b64encode(open("templates/network_topology.png", "rb").read())
        return json.dumps({'status': 'OK', 'Network_Topology': encoded})


if __name__ == "__main__":
    app.run()
