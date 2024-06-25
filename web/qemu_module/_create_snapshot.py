import subprocess
import os
import time
import shutil

from web.models import Vm
from datetime import datetime


def create_snapshot(self, vmid, node_name=None):
    vm = Vm.objects.get(id=vmid)
    flag = False
    if vm is None:
        print(f'VM {vmid} does not exist.')
        return
    if vm.status == 'running':
        flag = True
        self.stop_vm(int(vmid))
        time.sleep(5)
    snapshot_name = f'{vm.name}_{datetime.now().strftime("%Y%m%d%H%M%S")}.qcow2'
    snapshot_path = f'qemu_module/snapshots/{snapshot_name}'
    image_path = f'qemu_module/qcows/{vm.name}.qcow2'
    cmd = [
        'qemu-img',
        'create',
        '-f', 'qcow2',
        '-F', 'qcow2',
        '-b',
        image_path,
        snapshot_name
    ]
    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f'Error creating snapshot: {e.stderr.decode()}')
        return
    if flag:
        print(f'Starting VM {vmid} after snapshot.')
        self.start_vm(int(vmid))
    shutil.move(snapshot_name, snapshot_path)   #bug 1569835 workaround
    return