import os
import sys
import django
from datetime import datetime, timezone
import subprocess
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Vm


def get_virt_storage(self, print_storage=False, node_names=None):
    """
    Retrieves virtual storage information for VMs on a specified node.

    This function filters VM instances by the first node name provided in the `node_names` list. For each VM, it calculates
    the used and available storage space, then compiles and returns a list of dictionaries with detailed storage information
    for each VM. The information includes the VM's name, used and available storage space, total disk size, and other relevant
    details.

    Args:
        print_storage (bool, optional): If True, prints the storage information. Defaults to False.
        node_names (list, optional): A list of node names to filter the VMs by. Currently, only the first node name is used.

    Returns:
        list: A list of dictionaries, each containing storage information for a VM. Includes the VM's name, used and available
              storage space, total disk size, and other details.

    Note:
        - The storage space is calculated based on the VM's disk size attribute and the actual file size on disk.
        - The function assumes that the `storage` attribute of a VM instance contains the path to its disk image file.
        - The `enabled`, `type`, and `vmid` fields in the returned dictionaries are hardcoded for demonstration purposes.
    """
    tmp = Vm.objects.filter(connection__host=node_names[0])
    formdata = []

    for i in tmp:
        storage_used = os.path.getsize(i.storage)
        storage_free = float(i.disk_size)*1024*1024*1024 - storage_used
        formdata.append({'storage': i.name,
                         'used_fraction': 0,
                         'shared': False,
                         'total': i.disk_size,
                         'avail': round(float(storage_free / 1024 / 1024 / 1024), 2),
                         'used': round(float(storage_used / 1024 / 1024 / 1024), 2),
                         'enabled': True,
                         'type': 'qcow2',
                         'vmid': i.id,
                         })
    return formdata
