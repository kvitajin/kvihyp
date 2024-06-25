# TODO nastavit cestu k isu... list existujicich is?

def create_virt_storage(self, storage, vmid, size, node_name=None):
    """
    Creates a virtual storage on a specified node within the Proxmox environment.

    This method initiates the creation of a virtual storage disk for a virtual machine (VM) identified by `vmid`.
    The storage is created within the specified storage resource on the Proxmox node. If `node_name` is not provided,
    the method defaults to using the first node returned by `get_nodes()`. The storage disk is named in a standard
    format and its size is specified by the `size` parameter.

    Args:
        storage (str): The name of the storage resource within Proxmox where the disk will be created.
        vmid (int): The ID of the VM for which the storage disk is being created.
        size (str): The size of the storage disk to be created, specified in a format recognized by Proxmox (e.g., '30G').
        node_name (str, optional): The name of the node on which to create the storage. Defaults to None, in which
                                   case the first node returned by `get_nodes()` is used.

    Returns:
        requests.Response: The response object from the Proxmox API call. Includes status code, success message,
                           or error reason.
    """
    if not node_name:
        node_name = self.get_nodes()[0]
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
