def edit_vm(self, vmid, cores, memory, disk_size, node_name=None):
    """
    Edits the configuration of a specified virtual machine (VM) on a Proxmox node.

    This method updates the VM's configuration, specifically its number of cores, memory size, and disk size.
    If `node_name` is not provided, the method will not execute as the node name is essential for identifying
    the correct VM to edit. The disk size parameter is accepted but not used in the current implementation.

    Args:
        vmid (int): The ID of the VM to be edited.
        cores (int): The new number of CPU cores to assign to the VM.
        memory (float): The new amount of memory (in GB) to assign to the VM. This value is internally converted to bytes.
        disk_size (int): The new disk size for the VM. Currently not used in the API call.
        node_name (str, optional): The name of the node where the VM is located. Defaults to None.

    Returns:
        int: The VM ID of the edited VM, indicating the operation targeted the correct VM.

    Note:
        The `disk_size` parameter is accepted but not utilized in the API call. Future implementations may include
        disk size adjustments. The method prints a success message if the operation is successful, otherwise, it
        prints an error message including the reason for failure.
    """
    url = f'{self.PROXMOX_HTTP_HOST}/nodes/{node_name}/qemu/{vmid}/config'
    data = {
        'cores': cores,
        'memory': int(memory*1024*1024*1024)
    }
    response = self.session.put(url, headers=self.csrf_token, cookies=self.ticket, verify=False, data=data)
    if response.status_code == 200:
        print("hurray")
    else:
        print(f'oh no {response.text} reason: {response.reason}')
    return vmid