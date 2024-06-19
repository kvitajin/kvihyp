import my_secrets
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
from requests.packages.urllib3.exceptions import InsecureRequestWarning



class Proxmox(object):
    def __init__(self,
                 http_host=my_secrets.PROXMOX_HTTP_HOST,
                 password=my_secrets.PROXMOX_PASSWORD,
                 username=my_secrets.PROXMOX_USERNAME,
                 ip_host=my_secrets.PROXMOX_IP_HOST):

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

        nodes_url = f'{self.PROXMOX_HTTP_HOST}/nodes'
        self.nodes_response = self.session.get(nodes_url, verify=False)
        self.nodes = self.get_nodes()





