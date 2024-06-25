def get_virt_storage(self, print_storage=False, node_names=None):
    """
    Retrieves virtual storage information from specified Proxmox nodes.

    This method fetches the virtual storage details from the Proxmox cluster for the given nodes. If no node names are
    provided, it defaults to the first node returned by `get_nodes()`. The method can either print the storage details
    directly or return them as a list of dictionaries, based on the `print_storage` flag.

    Args:
        print_storage (bool, optional): If True, prints the storage details directly. If False, returns the storage
                                        details as a list of dictionaries. Defaults to False.
        node_names (list, optional): A list of node names from which to retrieve storage information. If not provided,
                                     defaults to the first node returned by `get_nodes()`.

    Returns:
        list: A list of dictionaries containing storage details for each storage on the specified nodes. Each dictionary
              includes storage name, used fraction, whether it's shared, active, type, content, total size, used size,
              available size, and whether it's enabled. This return value is provided only if `print_storage` is False.

    Note:
        If `print_storage` is True, the method does not return any value but prints the storage details directly.
    """
    if not node_names:
        node_names = self.get_nodes()[0]
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
