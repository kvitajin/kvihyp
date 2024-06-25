import requests


def suspend_vm(self, vmid, node_name=None):
    """
    Suspends a specified virtual machine (VM) on a Proxmox node.

    This method sends a POST request to the Proxmox API to suspend a VM identified by its VM ID (`vmid`). If the `node_name`
    is not specified, it defaults to the first node returned by `get_nodes()`. The method prints a success message if the
    VM is suspended successfully, or an error message if the suspend request fails.

    Args:
        vmid (int): The VM ID of the virtual machine to suspend.
        node_name (str, optional): The name of the node where the VM is located. If not specified, the first node in the
                                   cluster is used. Defaults to None.

    Note:
        - This method requires `self.PROXMOX_HTTP_HOST`, `self.csrf_token`, and `self.ticket` to be set with the Proxmox
          host URL, CSRF prevention token, and authentication ticket, respectively.
        - The method does not return any value but prints the outcome of the suspend request.
    """
    if not node_name:
        node_name = self.get_nodes()[0]
    url = f'{self.PROXMOX_HTTP_HOST}/nodes/{node_name}/qemu/{vmid}/status/suspend'
    response = requests.post(url, headers=self.csrf_token, cookies=self.ticket, verify=False)
    if response.status_code == 200:
        print(f'VM was suspended {vmid}.')
    else:
        print(f'Could not suspend VM {vmid} :-( {response.reason}')
