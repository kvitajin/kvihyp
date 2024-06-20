import subprocess
import os


def create_vm(self, name, cores, memory, disk_size, storage=None, node_name=None):
    if cores < 1:
        return "Error: cores must be at least 1"
    if memory < 512:
        return "Error: memory must be at least 512"
    if disk_size < 1:
        return "Error: disk_size must be at least 1"

    if not os.path.exists(f'qcows/{name}.qcow2'):
        storage = self.get_virt_storage(size=disk_size, vmid=name)
    else:
        storage = f'qcows/{name}.qcow2'

    cmd = ['qemu-system-x86_64',
           '-enable-kvm',
           '-m', f'{memory}G',
           '-smp', f'{cores}',
           '-hda', f'{storage}',
           '-boot', 'd',
           '-cdrom', 'isos/debian-12.5.0-amd64-DVD-1.iso',
           '-netdev', 'user,id=net0,net=192.168.2.0/24',
           '-device', 'virtio-net-pci,netdev=net0',
           '-vga', 'qxl',
           '-device', 'virtio-serial-pci',
           '-spice', 'port=5900,disable-ticketing',
           '-device', 'virtserialport,chardev=spicechannel0,name=com.redhat.spice.0',
           '-chardev', 'spicevmc,id=spicechannel0,name=vdagent',
           '-device', 'spice-app',
           ]
    subprocess.run(cmd)
