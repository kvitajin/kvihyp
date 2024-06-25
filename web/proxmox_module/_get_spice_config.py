import requests


def get_spice_config(self, vmid):
    """
    Retrieves the SPICE configuration for a specified virtual machine (VM) from a Proxmox node.

    This method sends a POST request to the Proxmox API to fetch the SPICE proxy configuration for a VM identified by `vmid`.
    The method automatically selects the first node returned by `get_nodes()` for the request. If the request is successful,
    the SPICE configuration data is stored in `self.spice_config` and returned. If the request fails, an exception is raised
    indicating the failure to retrieve the SPICE configuration.

    Args:
        vmid (int): The ID of the VM for which to retrieve the SPICE configuration.

    Returns:
        dict: The SPICE configuration data for the specified VM if the request is successful.

    Raises:
        Exception: If the request fails, indicating an issue with retrieving the SPICE configuration.
    """
    url = f'{self.PROXMOX_HTTP_HOST}/nodes/{self.get_nodes()[0]}/qemu/{vmid}/spiceproxy'
    print(url)
    try:
        response = requests.post(url, headers=self.csrf_token, cookies=self.ticket, verify=False)
        if response.status_code == 200:
            self.spice_config = response.json()['data']
            return response.json()['data']
        else:
            raise Exception('Failed to get SPICE configuration')
    except Exception as e:
        print(e)
        return None
