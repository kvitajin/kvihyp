import secrets
import xmlrpc.client
import ssl
from ._delete_vm import delete_vm
from ._get_template import get_templates
from ._get_nodes import get_nodes
# from ._smazat import get_vm_ref, get_vms
from ._get_vms import get_vms
from ._create_vm import create_vm
from ._start_vm import start_vm
from ._stop_vm import stop_vm
from ._suspend_vm import suspend_vm
from ._open_console import open_console
from ._get_virt_storage import get_virt_storage
from ._create_virt_storage import create_virt_storage

class Xen(object):
    def __init__(self):
        self.session_id = ""
        self.server = ""
        self.session = ""
        self.nodes_response = ""
        self.nodes = []
        self.ticket = ""
        self.csrf_token = ""
        self.vms = ""
        self.spice_config = ""

        self.XEN_HOST = secrets.XEN_HOST

        self.XEN_USERNAME = secrets.XEN_USERNAME
        self.XEN_PASSWORD = secrets.XEN_PASSWORD

        Xen.delete_vm = delete_vm
        Xen.get_templates = get_templates
        Xen.get_nodes = get_nodes               #DONE
        # Xen.get_vm_info = get_vm_info
        # Xen.get_vm_ref = get_vm_ref
        Xen.get_vms = get_vms
        Xen.create_vm = create_vm
        Xen.start_vm = start_vm
        Xen.stop_vm = stop_vm
        Xen.suspend_vm = suspend_vm
        Xen.open_console = open_console
        Xen.get_virt_storage = get_virt_storage
        Xen.create_virt_storage = create_virt_storage
        # Proxmox.list_vms = list_vms
        # Proxmox.get_virt_storage = get_virt_storage
        # Proxmox.create_virt_storage = create_virt_storage

        # Proxmox.get_virt_detail = get_virt_detail
        # Proxmox.get_spice_config = get_spice_config
        # Proxmox.launch_spice_viewer = launch_spice_viewer




        self.server = xmlrpc.client.ServerProxy(secrets.XEN_HOST, context=ssl._create_unverified_context())
        self.session_id = self.login()

    def login(self):
        result = self.server.session.login_with_password(secrets.XEN_USERNAME, secrets.XEN_PASSWORD, "2.0", "python-script")
        session_id = result['Value']
        if session_id:
            print("Přihlášení úspěšné, session ID:", session_id)
            return session_id
        else:
            print("Přihlášení selhalo")
            return None

    def logout(self):
        if self.session_id:
            self.server.session.logout(self.session_id)
            print("Odhlášení úspěšné")
