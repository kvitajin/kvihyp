import os
import sys
import django
from datetime import datetime, timezone
import subprocess
import psutil
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Vm


def list_vms(self, print_vms=False, node_name=None):
    """
    Retrieves virtual storage information for VMs on a specified node.

    This function filters VM instances by the first node name provided in the `node_names` list. For each VM, it calculates
    the used and available storage space, then compiles and returns a list of dictionaries with detailed storage information
    for each VM. The information includes the VM's name, used and available storage space, total disk size, and other relevant
    details.

    Args:
        print_storage (bool, optional): If True, prints the storage information. Defaults to False.
        node_names (list, optional): A list of node names to filter the VMs by. Currently, only the first node name is used.

    Returns:
        list: A list of dictionaries, each containing storage information for a VM. Includes the VM's name, used and available
              storage space, total disk size, and other details.

    Note:
        - The storage space is calculated based on the VM's disk size attribute and the actual file size on disk.
        - The function assumes that the `storage` attribute of a VM instance contains the path to its disk image file.
        - The `enabled`, `type`, and `vmid` fields in the returned dictionaries are hardcoded for demonstration purposes.
    """
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
            command = ['ps', '-o', 'rss=', str(pid)] # Get the memory usage of the VM
            mem_usage = subprocess.run(command, capture_output=True, text=True)
            mem_usage = mem_usage.stdout.strip()
            mem_usage = float(mem_usage) // 1024 // 1024
            proces = psutil.Process(pid)
            cpu_usage = proces.cpu_percent(interval=None)
        else:
            mem_usage = str(0)
            cpu_usage = str(0)
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
