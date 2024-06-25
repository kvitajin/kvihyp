import sqlite3
import os
import sys
import django
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Vm


def open_console(self, vmid, node_name=None):
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

    if not vm.status == 'running':
        self.start_vm(vmid=vmid, node_name=node_name)
    cmd = ['spicy',
           '-h', 'localhost',
           '-p', '5900',
           ]
    subprocess.Popen(cmd)
