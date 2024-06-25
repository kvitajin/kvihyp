def edit_vm(self, vmid, cores, memory, disk_size, node_name=None):
    if not self.session_id:
        print("Nejste přihlášeni")
        return
    vm_ref = self.server.VM.get_by_uuid(self.session_id, vmid)['Value']
    result1=self.server.VM.set_VCPUs_max(self.session_id, vm_ref, cores)
    result3=self.server.VM.set_VCPUs_at_startup(self.session_id, vm_ref, cores)
    memory = int(memory * 1024 * 1024)
    result = self.server.VM.set_memory_limits(self.session_id, vm_ref, memory, memory, memory, memory)
    print(f'result 1: {result1}, result 3 {result3}, result 2: {result}')
    # print(result)
    return vmid