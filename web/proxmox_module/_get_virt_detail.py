import datetime
import json

def get_virt_detail(self, node_name=None, storage_name=None):
    if not node_name:
        node_name = self.get_nodes()[0]
    urlinside = f'{self.PROXMOX_HTTP_HOST}/nodes/{node_name}/storage/{storage_name}/content'
    response_inside = self.session.get(urlinside, verify=False)
    storages = response_inside.json()
    return storages['data']


# TODO tohle chce formatovani, jak prase drbani