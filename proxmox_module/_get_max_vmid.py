def get_max_vmid(self):
    if not self.vms:
        self.list_vms(False)
    vmids = []
    for vm in self.vms['data']:
        vmids.append(vm['vmid'])
    return max(vmids)
