# from web import my_secrets
import xmlrpc.client
import ssl
from ._delete_vm import delete_vm
from ._get_template import get_templates
from ._get_nodes import get_nodes
from ._get_vms import get_vms
from ._create_vm import create_vm
from ._start_vm import start_vm
from ._stop_vm import stop_vm
from ._suspend_vm import suspend_vm
from ._open_console import open_console
from ._get_virt_storage import get_virt_storage
from ._create_virt_storage import create_virt_storage
from ._create_snapshot import create_snapshot
from ._edit_vm import edit_vm
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import my_secrets


class Xen(object):
    """
    Represents a connection and interaction with a Xen hypervisor.

    This class encapsulates methods for managing virtual machines (VMs) on a Xen hypervisor, including creating, starting,
    stopping, and suspending VMs, as well as managing virtual storage and snapshots.

    Attributes:
        session_id (str): The session ID for the current Xen server session.
        server (str): The XML-RPC server proxy for interacting with the Xen API.
        session (str): Deprecated attribute, not used.
        nodes_response (str): Deprecated attribute, not used.
        nodes (list): Deprecated attribute, not used.
        ticket (str): Deprecated attribute, not used.
        csrf_token (str): Deprecated attribute, not used.
        vms (str): Deprecated attribute, not used.
        spice_config (str): Deprecated attribute, not used.
        XEN_HOST (str): The URL of the Xen server.
        XEN_USERNAME (str): The username for authentication with the Xen server.
        XEN_PASSWORD (str): The password for authentication with the Xen server.
    """
    def __init__(self,
                 xen_host=my_secrets.XEN_HOST,
                 xen_username=my_secrets.XEN_USERNAME,
                 xen_password=my_secrets.XEN_PASSWORD):
        """
        Initializes a new Xen object with the specified host, username, and password.

        Args:
            xen_host (str): The URL of the Xen server.
            xen_username (str): The username for authentication with the Xen server.
            xen_password (str): The password for authentication with the Xen server.
        """
        self.session_id = ""
        self.server = ""
        self.session = ""
        self.nodes_response = ""
        self.nodes = []
        self.ticket = ""
        self.csrf_token = ""
        self.vms = ""
        self.spice_config = ""

        self.XEN_HOST = xen_host

        self.XEN_USERNAME = xen_username
        self.XEN_PASSWORD = xen_password

        Xen.delete_vm = delete_vm
        Xen.get_templates = get_templates
        Xen.get_nodes = get_nodes               #DONE

        Xen.get_vms = get_vms
        Xen.create_vm = create_vm
        Xen.start_vm = start_vm
        Xen.stop_vm = stop_vm
        Xen.suspend_vm = suspend_vm
        Xen.open_console = open_console
        Xen.get_virt_storage = get_virt_storage
        Xen.create_virt_storage = create_virt_storage
        Xen.create_snapshot = create_snapshot
        Xen.edit_vm = edit_vm

        self.server = xmlrpc.client.ServerProxy(self.XEN_HOST, context=ssl._create_unverified_context())
        self.session_id = self.login()



    def login(self):
        """
        Logs in to the Xen server with the provided credentials.

        Returns:
            str: The session ID if login is successful, None otherwise.
        """
        result = self.server.session.login_with_password(self.XEN_USERNAME, self.XEN_PASSWORD, "2.0", "python-script")
        session_id = result['Value']
        if session_id:
            print("Přihlášení úspěšné, session ID:", session_id)
            return session_id
        else:
            print("Přihlášení selhalo")
            return None

    def logout(self):
        """
        Logs out from the Xen server, invalidating the current session ID.
        """
        if self.session_id:
            self.server.session.logout(self.session_id)
            print("Odhlášení úspěšné")
