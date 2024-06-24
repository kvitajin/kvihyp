import os
import sys
import django
from datetime import datetime, timezone
import subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Vm


def get_virt_storage(self, print_storage=False, node_names=None):
    # pokus = Vm.objects.all()
    tmp = Vm.objects.filter(connection__host=node_names[0])
    formdata = []
    print(f'tmp: {tmp}')

    for i in tmp:
        storage_used = os.path.getsize(i.storage)
        storage_free = float(i.disk_size)*1024*1024*1024 - storage_used
        formdata.append({'storage': i.name,
                         'used_fraction': 0,
                         'shared': False,
                         'total': i.disk_size,
                         'avail': round(float(storage_free / 1024 / 1024 / 1024), 2),
                         'used': round(float(storage_used / 1024 / 1024 / 1024), 2),
                         'enabled': True,
                         'type': 'qcow2'

                         })


            # {'name': i.name,
            #              'storage': i.storage,
            #              'vmid': i.id})
    print(formdata)
    return formdata
