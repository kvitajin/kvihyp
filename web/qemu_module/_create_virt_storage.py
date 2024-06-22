import subprocess
import os


def create_virt_storage(self, vmid, size, storage='qcows'):
    cmd = [
        'qemu-img',
        'create',
        '-f',
        'qcow2',
        f'web/qemu_module/{storage}/{vmid}.qcow2',
        f'{size}G'
    ]
    subprocess.run(cmd)
    print(os.getcwd())
    return f'web/qemu_module/{storage}/{vmid}.qcow2'
