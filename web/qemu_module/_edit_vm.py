import subprocess
import os, sys
import django
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Vm


def edit_vm(self, vmid, cores, memory, disk_size, node_name=None):
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