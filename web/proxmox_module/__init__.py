import requests
from ._get_nodes import get_nodes
from ._list_vms import list_vms
from ._get_virt_storage import get_virt_storage
from ._create_virt_storage import create_virt_storage
from ._delete_vm import delete_vm
from ._start_vm import start_vm
from ._stop_vm import stop_vm
from ._suspend_vm import suspend_vm
from ._create_vm import create_vm
from ._get_max_vmid import get_max_vmid
from ._open_console import open_console
from ._get_virt_detail import get_virt_detail
# from proxmox_module._get_nodes import get_nodes
from ._get_spice_config import get_spice_config
from ._launch_spice_viewer import launch_spice_viewer
from ._create_snapshot import create_snapshot
from ._edit_vm import edit_vm

from requests.packages.urllib3.exceptions import InsecureRequestWarning

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import my_secrets


class Proxmox(object):
    """
    A class to interact with Proxmox virtual environment through its API.

    This class provides methods to authenticate and perform various operations
    in a Proxmox VE cluster, such as managing nodes, virtual machines, and storages.

    Attributes:
        session (requests.Session): A session object for making API requests.
        nodes_response (str): Raw response from the nodes API endpoint.
        nodes (list): A list of nodes in the Proxmox cluster.
        ticket (str): Authentication ticket for the session.
        csrf_token (str): CSRF prevention token for making POST requests.
        vms (str): Placeholder for VMs, not used.
        spice_config (str): Placeholder for SPICE configuration, not used.
        PROXMOX_HTTP_HOST (str): The HTTP host URL of the Proxmox server.
        PROXMOX_USERNAME_AT (str): The username with realm for authentication.
        PROXMOX_PASSWORD (str): The password for authentication.
        PROXMOX_USERNAME (str): The username for authentication.
        PROXMOX_IP_HOST (str): The IP host of the Proxmox server.
    """
    def __init__(self,
                 http_host=my_secrets.PROXMOX_HTTP_HOST,
                 password=my_secrets.PROXMOX_PASSWORD,
                 username=my_secrets.PROXMOX_USERNAME,
                 ip_host=my_secrets.PROXMOX_IP_HOST):
        """
        Initializes the Proxmox object with credentials and sets up the session.

        Args:
            http_host (str): The HTTP host URL of the Proxmox server.
            password (str): The password for authentication.
            username (str): The username for authentication.
            ip_host (str): The IP host of the Proxmox server.
        """
        self.session = ""
        self.nodes_response = ""
        self.nodes = []
        self.ticket = ""
        self.csrf_token = ""
        self.vms = ""
        self.spice_config = ""

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        # TODO udelat nabidku, kde se zapise
        self.PROXMOX_HTTP_HOST = http_host
        self.PROXMOX_USERNAME_AT = username + '@pam'
        self.PROXMOX_PASSWORD = password
        self.PROXMOX_USERNAME = username
        self.PROXMOX_IP_HOST = ip_host

        # Assigning module functions directly to the class
        Proxmox.get_nodes = get_nodes
        Proxmox.list_vms = list_vms
        Proxmox.get_virt_storage = get_virt_storage
        Proxmox.create_virt_storage = create_virt_storage
        Proxmox.delete_vm = delete_vm
        Proxmox.start_vm = start_vm
        Proxmox.stop_vm = stop_vm
        Proxmox.suspend_vm = suspend_vm
        Proxmox.create_vm = create_vm
        Proxmox.get_max_vmid = get_max_vmid
        Proxmox.open_console = open_console
        Proxmox.get_virt_detail = get_virt_detail
        Proxmox.get_spice_config = get_spice_config
        Proxmox.launch_spice_viewer = launch_spice_viewer
        Proxmox.create_snapshot = create_snapshot
        Proxmox.edit_vm = edit_vm

        # Authentication and session setup
        auth_url = f'{self.PROXMOX_HTTP_HOST}/access/ticket'
        auth_data = {'username': self.PROXMOX_USERNAME_AT, 'password': self.PROXMOX_PASSWORD}
        response = requests.post(auth_url, data=auth_data, verify=False)
        auth_response = response.json()
        self.ticket = auth_response['data']['ticket']
        CSRFPreventionToken = auth_response['data']['CSRFPreventionToken']

        self.session = requests.Session()
        self.csrf_token = {'CSRFPreventionToken': CSRFPreventionToken}
        self.session.headers.update(self.csrf_token)
        self.session.cookies['PVEAuthCookie'] = self.ticket
        self.ticket = {'PVEAuthCookie': self.ticket}
        retries = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount('http://', retries)
        self.session.mount('https://', retries)
        self.session.verify = False

        # Fetching nodes to initialize the nodes attribute
        nodes_url = f'{self.PROXMOX_HTTP_HOST}/nodes'
        self.nodes_response = self.session.get(nodes_url, verify=False)
        self.nodes = self.get_nodes()





