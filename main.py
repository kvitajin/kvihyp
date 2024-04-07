import requests
import secrets
import datetime

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TODO list
#  mazat virtualky      - DONE
#  start                - DONE
#  stop                 - DONE?
#  pause
#  pristup ke konzoli
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
        print(f'im here> \t{data}')
        for row in data['data']:
            print(row)
            self.nodes.append(row['node'])
            # i = i+1
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
                    print(f'Name: {vm["name"]}\n\tcpus: {str(vm["cpus"])} \n\t'
                          f'Cpu usage: {str("{:.2f}".format(vm["cpu"] * 100))}%\n\t'
                          f'Max memory usage: {str(vm["maxmem"] / 1024 / 1024 / 1024)} GiB\n\t'
                          f'Mem usage: {str("{:.3f}".format(vm["mem"] / 1024 / 1024 / 1024))} GiB\n\t'
                          f'Uptime: {str(datetime.timedelta(seconds=vm["uptime"]))}')
                return
        return self.vms
    #function which create new virtual machine
    # arguments: vm_name, max memory, cpus

    def get_virt_storage(self, print_storage=False):
        for node_name in self.get_nodes():
            url = f'{self.PROXMOX_HOST}/nodes/{node_name}/storage'
            response = self.session.get(url, verify=False)
            storages = response.json()
            for storage in storages['data']:
                if print_storage:
                    print(f'Storage: {storage["storage"]}\n\t'
                          f'Used fraction: {"{:.2f}".format(storage["used_fraction"]*100)}%\n\t'
                          f'Shared: {str(storage["shared"])} \n\t'
                          f'Active: {storage["active"]}\n\t'
                          f'Type: {storage["type"]} \n\t'
                          f'Content: {storage["content"]}\n\t'
                          f'Total: {"{:.2f}".format(storage["total"]/1024/1024/1024)}GiB\n\t'
                          f'Used: {"{:.2f}".format(storage["used"]/1024/1024/1024)}GiB\n\t'
                          f'Available: {"{:.2f}".format(storage["avail"]/1024/1024/1024)}GiB\n\t'
                          f'Enabled: {storage["enabled"]}\n\t'
                          )
                return storages

    def get_virt_pokus(self):
        storages = self.get_virt_storage()
        # print(storages)
        for storage in storages['data']:
            urlinside = f'{self.PROXMOX_HOST}/nodes/{self.get_nodes()[0]}/storage/{storage["storage"]}/content'
            response_inside = self.session.get(urlinside, verify=False)
            print(storage)
            print(f'\t{vars(response_inside)}')

    def create_virt_storage(self, storage, vmid, size):
        url = f'{self.PROXMOX_HOST}/nodes/{self.get_nodes()[0]}/storage/{storage}/content'
        print(url)
        data = {'vmid': vmid,
                'filename': f"vm-{vmid}-disk-1",
                'size': size,
                'format': 'raw'
                }
        response = self.session.post(url, data=data, headers=self.csrf_token, cookies={'PVEAuthCookie': self.ticket})
        if response.status_code == 200:
            print(f'uspesne vytvoreno na {storage}')
        else:
            print(f'neco se nepovedlo duvod: {response.reason}')

    def create_vm(self, name, cores, memory, vmid, disk_size, storage="local-lvm"):
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
        virtio = f'{storage}:vm-{vmid}-disk-1'
        data = {
            'vmid': vmid,
            'name': name,
            'memory': memory,
            'cores': cores,
            'net0': 'virtio,bridge=vmbr0',
            'ostype': 'l26',  # Linux 2.6/3.X/4.X
            'ide2': 'none,media=cdrom',
            'bootdisk': 'virtio0',
            'virtio0': virtio
        }
        self.create_virt_storage(storage=storage, size=disk_size, vmid=vmid)
        response = self.session.post(create_url,
                                     data=data,
                                     verify=False, headers=self.csrf_token, cookies={'PVEAuthCookie': self.ticket})
        if response.status_code == 200:
            print("hurray")
        else:
            print(f'oh no {response.text} reason: {response.reason}')

    def delete_vm(self, vmid):
        if not self.nodes:
            url = f'{self.PROXMOX_HOST}/nodes/{self.get_nodes()[0]}/qemu/{vmid}'
        else:
            url = f'{self.PROXMOX_HOST}/nodes/{self.nodes[0]}/qemu/{vmid}'
        response = requests.delete(url, verify=False, headers=self.csrf_token, cookies={'PVEAuthCookie': self.ticket})
        if response.status_code in [200, 202]:
            print(f'VM {vmid}.RIP.')
        else:
            print(f'VM {vmid} is still alive . Error: {response.text} status code:{response.status_code} {response.reason}')

    def get_max_vmid(self):
        if not self.vms:
            self.list_vms(False)
        vmids = []
        for vm in self.vms['data']:
            vmids.append(vm['vmid'])
        # print(vmids)
        return max(vmids)

    def start_vm(self, vmid):
        url = f'{self.PROXMOX_HOST}/nodes/{self.nodes[0]}/qemu/{vmid}/status/start'
        response = requests.post(url, headers=self.csrf_token, cookies={'PVEAuthCookie': self.ticket}, verify=False)
        if response.status_code == 200:
            print(f'Run Forest VM {vmid}.')
        else:
            print(f'VM {vmid} is still sleeping :-( {response.reason}')

    def stop_vm(self, vmid):
        url = f'{self.PROXMOX_HOST}/nodes/{self.nodes[0]}/qemu/{vmid}/status/stop'
        response = requests.post(url, headers=self.csrf_token, cookies={'PVEAuthCookie': self.ticket}, verify=False)
        if response.status_code == 200:
            print(f'VM stopped {vmid}.')
        else:
            print(f'Could not stop VM {vmid} :-( {response.reason}')


if __name__ == '__main__':

    connection = Connection()
    # connection.get_nodes()
    # vms = connection.list_vms(False)
    # print(vms['data'])
    # connection.create_vm(name="pokus", cores=1, memory=512, vmid=connection.get_max_vmid()+1, disk_size=32)
    # connection.create_vm(name="pokus", cores=1, memory=512, vmid=112, disk_size=32)
    # connection.delete_vm(vmid=112)
    # print(connection.get_max_vmid())
    # connection.start_vm(112)
    # connection.stop_vm(112)
    # connection.get_virt_storage()
    # connection.get_virt_pokus()
    # connection.create_virt_storage(storage="local-lvm", size=1024, vmid=112)
    connection.create_vm(name="vyser-si-oko",
                         cores=2,
                         memory=1024,
                         vmid=connection.get_max_vmid()+1,
                         disk_size=1024,
                         storage="local-lvm")
