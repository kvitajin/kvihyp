import subprocess
import os
import sys
import django
from datetime import datetime
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Vm


def start_vm(self, vmid, node_name=None):
    """
    Opens a console connection to a specified virtual machine (VM) by its ID.

    This function first attempts to retrieve the VM instance from the database using its `vmid`. If the VM does not exist,
    it prints a message and returns. If the VM exists but is not running, it attempts to start the VM using the `start_vm`
    method. After ensuring the VM is running, it opens a console connection using the `spicy` command, connecting to
    localhost on port 5900.

    Args:
        vmid (int): The ID of the VM to open a console connection to.
        node_name (str, optional): The name of the node where the VM is located. This parameter is not used in the current
                                   implementation but can be utilized for node-specific logic in future enhancements.

    Returns:
        None

    Note:
        - This function assumes that the `status` attribute of the VM instance indicates whether the VM is running.
        - The `spicy` command is used to open the console connection. This requires `spicy` to be installed and accessible
          in the system's PATH.
        - The function does not handle exceptions that may arise from starting the VM or opening the console connection.
    """
    vm = Vm.objects.get(id=vmid)
    if vm is None:
        print(f'VM {vmid} does not exist.')
        return
    if vm.status == 'running' and vmid-1 in self.running_vms:
        print(f'VM {vmid} is already running.')
        return
    cmd = [
        'qemu-system-x86_64',
        '-enable-kvm',
        '-m', f'{vm.memory}G',
        '-smp', f'{vm.cores}',
        '-hda', f'{vm.storage}',
        '-boot', 'c',
        '-netdev', 'user,id=net0,net=192.168.2.0/24',
        '-device', 'virtio-net-pci,netdev=net0',
        '-vga', 'qxl',
        '-device', 'virtio-serial-pci',
        '-spice', 'port=5900,disable-ticketing=on',
        '-device', 'virtserialport,chardev=spicechannel0,name=com.redhat.spice.0',
        '-chardev', 'spicevmc,id=spicechannel0,name=vdagent',
    ]
    self.running_vms[int(vmid)-1] = subprocess.Popen(cmd)
    vm.status = 'running'
    vm.last_update = datetime.now()
    vm.save()
    print(f'VM {vmid} started.')
    return

