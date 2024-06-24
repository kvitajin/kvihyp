import subprocess
import os
import sys
import django
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Vm



def delete_vm(self, vmid, node_name=None):
    vm = Vm.objects.get(id=vmid)
    if vm is None:
        print(f'VM {vmid} does not exist.')
        return
    if vm.status == 'running':
        self.running_vms[vmid-1].terminate()
    os.remove(vm.storage)
    vm.delete()
    return
