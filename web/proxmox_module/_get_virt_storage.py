def get_virt_storage(self, print_storage=False, node_names=None):
    # function which create new virtual machine
    # arguments: vm_name, max memory, cpus
    if not node_names:
        self.get_nodes()
    data = []
    for node_name in node_names:
        url = f'{self.PROXMOX_HTTP_HOST}/nodes/{node_name}/storage'
        response = self.session.get(url, verify=False)
        storages = response.json()
        for storage in storages['data']:
            if print_storage:
                print(f'Storage: {storage["storage"]}\n\t'
                      f'Used fraction: {"{:.2f}".format(storage["used_fraction"] * 100)}%\n\t'
                      f'Shared: {str(storage["shared"])} \n\t'
                      f'Active: {storage["active"]}\n\t'
                      f'Type: {storage["type"]} \n\t'
                      f'Content: {storage["content"]}\n\t'
                      f'Total: {"{:.2f}".format(storage["total"] / 1024 / 1024 / 1024)}GiB\n\t'
                      f'Used: {"{:.2f}".format(storage["used"] / 1024 / 1024 / 1024)}GiB\n\t'
                      f'Available: {"{:.2f}".format(storage["avail"] / 1024 / 1024 / 1024)}GiB\n\t'
                      f'Enabled: {storage["enabled"]}\n\t'
                      )
            else:
                data.append({'storage': storage['storage'],
                             'used_fraction': "{:.2f}".format(storage["used_fraction"] * 100),
                             'shared': storage['shared'],
                             'active': storage['active'],
                             'type': storage['type'],
                             'content': storage['content'],
                             'total': "{:.2f}".format(storage["total"] / 1024 / 1024 / 1024),
                             'used': "{:.2f}".format(storage["used"] / 1024 / 1024 / 1024),
                             'avail': "{:.2f}".format(storage["avail"] / 1024 / 1024 / 1024),
                             'enabled': storage['enabled']
                             })

    if not data:
        return storages['data']
    return data
