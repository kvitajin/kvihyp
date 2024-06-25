def create_vm(self, name, cores, memory, disk_size, storage="local-lvm", node_name=None):
    """
    Creates a new virtual machine (VM) on the Xen server.

    This method clones a template VM, sets the new VM's name, description, memory size, number of virtual CPUs, and provisions it.
    It then starts the VM. If the session ID is not set, indicating that the user is not logged in, it prints an error message.

    Args:
        name (str): The name of the new VM.
        cores (int): The number of virtual CPUs for the VM.
        memory (int): The amount of memory for the VM in bytes.
        disk_size (int): The size of the disk for the VM in bytes (currently not used in the method).
        storage (str, optional): The storage repository to use for the VM. Defaults to "local-lvm".
        node_name (str, optional): The name of the node on which to create the VM. Defaults to None.

    Note:
        - The `disk_size` parameter is accepted but not currently used in the method.
        - The method assumes a template VM exists with a hardcoded reference.
        - If `dry_run` is set to True, the VM is not actually provisioned or started, and a success message is printed.
    """
    if not self.session_id:
        print("Nejste přihlášeni")
        return
    dry_run = False
    tmp = self.server.VM.clone(self.session_id, 'OpaqueRef:88d11412-f2fc-4399-a670-188df7118f76', name)

    if tmp['Status'] != "Success":
        print(f"Nepodařilo se vytvořit virtuální stroj {tmp['ErrorDescription']}")
        return
    vm_ref = tmp['Value']

    self.server.VM.set_name_description(self.session_id, vm_ref, name)
    self.server.VM.set_memory(self.session_id, vm_ref, memory)
    self.server.VM.set_vCPUs_number(self.session_id, vm_ref, cores)
    vif = self.server.VM.get_VIFs(self.session_id, vm_ref)
    self.server.VM.set_VIFs(self.session_id, vif)
    if dry_run:
        print(f"Virtuální stroj {name} byl vytvořen úspěšně (dry run)")
        return

    self.server.VM.provision(self.session_id, vm_ref)
    self.server.VM.start(self.session_id, vm_ref, False, False)
    return