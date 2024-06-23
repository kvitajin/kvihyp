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

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
        self.running_vms = []
        for i in range(100):
            self.running_vms.append(None)
        self.conn = sqlite3.connect('web/db.sqlite3')
        self.cursor = self.conn.cursor()


        # Proxmox.get_virt_storage = get_virt_storage
        # Proxmox.open_console = open_console
        # Proxmox.get_virt_detail = get_virt_detail
        # Proxmox.get_spice_config = get_spice_config
        # Proxmox.launch_spice_viewer = launch_spice_viewer





        self.conn = sqlite3.connect('web/db.sqlite3')
        self.cursor = self.conn.cursor()


