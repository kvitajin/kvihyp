import sqlite3
import subprocess
from ._create_virt_storage import create_virt_storage
from ._create_vm import create_vm
from ._get_nodes import get_nodes
from ._list_vms import list_vms
from ._start_vm import start_vm

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import my_secrets


class Qemu(object):
    def __init__(self, http_host='localhost',
                 password='bulanci',
                 username='root',
                 ip_host=''):
        Qemu.create_virt_storage = create_virt_storage
        Qemu.create_vm = create_vm
        Qemu.get_nodes = get_nodes
        Qemu.list_vms = list_vms
        Qemu.start_vm = start_vm

        self.conn = sqlite3.connect('web/db.sqlite3')
        self.cursor = self.conn.cursor()


        # Proxmox.get_virt_storage = get_virt_storage
        # Proxmox.create_virt_storage = create_virt_storage
        # Proxmox.delete_vm = delete_vm
        # Proxmox.start_vm = start_vm
        # Proxmox.stop_vm = stop_vm
        # Proxmox.suspend_vm = suspend_vm
        # Proxmox.create_vm = create_vm
        # Proxmox.get_max_vmid = get_max_vmid
        # Proxmox.open_console = open_console
        # Proxmox.get_virt_detail = get_virt_detail
        # Proxmox.get_spice_config = get_spice_config
        # Proxmox.launch_spice_viewer = launch_spice_viewer





        self.conn = sqlite3.connect('web/db.sqlite3')
        self.cursor = self.conn.cursor()


