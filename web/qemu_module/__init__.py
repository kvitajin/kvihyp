import sqlite3
import subprocess
from ._create_virt_storage import create_virt_storage
from ._create_vm import create_vm

class Qemu(object):
    def __init__(self):
        Qemu.create_virt_storage = create_virt_storage
        Qemu.create_vm = create_vm


