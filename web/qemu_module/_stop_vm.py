import subprocess
import os
import sys
import django
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Vm
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()

def stop_vm(self, vmid, node_name=None):
    vm = Vm.objects.get(id=vmid)
    if vm is None:
        print(f'VM {vmid} does not exist.')
        return
    if vm.status == 'stopped':
        print(f'VM {vmid} is already stopped.')
        return
    if vm.status == 'running':
        self.running_vms[vmid-1].terminate()
    vm.status = 'stopped'
    vm.last_update = datetime.now()
    vm.save()
    return