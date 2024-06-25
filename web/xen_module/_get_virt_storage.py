def get_virt_storage(self, print_storage=False, node_names=None):
    """
    Retrieves virtual storage information from the Xen server.

    This method fetches all storage repositories (SR) records from the Xen server and calculates the used, free, and total
    storage space for each. It can either print the storage information directly or return it as a list of dictionaries,
    depending on the `print_storage` flag.

    Args:
        print_storage (bool, optional): If True, prints the storage information. Otherwise, returns the information as a list.
                                        Defaults to False.
        node_names (list, optional): A list of node names to filter the storage repositories. Currently not used in the method.

    Returns:
        list: A list of dictionaries containing storage information, including the name, used fraction, whether it's shared,
              total size, available size, used size, and type of each storage repository. This is returned only if `print_storage`
              is False.

    Note:
        - The method currently does not use the `node_names` parameter, but it is included for future expansion.
        - The storage sizes are converted to GiB for readability.
        - A divide by zero check is performed to avoid calculation errors when `storage_max` is 0.
    """
    SR = self.server.SR.get_all_records(self.session_id)['Value']
    storages = []
    for opaque_ref, storage in SR.items():
        storage_max = int(storage["physical_size"])
        storage_used = int(storage["physical_utilisation"])
        storage_free = storage_max - storage_used
        if storage_max != 0:
            used_perc = storage_used / storage_max * 100
        else:
            used_perc = 0

        if print_storage:
            print(f'Storage: {storage["name_label"]}\n\t'
                  f'Used fraction: {"{:.2f}".format(used_perc)}%\n\t'    #TODO: divide by zero
                  f'Shared: {str(storage["shared"])} \n\t'
                  f'Type: {storage["type"]} \n\t'
                  f'Content: {storage["content_type"]}\n\t'
                  f'Total: {"{:.2f}".format(storage_max / 1024 / 1024 / 1024)}GiB\n\t'
                  f'Used: {"{:.2f}".format(storage_used / 1024 / 1024 / 1024)}GiB\n\t'
                  f'Available: {"{:.2f}".format(storage_free / 1024 / 1024 / 1024)}GiB\n\t'
                  )
        else:
            storages.append({'storage': storage["name_label"],
                             'used_fraction': "{:.2f}".format(used_perc),
                             'shared': storage['shared'],
                             'total': round(float(storage_max / 1024 / 1024 / 1024), 2),
                             'avail': round(float(storage_free / 1024 / 1024 / 1024), 2),
                             'used': round(float(storage_used / 1024 / 1024 / 1024), 2),
                             'type': storage['type']
                             })
    return storages
