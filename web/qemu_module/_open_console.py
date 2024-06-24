import sqlite3
import os
import sys
import django
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Vm




def open_console(self, vmid, node_name=None):
    vm = Vm.objects.get(id=vmid)
    if vm is None:
        print(f'VM {vmid} does not exist.')
        return

    if not vm.status == 'running':
        # self.running_vms[vmid-1]
        self.start_vm(vmid=vmid, node_name=node_name)
    cmd = ['spicy',
           '-h', 'localhost',
           '-p', '5900',
           ]
    subprocess.Popen(cmd)
