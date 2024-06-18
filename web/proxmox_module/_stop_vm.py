import requests


def stop_vm(self, vmid, node_name=None):
    if not node_name:
        node_name = self.get_nodes()[0]
    url = f'{self.PROXMOX_HTTP_HOST}/nodes/{node_name}/qemu/{vmid}/status/stop'
    response = requests.post(url, headers=self.csrf_token, cookies=self.ticket, verify=False)
    if response.status_code == 200:
        print(f'VM stopped {vmid}.')
    else:
        print(f'Could not stop VM {vmid} :-( {response.reason}')