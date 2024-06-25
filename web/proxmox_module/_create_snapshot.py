import datetime


def create_snapshot(self, vmid, node_name=None):
    """
    Creates a snapshot for a specified virtual machine (VM) on a Proxmox node.

    This method generates a snapshot for a VM identified by `vmid`. If `node_name` is not provided,
    the snapshot is created on the first node returned by `get_nodes()`. The snapshot name is
    automatically generated based on the VM ID and the current timestamp.

    Args:
        vmid (int): The ID of the VM for which to create a snapshot.
        node_name (str, optional): The name of the node on which the VM resides. Defaults to None,
                                   in which case the first node returned by `get_nodes()` is used.

    Returns:
        requests.Response: The response object from the Proxmox API call. Includes status code,
                           snapshot creation success message, or error reason.
    """
    if not node_name:
        node_name = self.get_nodes()[0]

    snapname = f"snapshot-{vmid}-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}"

    url = f"{self.PROXMOX_HTTP_HOST}/nodes/{node_name}/qemu/{vmid}/snapshot"

    data = {
        'snapname': snapname,
    }
    response = self.session.post(url, data=data, headers=self.csrf_token, cookies=self.ticket, verify=False)
    if response.status_code == 200:
        print(f'snapshot uspesne vytvoren')
    else:
        print(f'neco se nepovedlo, duvod: {response.reason}')
    return response
