import requests


def delete_vm(self, vmid, node_name=None):
    """
    Deletes a virtual machine (VM) from a specified node in the Proxmox cluster.

    This method sends a DELETE request to the Proxmox API to remove a VM identified by `vmid`.
    If `node_name` is not provided, the method defaults to using the first node returned by `get_nodes()`.
    The method prints a confirmation message if the deletion is successful, or an error message if it fails.

    Args:
        vmid (int): The ID of the VM to be deleted.
        node_name (str, optional): The name of the node from which the VM will be deleted. Defaults to None,
                                   in which case the first node returned by `get_nodes()` is used.

    Returns:
        None: This method prints the outcome of the deletion attempt and does not return a value.
    """
    if not node_name:
        node_name = self.get_nodes()[0]
    url = f'{self.PROXMOX_HTTP_HOST}/nodes/{node_name}/qemu/{vmid}'
    response = requests.delete(url, verify=False, headers=self.csrf_token, cookies=self.ticket)
    if response.status_code in [200, 202]:
        print(f'VM {vmid}.RIP.')
    else:
        print(f'VM {vmid} is still alive . Error: {response.text} status code:{response.status_code} {response.reason}')
