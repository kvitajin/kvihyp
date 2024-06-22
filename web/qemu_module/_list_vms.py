import os
import sys
import django
import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Vm
def list_vms(self, print_vms=False, node_name=None):
    tmp = Vm.objects.filter(connection__host=node_name)
    formdata = []
    for vm in tmp:
        if vm.status == "running":
            uptime = str(datetime.datetime.now() - vm.last_update)
        else:
            uptime = 0
        formdata.append({'name': vm.name,
                         'cpus': vm.cores,
                         'cpu_usage': str(0),
                         'status': vm.status,
                         'vmid': vm.id,
                         'maxmem': str(vm.memory),
                         'mem_usage': str(0),
                         'uptime': str(uptime)})
    return formdata