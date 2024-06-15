import datetime


def get_virt_detail(self, node_name=None, storage_name=None):
    if not node_name:
        node_name = self.get_nodes()[0]
    data = []
    urlinside = f'{self.PROXMOX_HTTP_HOST}/nodes/{node_name}/storage/{storage_name}/content'
    response_inside = self.session.get(urlinside, verify=False)
    storages = response_inside.json()
    data.append({'storage': storage_name, 'content': storages['data']})
    print(storages['data'])
    tmp = storages['data']
    print (f'tmp {tmp}\n')
    for storage in tmp:
        data.append({"ctime": str(datetime.timedelta(seconds=storage["ctime"])),
                      "volid": storage["volid"],
                      "size": storage["size"]/1024/1024/1024,
                      "format": storage["format"],
                      "content": storage["content"],
                      "vmid": storage["vmid"]})

        # print(storage)
        # print(f'\t{vars(response_inside)}')
    return data

# TODO tohle chce formatovani, jak prase drbani