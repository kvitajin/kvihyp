import requests


def stop_vm(self, vmid):
    url = f'{self.PROXMOX_HOST}/nodes/{self.nodes[0]}/qemu/{vmid}/status/stop'
    response = requests.post(url, headers=self.csrf_token, cookies=self.ticket, verify=False)
    if response.status_code == 200:
        print(f'VM stopped {vmid}.')
    else:
        print(f'Could not stop VM {vmid} :-( {response.reason}')