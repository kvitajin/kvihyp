import subprocess
import os
from datetime import datetime
# TODO jeste asi nefunguje idealne, ale do db zapsalo, tak to asi muselo probehnout spravne
def create_vm(self, name, cores, memory, disk_size, storage=None, node_name=None):
    if cores < 1:
        return "Error: cores must be at least 1"
    if memory < 1:
        return "Error: memory must be at least 512"
    if disk_size < 1:
        return "Error: disk_size must be at least 1"

    if not os.path.exists(f'web/qemu_module/qcows/{name}.qcow2'):
        storage = self.create_virt_storage(size=disk_size, vmid=name)
    else:
        storage = f'web/qemu_module/qcows/{name}.qcow2'
    print(f"storage jede {storage}")
    cmd = ['qemu-system-x86_64',
           '-enable-kvm',
           '-m', f'{memory}G',
           '-smp', f'{cores}',
           '-hda', f'{storage}',
           '-boot', 'd',
           '-cdrom', 'web/qemu_module/isos/debian-12.5.0-amd64-DVD-1.iso',
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
    print("jedeme")
    sql = (f"INSERT INTO web_vm (name, cores, memory, vmid, disk_size, storage, status, last_update, connection_id) "
           f"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)")
    data = (name, cores, memory, name, disk_size, storage, 'stopped', datetime.now(), 3)
    self.cursor.execute(sql, data)
    self.conn.commit()

    return f'web/qemu_module/qcows/{name}.qcow2'