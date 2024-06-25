import subprocess
import os
import sys
import django
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Vm


def suspend_vm(self, vmid, node_name=None):
    """
    Stops a virtual machine (VM) identified by its ID.

    This function attempts to stop a VM by terminating its process. It first checks if the VM exists in the database and
    whether it is already in a 'stopped' state to avoid unnecessary operations. If the VM is running, it retrieves the
    process handle from a tracking list and sends a terminate signal to the process. Finally, it updates the VM's status
    to 'stopped' and records the current timestamp as the last update time in the database.

    Args:
        vmid (int): The ID of the VM to be stopped.
        node_name (str, optional): The name of the node where the VM is located. This parameter is currently not used but
                                   can be utilized for node-specific logic in future enhancements.

    Returns:
        None

    Note:
        - The function checks if the VM exists and whether it is already stopped to avoid attempting to stop it multiple times.
        - The VM's process handle is expected to be stored in a list (`self.running_vms`) with indices corresponding to VM IDs.
        - The function updates the VM's status and last update timestamp in the database after successfully stopping the VM.
    """

    vm = Vm.objects.get(id=vmid)
    self.running_vms[int(vmid)-1].terminate()
    vm.status = 'suspended'
    vm.last_update = datetime.now()
    vm.save()
    if vm is None:
        print(f'VM {vmid} does not exist.')
        return
    if vm.status == 'suspended':
        print(f'VM {vmid} is already suspended.')
        return
