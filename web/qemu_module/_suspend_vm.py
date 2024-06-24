import subprocess
import os
import sys
import django
from datetime import datetime
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Vm



def suspend_vm(self, vmid, node_name=None):
    # print(f'VMID: {vmid}, Node Name: {node_name}')

    vm = Vm.objects.get(id=vmid)
    print(vmid)
    self.running_vms[int(vmid)-1].terminate()
    vm.status = 'suspended'
    vm.last_update = datetime.now()
    vm.save()
    if vm is None:
        print(f'VM {vmid} does not exist.')
        return
    if vm.status == 'suspended':
        print(f'VM {vmid} is already suspended.')
        return
