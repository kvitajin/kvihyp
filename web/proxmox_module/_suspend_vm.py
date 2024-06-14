import requests


def suspend_vm(self, vmid):
    url = f'{self.PROXMOX_HTTP_HOST}/nodes/{self.nodes[0]}/qemu/{vmid}/status/suspend'
    response = requests.post(url, headers=self.csrf_token, cookies=self.ticket, verify=False)
    if response.status_code == 200:
        print(f'VM was suspended {vmid}.')
    else:
        print(f'Could not suspend VM {vmid} :-( {response.reason}')
