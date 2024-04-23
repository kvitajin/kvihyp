from proxmox_module import Proxmox
from xen_module import Xen
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


# class Xen(object):



    # """function, which creates vm in xen_module"""
    # def create_vm(self, name_label, name_description, template_ref):
    #     if not self.session_id:
    #         print("Nejste přihlášeni")
    #         return
    #
    #     # get default SR
    #     default_sr = self.server.VM.get_by_name_label(self.session_id, "Local storage")['Value']
    #     # get network
    #     network = self.server.network.get_all(self.session_id)['Value'][0]
    #     # get host
    #     host = self.server.host.get_all(self.session_id)['Value'][0]
    #
    #     # create vm
    #     vm_ref = self.server.VM.clone(self.session_id, template_ref, name_label)
    #     if vm_ref['Status'] != "Success":
    #         print(f"Nepodařilo se vytvořit virtuální stroj {vm_ref['ErrorDescription']}")
    #         return
    #
    #     self.server.VM.set_name_description(self.session_id, vm_ref, name_description)
    #     self.server.VM.set_name_label(self.session_id, vm_ref, name_label)
    #     tmp= self.server.VM.get_VIFs(self.session_id, vm_ref)
    #     print("here")
    #     print(tmp)
    #
    #     self.server.VM.set_VIF_network(self.session_id, tmp, network)
    #     self.server.VM.set_other_config(self.session_id, vm_ref, {'install-repository': 'http://archive.ubuntu.com/ubuntu'})
    #     self.server.VM.provision(self.session_id, vm_ref)
    #     self.server.VM.start(self.session_id, vm_ref, False, False)
    #     print(f"Virtual machine {name_label} was created successfully")

    #
    #
    # def create_vm_whithout_template(self, name_label, name_description):
    #     if not self.session_id:
    #         print("Nejste přihlášeni")
    #         return
    #
    #     # get default SR
    #     default_sr = self.server.VM.get_by_name_label(self.session_id, "Local storage")['Value']
    #     # get network
    #     network = self.server.network.get_all(self.session_id)['Value'][0]
    #     # get host
    #     host = self.server.host.get_all(self.session_id)['Value'][0]
    #     data = {
    #         'name_label': name_label,
    #         'name_description': name_description,
    #         'memory_static_max': 1073741824,
    #         'memory_static_min': 1073741824,
    #         'memory_dynamic_max': 1073741824,
    #         'memory_dynamic_min': 536870912,
    #         'VCPUs_max': 2,
    #         'VCPUs_params': {},
    #         'VCPUs_at_startup': 2,
    #         'actions_after_shutdown': 'destroy',
    #         'actions_after_reboot': 'restart',
    #         'actions_after_crash': 'restart',
    #         'PV_bootloader': 'eliloader',
    #         'PV_kernel': '',
    #         'PV_ramdisk': '',
    #         'PV_args': '',
    #         'PV_bootloader_args': '',
    #         'PV_legacy_args': '',
    #         'HVM_boot_policy': 'BIOS order',
    #         'HVM_boot_params': {'order': 'cn', 'bios': '', 'legacy_start': 'false', 'UEFI': 'true', },
    #         'platform': {
    #             'nx': 'true',
    #             'acpi': 'true',
    #             'apic': 'true',
    #             'pae': 'true',
    #             'viridian': 'true',
    #             'timeoffset': '0'
    #         },
    #         'PCI_bus': '',
    #         #TODO asi chzbi pripojeni k netu, tak se nestahne a jebe se to
    #         # 'other_config': {'install-repository': 'https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.5.0-amd64-netinst.iso'},
    #         'other_config': {'install-repository': 'http://archive.ubuntu.com/ubuntu/dists/noble/main/debian-installer/binary-amd64/'},
    #         'recommendations': '',
    #         'xenstore_data': {},
    #         'ha_always_run': False,
    #         'ha_restart_priority': '',
    #         'is_a_template': False,
    #         'is_a_snapshot': False,
    #         'snapshot_of': '',
    #         'snapshot_time': '',
    #         'transportable_snapshot_id': '',
    #         'blobs': {},
    #         'tags': [],
    #         'blocked_operations': {},
    #         'protection_policy': '',
    #         'user_version': 1,
    #         'affinity': '',
    #     }
    #
    #     try:
    #         vm_ref = self.server.VM.create(self.session_id, data)
    #         if vm_ref['Status'] != "Success":
    #             print(f"Nepodařilo se vytvořit virtuální stroj {vm_ref['ErrorDescription']}")
    #             return None
    #     except Exception as e:
    #         print(e)
    #         return None
    #
    #     result = self.server.VM.set_name_description(self.session_id, vm_ref['Value'], name_description)
    #     if result['Status'] != "Success":
    #         print(f"Nepodařilo se nastavit popis virtuálního stroje {result['ErrorDescription']}")
    #         return None
    #     result = self.server.VM.set_name_label(self.session_id, vm_ref['Value'], name_label)
    #     if result['Status'] != "Success":
    #         print(f"Nepodařilo se nastavit jméno virtuálního stroje {result['ErrorDescription']}")
    #         return None
    #     network = self.server.VIF.get_all(self.session_id)
    #
    #     network = self.server.VIF.get_status_code(self.session_id, network['Value'][1])
    #     print(network)
    #
    #     # return None
    #     # if not network:
    #     #     print(f"Nepodařilo se získat síť {network['ErrorDescription']}")
    #     #     return None
    #     # print(f' site: {network}')
    #     # network = self.server.VIF.get_all(self.session_id)
    #     # print(f' site: {network}')
    #     # tmp = self.server.VIF
    #     #
    #     # .set_other_config(self.session_id, {'network': network['Value'][0]})
    #     # tmp = self.server.VM.get_VIFs(self.session_id, vm_ref['Value'])
    #     # if tmp['Status'] != "Success":
    #     #     print(f"Nepodařilo se získat síť virtuálního stroje {tmp['ErrorDescription']}")
    #     #     return None
    #     # print(f"ref {vm_ref['Value']}")
    #     # print(f"tmp {tmp}")
    #     # print(tmp)
    #     # result = self.server.VM.set_VIF(self.session_id, tmp, network)
    #     # if result['Status'] != "Success":
    #     #     print(f"Nepodařilo se nastavit síť virtuálního stroje 2{result['ErrorDescription']}")
    #     #     return None
    #     # self.server.VM.set_other_config(self.session_id, vm_ref, {'install-repository': 'http://archive.ubuntu.com/ubuntu/dists/noble/main/debian-installer/binary-amd64/'})
    #     # result = self.server.VM.provision(self.session_id, vm_ref['Value'])
    #     # if result['Status'] != "Success":
    #     #     print(f"Nepodařilo se provizovat virtuální stroj {result['ErrorDescription']}")
    #     #     return None
    #     result = self.server.VM.start(self.session_id, vm_ref['Value'], False, False)
    #     if result['Status'] != "Success":
    #         print(f"Nepodařilo se spustit virtuální stroj {result['ErrorDescription']}")
    #         return None
    #     print(f"Virtual machine {name_label} was created successfully")
    #
    #
    #
    # def get_all_vm_info(self):
    #     if not self.session_id:
    #         print("Nejste přihlášeni")
    #         return
    #
    #     vm_refs = self.server.VM.get_all(self.session_id)['Value']
    #     for vm_ref in vm_refs:
    #         vm_record = self.server.VM.get_record(self.session_id, vm_ref)['Value']
    #         print(f"Name: {vm_record['name_label']}")
    #         print(f"Description: {vm_record['name_description']}")
    #         print(f"Power state: {vm_record['power_state']}")
    #         print(f"Memory: {vm_record['memory_static_max']}")
    #         print(f"VCPUs: {vm_record['VCPUs_max']}")
    #         print(f"Host: {vm_record['resident_on']}")
    #         # print(f"SR: {vm_record['SR']}")
    #         print(f"Network: {vm_record['VIFs']}")
    #         print(f"")
    #         print(f"")
    #
    # '''cli command: xe other-config-install-repository'''
    # def set_install_repository(self, vm_ref, repository_url):
    #     # Získání aktuální konfigurace
    #     vm = self.server.VM.get_record(self.session_id, vm_ref)
    #     if 'Value' in vm:
    #         other_config = vm['Value']['other_config']
    #         # Přidání nebo aktualizace install-repository
    #         other_config['install-repository'] = repository_url
    #         # Nastavení upraveného other_config zpět na VM
    #         result = self.server.VM.set_other_config(self.session_id, vm_ref, other_config)
    #         if 'Value' in result:
    #             print("Install-repository byl úspěšně nastaven")
    #         else:
    #             print("Nastavení install-repository selhalo: " + str(result))
    #     else:
    #         print("Nepodařilo se získat konfiguraci VM: " + str(vm))
    #
    # def get_vCPUs_params(self, vm_ref):
    #     return self.server.VM.get_VCPUs_params(self.session_id, vm_ref)
    # def get_VMs(self):
    #     return self.server.VM.get_all(self.session_id)



if __name__ == '__main__':
    print("Proxmox")
    conn = Proxmox()
    print(conn.get_nodes())
    # print(conn.get_virt_detail())
    # print(conn.list_vms(False))
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
    # conn.get_spice_config(113)
    # conn.launch_spice_viewer(113)
    xen = Xen()
    # xen_module.list_templates()
    # xen.create_vm_whithout_template(name_label="pokus weeee", name_description="tak hodne stesti")
    # xen_module.create_vm_whithout_template(name_label="pokus", name_description="tak hodne stesti")
    # template_ref="0a2d918d-f506-0c6d-5d20-e0893dc6dfc5"
    # xen_module.get_all_vm_info()
    # print(xen_module.get_VMs())
    print("Xen")
    # print(xen.get_nodes())
    data = []
    fuckit = xen.fuckit()
    print(f'fuckit: {fuckit}')
    # for i in fuckit:
    #     data.append(xen.get_vm_info(i))

    # for key, value in data:
    #     print(f'{key}={value}\n')
    # print(data[0])


    # print(xen.get_vm_info(xen.fuckit()[0]))
    # print(xen.fuckit())

