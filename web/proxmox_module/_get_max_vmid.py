def get_max_vmid(self):
    """
    Retrieves the highest VM ID currently in use within the Proxmox cluster.

    This method first checks if the VM list (`self.vms`) is populated. If not, it populates it by calling
    `self.list_vms(False)`. It then iterates through the VM list, collecting all VM IDs into a list, and
    returns the maximum VM ID found. This is useful for determining the next available VM ID for creating
    new VMs.

    Returns:
        int: The highest VM ID currently in use.
    """
    if not self.vms:
        self.list_vms(False)
    vmids = []
    for vm in self.vms['data']:
        vmids.append(vm['vmid'])
    return max(vmids)
