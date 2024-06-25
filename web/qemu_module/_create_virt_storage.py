import subprocess
import os


def create_virt_storage(self, vmid, size, storage='qcows'):
    """
    Creates a virtual storage disk for a specified VM.

    This function uses the `qemu-img` command to create a new QCOW2 format disk image with a specified size for a virtual machine.
    The disk image is stored in a specified directory within the `qemu_module` directory.

    Args:
        vmid (int): The ID of the VM for which the storage is being created. This ID is used as the filename.
        size (str): The size of the virtual disk to be created, specified in gigabytes (G).
        storage (str, optional): The subdirectory within `qemu_module` where the disk image will be stored. Defaults to 'qcows'.

    Returns:
        str: The path to the created disk image relative to the project root.

    Note:
        - The function prints the current working directory after creating the disk image.
        - If the `qemu-img` command fails, an error will be raised by `subprocess.run`.
    """
    cmd = [
        'qemu-img',
        'create',
        '-f',
        'qcow2',
        f'qemu_module/{storage}/{vmid}.qcow2',
        f'{size}G'
    ]
    subprocess.run(cmd)
    print(os.getcwd())
    return f'qemu_module/{storage}/{vmid}.qcow2'
