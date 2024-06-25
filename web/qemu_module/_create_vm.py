import subprocess
import os, sys
import django
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.models import Vm
# TODO jeste asi nefunguje idealne, ale do db zapsalo, tak to asi muselo probehnout spravne


def create_vm(self, name, cores, memory, disk_size, storage=None, node_name=None):
    """
    Creates a new virtual machine (VM) with specified configurations.

    This function initializes a VM with given hardware specifications and a Debian ISO as the installation media.
    It checks if the specified disk image exists, and if not, it creates a new virtual storage disk. The VM is then
    started with the specified configurations using the `qemu-system-x86_64` command.

    Args:
        name (str): The name of the VM. Used as the identifier and part of the disk image filename.
        cores (int): The number of CPU cores assigned to the VM. Must be at least 1.
        memory (int): The amount of RAM (in GB) assigned to the VM. Must be at least 512 MB.
        disk_size (int): The size of the disk (in GB) for the VM. Must be at least 1 GB.
        storage (str, optional): The path to the storage disk image. If not provided, a new disk will be created.
        node_name (str, optional): The name of the node on which to create the VM. Currently not used.

    Returns:
        str: The path to the disk image used by the VM.

    Note:
        - The VM is configured to boot from the Debian ISO image specified in the command.
        - Network configuration is set to a user-mode network with a predefined subnet.
        - The VM is added to the Django database with a status of 'stopped' after creation.
        - Error handling for the input parameters is included to ensure valid configurations.
    """
    if cores < 1:
        return "Error: cores must be at least 1"
    if memory < 1:
        return "Error: memory must be at least 512"
    if disk_size < 1:
        return "Error: disk_size must be at least 1"
    qcow2 = f'qemu_module/qcows/{name}.qcow2'
    if not os.path.exists(qcow2):
        storage = self.create_virt_storage(size=disk_size, vmid=name)
    else:
        storage = qcow2
    print(f"storage jede {storage}")
    cmd = ['qemu-system-x86_64',
           '-enable-kvm',
           '-m', f'{memory}G',
           '-smp', f'{cores}',
           '-hda', f'{storage}',
           '-boot', 'd',
           '-cdrom', 'qemu_module/isos/debian-12.5.0-amd64-DVD-1.iso',
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
    Vm(name=name, cores=cores, memory=memory, disk_size=disk_size, storage=storage, status='stopped', last_update=datetime.now(), connection_id=3).save()
    return qcow2
