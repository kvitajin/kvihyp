import subprocess
import os
import sys
import django
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Vm
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()


def start_vm(self, vmid, node_name=None):
    # print(f'VMID: {vmid}, Node Name: {node_name}')

    vm = Vm.objects.get(id=vmid)
    # print(f'VM: {vm}')
    # self.cursor.execute("SELECT * FROM Vm WHERE id=?", (vmid))
    # vm = self.cursor.fetchone()
    if vm is None:
        print(f'VM {vmid} does not exist.')
        return
    cmd = [
        'qemu-system-x86_64',
        '-enable-kvm',
        '-m', f'{vm.memory}G',
        '-smp', f'{vm.cores}',
        '-hda', f'{vm.storage}',
        '-boot', 'c',
        '-netdev', 'user,id=net0,net=192.168.2.0/24',
        '-device', 'virtio-net-pci,netdev=net0',
        '-vga', 'qxl',
        '-device', 'virtio-serial-pci',
        '-spice', 'port=5900,disable-ticketing=on',
        '-device', 'virtserialport,chardev=spicechannel0,name=com.redhat.spice.0',
        '-chardev', 'spicevmc,id=spicechannel0,name=vdagent',
    ]
    runstatus = subprocess.run(cmd)
    print(runstatus.returncode)
    vm.status = 'running'
    vm.last_update = datetime.now()
    vm.save()
    # self.cursor.execute("UPDATE Vm SET status='running', last_update= ? WHERE id=?", (datetime.now(), vmid))
    # self.cursor.commit()
    print(f'VM {vmid} started.')
    return

