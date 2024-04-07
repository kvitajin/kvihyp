import secrets
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
# from proxmox_module._get_nodes import get_nodes


class Connection(object):
    def __init__(self):

        self.session = ""
        self.nodes_response = ""
        self.nodes = []
        self.ticket = ""
        self.csrf_token = ""
        self.vms = ""

        # TODO udelat nabidku, kde se zapise
        self.PROXMOX_HOST = secrets.PROXMOX_HOST
        self.USERNAME = secrets.USERNAME
        self.PASSWORD = secrets.PASSWORD

        Connection.get_nodes = get_nodes
        Connection.list_vms = list_vms
        Connection.get_virt_storage = get_virt_storage
        Connection.create_virt_storage = create_virt_storage
        Connection.delete_vm = delete_vm
        Connection.start_vm = start_vm
        Connection.stop_vm = stop_vm
        Connection.suspend_vm = suspend_vm
        Connection.create_vm = create_vm
        Connection.get_max_vmid = get_max_vmid



        auth_url = f'{self.PROXMOX_HOST}/access/ticket'
        auth_data = {'username': self.USERNAME, 'password': self.PASSWORD}
        response = requests.post(auth_url, data=auth_data, verify=False)
        auth_response = response.json()
        self.ticket = auth_response['data']['ticket']
        CSRFPreventionToken = auth_response['data']['CSRFPreventionToken']

        self.session = requests.Session()
        self.csrf_token = {'CSRFPreventionToken': CSRFPreventionToken}
        self.session.headers.update(self.csrf_token)
        self.session.cookies['PVEAuthCookie'] = self.ticket
        self.ticket = {'PVEAuthCookie': self.ticket}

        nodes_url = f'{self.PROXMOX_HOST}/nodes'
        self.nodes_response = self.session.get(nodes_url, verify=False)
        self.nodes = self.get_nodes()





