import os
import sys
import django
from datetime import datetime, timezone
import subprocess
import psutil
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Vm


def list_vms(self, print_vms=False, node_name=None):
    tmp = Vm.objects.filter(connection__host=node_name)
    count = 0
    flag = False
    for i in self.running_vms:
        if i is not None:
            print(f'vm {i}')
        else:
            count = count + 1
    if count == len(self.running_vms):
        flag = True
        print('No VMs are running')
    formdata = []
    for vm in tmp:
        if flag:
            vm.status = 'stopped'
        if vm.status == 'running':
            uptime = str(datetime.now(timezone.utc) - vm.last_update)
        else:
            uptime = 0
        if vm.status == 'running' and self.running_vms.get(int(vm.id)-1) is not None:
            pid = self.running_vms.get(int(vm.id)-1).pid
            # print(f'PID: {pid}')
            command = ['ps', '-o', 'rss=', str(pid)] # Get the memory usage of the VM
            mem_usage = subprocess.run(command, capture_output=True, text=True)
            mem_usage = mem_usage.stdout.strip()
            mem_usage = float(mem_usage) // 1024 // 1024
            proces = psutil.Process(pid)
            cpu_usage = proces.cpu_percent(interval=None)
            # mem_usage = str(0)
        else:
            mem_usage = str(0)
            cpu_usage = str(0)
        # print(mem_usage)
        formdata.append({'name': vm.name,
                         'cpus': vm.cores,
                         'cpu_usage': cpu_usage,
                         'status': vm.status,
                         'vmid': vm.id,
                         'maxmem': str(vm.memory),
                         'mem_usage': mem_usage,
                         'uptime': str(uptime)})
    flag = False
    return formdata
