import subprocess
import os
import time
import shutil

from web.models import Vm
from datetime import datetime


def create_snapshot(self, vmid, node_name=None):
    """
    Creates a snapshot of a specified virtual machine (VM).

    This function stops the VM if it is running, creates a snapshot of its disk image, and then restarts the VM if it was
    running before the snapshot process. The snapshot is saved with a timestamp in its name to ensure uniqueness.

    Args:
        vmid (int): The ID of the VM for which to create a snapshot.
        node_name (str, optional): The name of the node where the VM is located. This parameter is currently not used
                                   in the function but can be implemented for future use where node-specific actions
                                   might be required.

    Note:
        - The VM is identified using its ID and the snapshot is named using the VM's name and the current timestamp.
        - If the VM is running, it is stopped before taking the snapshot and restarted afterwards.
        - The snapshot is saved in the 'qemu_module/snapshots/' directory.
        - This function uses the 'qemu-img' command to create the snapshot.
        - In case of an error during the snapshot creation, an error message is printed.
        - A workaround for bug 1569835 is implemented by moving the snapshot file after creation.

    Returns:
        None
    """
    vm = Vm.objects.get(id=vmid)
    flag = False
    if vm is None:
        print(f'VM {vmid} does not exist.')
        return
    if vm.status == 'running':
        flag = True
        self.stop_vm(int(vmid))
        time.sleep(5)
    snapshot_name = f'{vm.name}_{datetime.now().strftime("%Y%m%d%H%M%S")}.qcow2'
    snapshot_path = f'qemu_module/snapshots/{snapshot_name}'
    image_path = f'qemu_module/qcows/{vm.name}.qcow2'
    cmd = [
        'qemu-img',
        'create',
        '-f', 'qcow2',
        '-F', 'qcow2',
        '-b',
        image_path,
        snapshot_name
    ]
    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f'Error creating snapshot: {e.stderr.decode()}')
        return
    if flag:
        print(f'Starting VM {vmid} after snapshot.')
        self.start_vm(int(vmid))
    shutil.move(snapshot_name, snapshot_path)   #bug 1569835 workaround
    return