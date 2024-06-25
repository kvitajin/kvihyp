import sqlite3
import subprocess
from ._create_virt_storage import create_virt_storage
from ._create_vm import create_vm
from ._get_nodes import get_nodes
from ._list_vms import list_vms
from ._start_vm import start_vm
from ._suspend_vm import suspend_vm
from ._stop_vm import stop_vm
from ._delete_vm import delete_vm
from ._get_virt_storage import get_virt_storage
from ._open_console import open_console
from ._create_snapshot import create_snapshot
from ._edit_vm import edit_vm

# Now this script or any imported module can use any part of Django it needs.


import sys
import os
project_root = sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)
from web.models import Vm
import my_secrets


class Qemu(object):
    """
    A class to manage QEMU virtual machines through Proxmox API.

    This class provides methods to create, list, start, stop, suspend, and delete virtual machines (VMs) on a Proxmox cluster.
    It also includes functionality to manage virtual storage and snapshots for VMs.

    Attributes:
        create_virt_storage (function): Static method to create virtual storage.
        create_vm (function): Static method to create a new VM.
        get_nodes (function): Static method to get a list of nodes in the Proxmox cluster.
        list_vms (function): Static method to list VMs.
        start_vm (function): Static method to start a VM.
        suspend_vm (function): Static method to suspend a VM.
        stop_vm (function): Static method to stop a VM.
        delete_vm (function): Static method to delete a VM.
        get_virt_storage (function): Static method to get virtual storage details.
        open_console (function): Static method to open a console to a VM.
        create_snapshot (function): Static method to create a snapshot of a VM.
        edit_vm (function): Static method to edit VM details.
        running_vms (dict): A dictionary to keep track of running VMs.
        conn (sqlite3.Connection): Connection to the SQLite database.
        cursor (sqlite3.Cursor): Cursor for the SQLite database connection.

    Args:
        http_host (str): The HTTP host of the Proxmox server. Defaults to 'localhost'.
        password (str): The password for authentication with the Proxmox server. Defaults to 'password'.
        username (str): The username for authentication with the Proxmox server. Defaults to 'root'.
    """
    def __init__(self, http_host='localhost',
                 password='password',
                 username='root'):
        Qemu.create_virt_storage = create_virt_storage
        Qemu.create_vm = create_vm
        Qemu.get_nodes = get_nodes
        Qemu.list_vms = list_vms
        Qemu.start_vm = start_vm
        Qemu.suspend_vm = suspend_vm
        Qemu.stop_vm = stop_vm
        Qemu.delete_vm = delete_vm
        Qemu.get_virt_storage = get_virt_storage
        Qemu.open_console = open_console
        Qemu.create_snapshot = create_snapshot
        Qemu.edit_vm = edit_vm

        self.running_vms = {}
        # for i in range(100):
        #     self.running_vms.append(None)
        self.conn = sqlite3.connect('web/db.sqlite3')
        self.cursor = self.conn.cursor()

