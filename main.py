from proxmox_module import Proxmox
import urllib3
import xmlrpc.client
import secrets
import ssl

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# TODO list
#  mazat virtualky      - DONE
#  start                - DONE
#  stop                 - DONE
#  pause                - DONE
#  pristup ke konzoli


class Xen(object):
    def __init__(self):
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

    def list_templates(self):
        if not self.session_id:
            print("Nejste přihlášeni")
            return

        vm_refs = self.server.VM.get_all(self.session_id)['Value']
        templates = []
        for vm_ref in vm_refs:
            vm_record = self.server.VM.get_record(self.session_id, vm_ref)['Value']
            if vm_record['is_a_template']:
                templates.append((vm_record['name_label'], vm_ref))

        if templates:
            print("Dostupné šablony:")
            for name, ref in templates:
                print(f"{name} - {ref}")
        else:
            print("Nebyly nalezeny žádné šablony.")



    """function, which creates vm in xen"""
    def create_vm(self, name_label, name_description, template_ref):
        if not self.session_id:
            print("Nejste přihlášeni")
            return

        # get default SR
        default_sr = self.server.VM.get_by_name_label(self.session_id, "Local storage")['Value']
        # get network
        network = self.server.network.get_all(self.session_id)['Value'][0]
        # get host
        host = self.server.host.get_all(self.session_id)['Value'][0]

        # create vm
        vm_ref = self.server.VM.clone(self.session_id, template_ref, name_label)
        if vm_ref['Status'] != "Success":
            print(f"Nepodařilo se vytvořit virtuální stroj {vm_ref['ErrorDescription']}")
            return

        self.server.VM.set_name_description(self.session_id, vm_ref, name_description)
        self.server.VM.set_name_label(self.session_id, vm_ref, name_label)
        tmp= self.server.VM.get_VIFs(self.session_id, vm_ref)
        print("here")
        print(tmp)

        self.server.VM.set_VIF_network(self.session_id, tmp, network)
        self.server.VM.set_other_config(self.session_id, vm_ref, {'install-repository': 'http://archive.ubuntu.com/ubuntu'})
        self.server.VM.provision(self.session_id, vm_ref)
        self.server.VM.start(self.session_id, vm_ref, False, False)
        print(f"Virtual machine {name_label} was created successfully")

    def create_vm_whithout_template(self, name_label, name_description):
        if not self.session_id:
            print("Nejste přihlášeni")
            return

        # get default SR
        default_sr = self.server.VM.get_by_name_label(self.session_id, "Local storage")['Value']
        # get network
        network = self.server.network.get_all(self.session_id)['Value'][0]
        # get host
        host = self.server.host.get_all(self.session_id)['Value'][0]
        data = {
            'name_label': name_label,
            'name_description': name_description,
            'memory_static_max': 1073741824,
            'memory_static_min': 1073741824,
            'memory_dynamic_max': 1073741824,
            'memory_dynamic_min': 536870912,
            'VCPUs_max': 2,
            'VCPUs_params': {},
            'VCPUs_at_startup': 2,
            'actions_after_shutdown': 'destroy',
            'actions_after_reboot': 'restart',
            'actions_after_crash': 'restart',
            'PV_bootloader': 'eliloader',
            'PV_kernel': '',
            'PV_ramdisk': '',
            'PV_args': '',
            'PV_bootloader_args': '',
            'HVM_boot_policy': '',
            'HVM_boot_params': '',
            'platform': {'nx': 'true', 'acpi': 'true', 'apic': 'true', 'pae': 'true', 'viridian': 'true', 'timeoffset': '0'},
            'PCI_bus': '',
            'other_config': {},
            'recommendations': '',
            'xenstore_data': {},
            'ha_always_run': False,
            'ha_restart_priority': '',
            'is_a_template': False,
            'is_a_snapshot': False,
            'snapshot_of': '',
            'snapshot_time': '',
            'transportable_snapshot_id': '',
            'blobs': {},
            'tags': [],
            'blocked_operations': {},
            'protection_policy': '',
            'user_version': 1,
            'affinity': '',
        }

        # create vm
        vm_ref = self.server.VM.create(self.session_id, data)
        if vm_ref['Status'] != "Success":
            print(f"Nepodařilo se vytvořit virtuální stroj {vm_ref['ErrorDescription']}")
            return

        self.server.VM.set_name_description(self.session_id, vm_ref, name_description)
        self.server.VM.set_name_label(self.session_id, vm_ref, name_label)
        tmp= self.server.VM.get_VIFs(self.session_id, vm_ref)
        print("here")
        print(tmp)

        self.server.VM.set_VIF_network(self.session_id, tmp, network)
        self.server.VM.set_other_config(self.session_id, vm_ref, {'install-repository': 'http://archive.ubuntu.com/ubuntu'})
        self.server.VM.provision(self.session_id, vm_ref)
        self.server.VM.start(self.session_id, vm_ref, False, False)
        print(f"Virtual machine {name_label} was created successfully")

    def get_all_vm_info(self):
        if not self.session_id:
            print("Nejste přihlášeni")
            return

        vm_refs = self.server.VM.get_all(self.session_id)['Value']
        for vm_ref in vm_refs:
            vm_record = self.server.VM.get_record(self.session_id, vm_ref)['Value']
            print(f"Name: {vm_record['name_label']}")
            print(f"Description: {vm_record['name_description']}")
            print(f"Power state: {vm_record['power_state']}")
            print(f"Memory: {vm_record['memory_static_max']}")
            print(f"VCPUs: {vm_record['VCPUs_max']}")
            print(f"Host: {vm_record['resident_on']}")
            # print(f"SR: {vm_record['SR']}")
            print(f"Network: {vm_record['VIFs']}")
            print(f"")
            print(f"")

    def get_vCPUs_params(self, vm_ref):
        return self.server.VM.get_VCPUs_params(self.session_id, vm_ref)
    def get_VMs(self):
        return self.server.VM.get_all(self.session_id)
