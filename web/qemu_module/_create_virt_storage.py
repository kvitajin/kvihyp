import subprocess


def create_virt_storage(self, vmid, size, storage='qcows'):
    cmd = [
        'qemu-img',
        'create',
        '-f',
        'qcow2',
        f'{storage}/{vmid}.qcow2',
        f'{size}G'
    ]
    subprocess.run(cmd)

    return f'{storage}/{vmid}.qcow2'
