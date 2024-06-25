def edit_vm(self, vmid, cores, memory, disk_size, node_name=None):
    """
    Edits the configuration of an existing virtual machine (VM) identified by its UUID.

    This method allows for the modification of a VM's number of virtual CPUs (both maximum and at startup), and its memory size.
    The disk size and node name parameters are accepted but not currently used in this implementation. Before making any changes,
    it checks if a session ID is present to ensure the user is logged in. If not, it prints a message indicating the user is not logged in.

    Args:
        vmid (str): The UUID of the VM to be edited.
        cores (int): The new number of virtual CPUs to be set for the VM.
        memory (float): The new amount of memory (in GB) to be set for the VM.
        disk_size (int): The new disk size for the VM in bytes (currently not used).
        node_name (str, optional): The name of the node where the VM is located (currently not used).

    Returns:
        str: The UUID of the edited VM.

    Note:
        - The `disk_size` and `node_name` parameters are accepted for future compatibility but are not utilized in the current implementation.
        - The memory size is internally converted from GB to bytes before setting it for the VM.
    """
    if not self.session_id:
        print("Nejste přihlášeni")
        return
    vm_ref = self.server.VM.get_by_uuid(self.session_id, vmid)['Value']
    result1 = self.server.VM.set_VCPUs_max(self.session_id, vm_ref, cores)
    result3 = self.server.VM.set_VCPUs_at_startup(self.session_id, vm_ref, cores)
    memory = int(memory * 1024 * 1024)
    result = self.server.VM.set_memory_limits(self.session_id, vm_ref, memory, memory, memory, memory)
    return vmid