import subprocess
import os, sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Vm


def edit_vm(self, vmid, cores, memory, disk_size, node_name=None):
    """
    Edits the configuration of an existing virtual machine (VM) identified by its ID.

    This function updates the VM's hardware specifications, including the number of CPU cores, the amount of RAM, and the disk size.
    After updating the VM's attributes in the database, it resizes the VM's disk image to match the new disk size specification using the `qemu-img resize` command.

    Args:
        vmid (int): The ID of the VM to be edited.
        cores (int): The new number of CPU cores to be assigned to the VM.
        memory (int): The new amount of RAM (in GB) to be assigned to the VM.
        disk_size (int): The new size of the disk (in GB) for the VM.
        node_name (str, optional): The name of the node where the VM is located. This parameter is not used in the current implementation but can be utilized for node-specific logic in future enhancements.

    Returns:
        int: The ID of the edited VM.

    Note:
        - The function assumes that the VM's storage file path is stored in the `storage` attribute of the VM instance.
        - If the disk resizing operation fails, an error message is printed.
    """
    vm = Vm.objects.get(id=vmid)
    vm.cores = cores
    vm.memory = memory
    vm.disk_size = disk_size
    vm.save()
    cmd = [
        'qemu-img', 'resize', vm.storage, f'{disk_size}G'
    ]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error resizing disk: {e}')
    return vmid