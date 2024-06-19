def create_vm(self, name, cores, memory, disk_size, storage="local-lvm", node_name=None):
    print("create_vm xen")
    if not self.session_id:
        print("Nejste přihlášeni")
        return
    dry_run = False
    # get default SR
    # default_sr = self.server.VM.get_by_name_label(self.session_id, "Local storage")['Value']
    # print(f'sr {default_sr}')
    # get network
    alls = self.server.network.get_all_records(self.session_id)
    network = self.server.network.get_all(self.session_id)['Value']
    network_details = self.server.network.get_record(self.session_id, network[0])
    # print(f'network {network}')
    # print(f'network details {network_details["Value"]},\ntmp {alls["Value"]}')
    zaz = self.server.VIF.get_all(self.session_id)
    # print(f'zaz {zaz}')


    # print(self.server.VIF.get_network(self.session_id, zaz['Value'][0]))
    # get host
    # host = self.server.host.get_all(self.session_id)['Value']
    # host_full = self.server.host.get_record(self.session_id, host[0])
    # print(f'host {host}')
    # print(f'host full {host_full}')

    # def create_vm(self, name_label, name_description, template_ref):

    tmp = self.server.VM.clone(self.session_id, 'OpaqueRef:88d11412-f2fc-4399-a670-188df7118f76', name)

    if tmp['Status'] != "Success":
        print(f"Nepodařilo se vytvořit virtuální stroj {tmp['ErrorDescription']}")
        return
    vm_ref = tmp['Value']

    self.server.VM.set_name_description(self.session_id, vm_ref, name)
    self.server.VM.set_memory(self.session_id, vm_ref, memory)
    self.server.VM.set_vCPUs_number(self.session_id, vm_ref, cores)
    # self.server.VM.set_name_description(self.session_id, tmp['Value'], description)
    vif = self.server.VM.get_VIFs(self.session_id, vm_ref)
    # print(f'vif {vif}')
    self.server.VM.set_VIFs(self.session_id, vif)
    if dry_run:
        print(f"Virtuální stroj {name} byl vytvořen úspěšně (dry run)")
        return

    self.server.VM.provision(self.session_id, vm_ref)
    self.server.VM.start(self.session_id, vm_ref, False, False)


    # self.server.VM.set_other_config(self.session_id, tmp['Value'], {'install-repository': 'http://archive.ubuntu.com/ubuntu'})


    # print(result)



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