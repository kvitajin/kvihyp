import requests


def get_spice_config(self, vmid):

    url = f'{self.PROXMOX_HTTP_HOST}/nodes/{self.get_nodes()[0]}/qemu/{vmid}/spiceproxy'
    print(url)
    response = requests.post(url, headers=self.csrf_token, cookies=self.ticket, verify=False)
    if response.status_code == 200:
        self.spice_config = response.json()['data']
        return response.json()['data']
    else:
        raise Exception('Failed to get SPICE configuration')