if __name__ == '__main__':
    conn = Proxmox()
    # conn.get_nodes()
    # vms = conn.list_vms(False)
    # print(vms['data'])
    # conn.create_vm(name="pokus", cores=1, memory=512, vmid=conn.get_max_vmid() + 1, disk_size=32)
    # conn.create_vm(name="pokus", cores=1, memory=512, vmid=112, disk_size=32)
    # conn.delete_vm(vmid=112)
    # print(conn.get_max_vmid())
    # conn.start_vm(112)
    # conn.stop_vm(112)
    # conn.get_virt_storage()
    # conn.get_virt_detail()
    # conn.create_virt_storage(storage="local-lvm", size=1024, vmid=112)
    # conn.create_vm(name="vyser-si-oko",
    #                cores=2,
    #                memory=1024,
    #                vmid=conn.get_max_vmid() + 1,
    #                disk_size=1024,
    #                storage="local-lvm")
    # conn.list_vms(True)
    # conn.start_vm(114)
    # # connection.stop_vm(114)
    # conn.suspend_vm(114)
    # conn.open_console()
    # conn.start_vm(11)
    conn.get_spice_config(113)
    conn.launch_spice_viewer(113)
    xen = Xen()
    # xen.list_templates()
    xen.create_vm(name_label="pokus", name_description="tak hodne stesti", template_ref="0a2d918d-f506-0c6d-5d20-e0893dc6dfc5")
    # xen.create_vm_whithout_template(name_label="pokus", name_description="tak hodne stesti")
    # print(xen.get_vCPUs_params("e0fcbe5b-b469-35a0-b644-a12543a21c37"))
    # print(xen.get_vCPUs_params("dfbf8a5c-0766-aeec-4920-fec5b851e63d"))
    # print(xen.get_vCPUs_params("ddf973f6-87b7-2a13-f124-5ceddbeedfb8"))
    # print(xen.get_vCPUs_params("daa02ea9-6d2f-f4b8-5833-3ecbbff27205"))
    # print(xen.get_vCPUs_params("d86a796c-5841-5da3-0a6a-ea65f8bb7d8b"))
    # print(xen.get_vCPUs_params("d6cfc249-4907-e46d-f43d-4056c26dec0a"))
    # print(xen.get_vCPUs_params("d0f5ed92-36d4-e996-6716-6f8948631f31"))
    # print(xen.get_vCPUs_params("ca1aa5b4-96d1-0b5b-5b11-805a8724a35d"))
    # print(xen.get_vCPUs_params("bd06a3a8-6913-f922-91a1-e741c83d134b"))
    # print(xen.get_vCPUs_params("9de26b23-3c9a-c738-32f2-047e34ac916c"))
    # print(xen.get_vCPUs_params("9710df1e-dd84-cbcd-0fff-dab62fa1ad29"))
    # print(xen.get_vCPUs_params("9036322f-2311-d23d-225f-2cde3f014830"))
    # print(xen.get_vCPUs_params("8edf0bc1-b4c3-823e-87ca-e643e0648c4d"))
    # print(xen.get_vCPUs_params("8c6f57b3-b189-a08d-608d-317bdc5b62be"))
    # print(xen.get_vCPUs_params("86b9eba2-3170-6763-4fd4-f517b8ea7128"))
    # print(xen.get_vCPUs_params("8697d445-a544-b259-84ae-3d5bf2c9d04f"))
    # print(xen.get_vCPUs_params("69ef6e3d-8f51-7d2b-d087-84fe8d102055"))
    # print(xen.get_vCPUs_params("69416b49-67e2-91ff-312f-1467524f0f7d"))
    # print(xen.get_vCPUs_params("654c59fd-ca7c-4c7e-ce80-389ed94caeac"))
    # print(xen.get_vCPUs_params("6538a09e-8877-4cb2-6794-7a904b12e34e"))
    # print(xen.get_vCPUs_params("52821d22-0bf8-03ab-ee5e-4a368b21f750"))
    # print(xen.get_vCPUs_params("4b975db4-c691-45bf-3d9d-f0f9d19081e1"))
    # print(xen.get_vCPUs_params("3d257e19-821a-e89b-a8ec-6098039b38cf"))
    # print(xen.get_vCPUs_params("3c02407e-dd0f-6a72-d24b-b798a7c5abf9"))
    # print(xen.get_vCPUs_params("231c3e28-2580-0dbd-9319-d1ebf1c46381"))
    # print(xen.get_vCPUs_params("16d6bb88-a25e-f126-c83a-b71a793dc364"))
    # print(xen.get_vCPUs_params("125a7c54-5a91-d7c2-03ce-b16e90de2ffb"))
    # print(xen.get_vCPUs_params("0de8b221-ad0b-25ee-e889-8ee996616fb9"))
    # print(xen.get_vCPUs_params("0a2d918d-f506-0c6d-5d20-e0893dc6dfc5"))
    # print(xen.get_vCPUs_params("02e956f0-33c5-82ca-7339-b13d8015d7c7"))
    xen.get_all_vm_info()
    # print(xen.get_VMs())

