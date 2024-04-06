import certifi
import requests
from requests.auth import HTTPBasicAuth
import ssl
import urllib.request
import urlopen
import secrets
import json
import datetime

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Connection:
    session = ""
    nodes_response = ""
    nodes = []
    ticket = ""
    csrf_token = ""
    vms = ""

    def __init__(self):
        #TODO udelat nabidku, kde se zapise
        self.PROXMOX_HOST = secrets.PROXMOX_HOST
        self.USERNAME = secrets.USERNAME
        self.PASSWORD = secrets.PASSWORD

        auth_url = f'{self.PROXMOX_HOST}/access/ticket'
        auth_data = {'username': self.USERNAME, 'password': self.PASSWORD}
        response = requests.post(auth_url, data=auth_data, verify=False)
        auth_response = response.json()
        self.ticket = auth_response['data']['ticket']
        CSRFPreventionToken = auth_response['data']['CSRFPreventionToken']

        # Create a session for subsequent requests
        self.session = requests.Session()
        self.csrf_token = {'CSRFPreventionToken': CSRFPreventionToken}
        self.session.headers.update(self.csrf_token)
        self.session.cookies['PVEAuthCookie'] = self.ticket
        # session.debug = session.post(auth_url,data={"username": "{}".format(USERNAME),  "password": "{}".format(PASSWORD)},verify=False)
        # print( vars(session.debug))
        # Step 2: Use the token to perform requests
        nodes_url = f'{self.PROXMOX_HOST}/nodes'
        self.nodes_response = self.session.get(nodes_url, verify=False)
        # nodes_response = session.get(nodes_url)
        # i = 0
        # for node in nodes_response:
        #     print("node: " + str(i) + "\n")
        #     print(node.json())
        #     i = i+1
        # print(vars(nodes_response))

# Returns list of nodes , for me pve-precision
    def get_nodes(self):
        data = self.nodes_response.json()
        self.nodes.clear()
        i = 0
        # print(data['data'])
        for row in data['data']:
            # print(row['node'])
            self.nodes.append(row['node'])
            i = i+1
        if not self.nodes:
            raise Exception('No nodes found')
        return self.nodes
# print(data['data'][0]['node'])

    def list_vms(self, print_vms=False):
        # print (self.get_nodes()[0])
        # for i in self.nodes:
        #     print(i['data']['name'])
        # print(self.nodes)
        for node_name in self.get_nodes():
            vms_url = f'{self.PROXMOX_HOST}/nodes/{node_name}/qemu/'
            self.nodes_response = self.session.get(vms_url, verify=False)
            self.vms = self.nodes_response.json()
            if print_vms:
                for vm in self.vms['data']:
                    print("Name: " + vm['name'] + "\n" + "\t cpus: " + str(vm['cpus']) + "\n" +
                          "\t Cpu usage: " + str("{:.2f}".format(vm['cpu'] * 100)) + "%\n" +
                          "\t Max memory usage: " + str(vm['maxmem'] / 1024 / 1024 / 1024) +
                          "GiB\n\t Mem usage:" + str("{:.3f}".format(vm['mem'] / 1024 / 1024 / 1024)) +
                          "GiB\n\t Uptime: " + str(datetime.timedelta(seconds=vm['uptime'])))
                return
        return self.vms
    #function which create new virtual machine
    # arguments: vm_name, max memory, cpus

    def create_vm(self, name, cores, memory, vmid):
        # vms_url = f'{self.PROXMOX_HOST}/'
        # self.vms_response = self.session.get(vms_url, verify=False)
        if not self.nodes:
            create_url = f'{self.PROXMOX_HOST}/nodes/{self.get_nodes()[0]}/qemu'
        else:
            create_url = f'{self.PROXMOX_HOST}/nodes/{self.nodes[0]}/qemu'
        print(create_url)
        # data = {'name': vm_name, 'cpus': vm_cpus, 'maxmem': vm_memory}
        # headers = {
        #     'CSRFPreventionToken': self.csrf_token,
        #     'Cookie': f'PVEAuthCookie={self.ticket}'
        # }
        data = {
            'vmid': vmid,
            'name': name,
            'memory': memory,
            'cores': cores

        }

        response = self.session.post(create_url,
                                     data=data,
                                     verify=False, headers=self.csrf_token, cookies={'PVEAuthCookie': self.ticket})
        if response.status_code == 200:
            print("hurray")
        else:
            print("oh no " + response.text)

    def get_max_vmid(self):
        if not self.vms:
            self.list_vms(False)
        vmids=[]
        for vm in self.vms['data']:
            vmids.append(vm['vmid'])
        # print(vmids)
        return max(vmids)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    connection = Connection()
    # connection.get_nodes()
    # vms = connection.list_vms(False)
    # print(vms['data'])
    connection.create_vm(name="pokus", cores=1, memory=512, vmid=connection.get_max_vmid()+1, )
    # print(connection.get_max_vmid())

