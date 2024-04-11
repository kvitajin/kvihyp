import requests


def delete_vm(self, vmid):
    if not self.nodes:
        url = f'{self.PROXMOX_HTTP_HOST}/nodes/{self.get_nodes()[0]}/qemu/{vmid}'
    else:
        url = f'{self.PROXMOX_HTTP_HOST}/nodes/{self.nodes[0]}/qemu/{vmid}'
    response = requests.delete(url, verify=False, headers=self.csrf_token, cookies=self.ticket)
    if response.status_code in [200, 202]:
        print(f'VM {vmid}.RIP.')
    else:
        print(f'VM {vmid} is still alive . Error: {response.text} status code:{response.status_code} {response.reason}')
