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

# Now this script or any imported module can use any part of Django it needs.


import sys
import os
project_root = sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)
from web.models import Vm
import my_secrets


class Qemu(object):
    def __init__(self, http_host='localhost',
                 password='bulanci',
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

        self.running_vms = {}
        # for i in range(100):
        #     self.running_vms.append(None)
        self.conn = sqlite3.connect('web/db.sqlite3')
        self.cursor = self.conn.cursor()


        # Proxmox.open_console = open_console
        # Proxmox.get_virt_detail = get_virt_detail

        self.conn = sqlite3.connect('web/db.sqlite3')
        self.cursor = self.conn.cursor()

