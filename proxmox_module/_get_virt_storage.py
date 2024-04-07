def get_virt_storage(self, print_storage=False):
    # function which create new virtual machine
    # arguments: vm_name, max memory, cpus
    for node_name in self.get_nodes():
        url = f'{self.PROXMOX_HOST}/nodes/{node_name}/storage'
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
            return storages
