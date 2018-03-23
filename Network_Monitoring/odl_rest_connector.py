import httplib2
import json
import ConfigParser
from flask import Flask,render_template, request, json, redirect

app = Flask(__name__)


'''
---REST Call APIs---
http://192.168.91.101:8080/controller/nb/v2/flowprogrammer/default/node/OF/00:00:00:00:00:00:00:01
http://192.168.91.101:8080/controller/nb/v2/flowprogrammer/default/node/OF/00:00:00:00:00:00:00:01/staticFlow/Flow1
http://192.168.91.101:8080/controller/nb/v2/flowprogrammer/default/
http://192.168.91.101:8080/restconf/operational/network-topology:network-topology
http://192.168.91.101:8080/controller/nb/v2/statistics/default/flow/node/OF/00:00:00:00:00:00:00:06/
'''


class OdlRestConnector:

    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        self.config.read('config.properties')
        username = self.config.get('dashboard_creds', 'user')
        password = self.config.get('dashboard_creds', 'password')
        self.ip = self.config.get('odl_controller', 'ip')
        self.req_obj = httplib2.Http(".cache")
        self.base_url = 'http://192.168.91.101:8080'
        self.req_obj.add_credentials(username, password)

    def request_flow(self, flow_id):
        resp, content = self.req_obj.request(
            self.base_url + '/controller/nb/v2/statistics/default/flow/node/OF/' + flow_id, "GET")
        return content

    def get_switches(self):
        resp, content = self.req_obj.request(
            self.base_url + '/controller/nb/v2/switchmanager/default/nodes', "GET")
        return content

    def get_edges(self):
        resp, content = self.req_obj.request(
            self.base_url + '/controller/nb/v2/topology/default', "GET")
        return content

    def get_flow_details(self):
        resp, content = self.req_obj.request(
            self.base_url + '/controller/nb/v2/flowprogrammer/default', 'GET')
        return content

    def get_flow_details_by_switch_id(self, flow_id):
        resp, content = self.req_obj.request(
            self.base_url + '/controller/nb/v2/flowprogrammer/default'
            '/node/OF/' + flow_id, 'GET')
        return content

    def get_active_hosts(self):
        resp, content = self.req_obj.request(
            self.base_url + '/controller/nb/v2/hosttracker/default/hosts/active/', "GET")
        host_config = json.loads(content)
        hosts = host_config['hostConfig']
        return hosts

    def get_each_flow_of_switch(self, switch_id, flow_name):
        resp, content = self.req_obj.request(
            self.base_url + '/controller/nb/v2/flowprogrammer/default/node/'
                            'OF/' + switch_id + '/staticFlow/' + flow_name, "GET")
        return content


@app.route('/')
def start_point():
    return render_template('signup.html')


@app.route('/network_monitoring', methods=['POST', 'GET'])
def get_details():
    if request.method == 'POST':
        user = request.form['User']
        password = request.form['Password']
        return json.dumps({'status': 'OK', 'user': user, 'pass': password})
        # change return statement and poin to UI page after loading with IP, User and Pwd


if __name__ == '__main__':
    app.run()
