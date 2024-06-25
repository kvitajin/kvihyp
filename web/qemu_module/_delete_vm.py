import subprocess
import os
import django
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Vm



def delete_vm(self, vmid, node_name=None):
    """
    Deletes a specified virtual machine (VM) by its ID.

    This function retrieves the VM instance from the database using its `vmid`. If the VM exists, it checks if the VM is
    currently running. If so, it terminates the VM's process. Then, it removes the VM's storage file from the filesystem
    and deletes the VM record from the database.

    Args:
        vmid (int): The ID of the VM to be deleted.
        node_name (str, optional): The name of the node where the VM is located. This parameter is not used in the current
                                   implementation but can be utilized for node-specific deletion logic in future enhancements.

    Returns:
        None

    Note:
        - This function assumes that the VM's storage file path is stored in the `storage` attribute of the VM instance.
        - If the VM does not exist in the database, a message is printed and the function returns without performing any deletion.
        - The function does not return any value or raise exceptions but prints messages to indicate the status of the operation.
    """
    vm = Vm.objects.get(id=vmid)
    if vm is None:
        print(f'VM {vmid} does not exist.')
        return
    if vm.status == 'running':
        self.running_vms[vmid-1].terminate()
    os.remove(vm.storage)
    vm.delete()
    return
