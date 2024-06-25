import datetime
import json

def get_virt_detail(self, node_name=None, storage_name=None):
    """
    Retrieves the details of virtual storage on a specified node within the Proxmox environment.

    This method sends a GET request to the Proxmox API to fetch the details of the virtual storage
    specified by `storage_name` on the node specified by `node_name`. If `node_name` is not provided,
    the method defaults to using the first node returned by `get_nodes()`. The response includes
    details such as the volume's name, size, and type.

    Args:
        node_name (str, optional): The name of the node on which the storage resides. Defaults to None,
                                   in which case the first node returned by `get_nodes()` is used.
        storage_name (str, optional): The name of the storage to retrieve details for. Defaults to None.

    Returns:
        list: A list of dictionaries, each representing a storage volume's details on the specified node.
    """
    if not node_name:
        node_name = self.get_nodes()[0]
    urlinside = f'{self.PROXMOX_HTTP_HOST}/nodes/{node_name}/storage/{storage_name}/content'
    response_inside = self.session.get(urlinside, verify=False)
    storages = response_inside.json()
    return storages['data']


# TODO tohle chce formatovani, jak prase drbani