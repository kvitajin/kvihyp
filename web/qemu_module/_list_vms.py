import os
import sys
import django
from datetime import datetime, timezone
import subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Vm
def list_vms(self, print_vms=False, node_name=None):
    tmp = Vm.objects.filter(connection__host=node_name)
    for i in self.running_vms:
        print(f'vm {i}')


    formdata = []
    for vm in tmp:
        if vm.status == "running":
            uptime = str(datetime.now(timezone.utc) - vm.last_update)
        else:
            uptime = 0
        if vm.status == 'running' and self.running_vms[int(vm.id)-1] is not None:
            pid = self.running_vms[int(vm.id)-1].pid
            print(f'PID: {pid}')
            command = ['ps', '-o', 'rss=', pid] # Get the memory usage of the VM
            mem_usage = subprocess.run(command, capture_output=True, text=True)
            mem_usage = mem_usage.stdout
        else:
            mem_usage = str(0)
        print(mem_usage)
        formdata.append({'name': vm.name,
                         'cpus': vm.cores,
                         'cpu_usage': str(0),
                         'status': vm.status,
                         'vmid': vm.id,
                         'maxmem': str(vm.memory),
                         'mem_usage': mem_usage,
                         'uptime': str(uptime)})
    return formdata