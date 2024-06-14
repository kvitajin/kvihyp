def get_virt_detail(self):
    storages = self.get_virt_storage()
    # print(storages)
    for storage in storages['data']:
        urlinside = f'{self.PROXMOX_HTTP_HOST}/nodes/{self.get_nodes()[0]}/storage/{storage["storage"]}/content'
        response_inside = self.session.get(urlinside, verify=False)
        print(storage)
        print(f'\t{vars(response_inside)}')

# TODO tohle chce formatovani, jak prase drbani