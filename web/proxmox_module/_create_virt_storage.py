# TODO nastavit cestu k isu... list existujicich is?

def create_virt_storage(self, storage, vmid, size, node_name=None):
    if not node_name:
        node_name = self.get_nodes()[0]
    print("IM in create storage")
    url = f'{self.PROXMOX_HTTP_HOST}/nodes/{node_name}/storage/{storage}/content'
    data = {'vmid': vmid,
            'filename': f"vm-{vmid}-disk-1",
            'size': size,
            'format': 'raw'
            }
    response = self.session.post(url, data=data, headers=self.csrf_token, cookies=self.ticket)
    if response.status_code == 200:
        print(f'uspesne vytvoreno na {storage}')
    else:
        print(f'neco se nepovedlo duvod: {response.reason}')
