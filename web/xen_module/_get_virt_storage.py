def get_virt_storage(self, print_storage=False, node_names=None):
    # print(self.server.SR.get_all(self.session_id))
    SR = self.server.SR.get_all_records(self.session_id)['Value']
    print(SR)
    # for sr in SR:
    #     print(sr)
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
            # print(storage)
            print(f'Storage: {storage["name_label"]}\n\t'
                  f'Used fraction: {"{:.2f}".format(used_perc)}%\n\t'    #TODO: divide by zero
                  f'Shared: {str(storage["shared"])} \n\t'
                  # f'Active: {storage["active"]}\n\t'
                  f'Type: {storage["type"]} \n\t'
                  f'Content: {storage["content_type"]}\n\t'
                  f'Total: {"{:.2f}".format(storage_max / 1024 / 1024 / 1024)}GiB\n\t'
                  f'Used: {"{:.2f}".format(storage_used / 1024 / 1024 / 1024)}GiB\n\t'
                  f'Available: {"{:.2f}".format(storage_free / 1024 / 1024 / 1024)}GiB\n\t'
                  # f'Enabled: {storage["enabled"]}\n\t'
                  )
        else:
            storages.append({'storage': storage["name_label"],
                             'total': round(float(storage_max / 1024 / 1024 / 1024), 2),
                             'avail': round(float(storage_free / 1024 / 1024 / 1024), 2),
                             'used': round(float(storage_used / 1024 / 1024 / 1024), 2),
                             # 'enabled': float(storage['enabled']),
                             'type': storage['type']
                             })


    return storages