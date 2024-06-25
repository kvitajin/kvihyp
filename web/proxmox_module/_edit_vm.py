def edit_vm(self, vmid, cores, memory, disk_size, node_name=None):
    url = f'{self.PROXMOX_HTTP_HOST}/nodes/{node_name}/qemu/{vmid}/config'
    data = {
        'cores': cores,
        'memory': int(memory*1024*1024*1024)
    }
    response = self.session.put(url, headers=self.csrf_token, cookies=self.ticket, verify=False, data=data)
    if response.status_code == 200:
        print("hurray")
    else:
        print(f'oh no {response.text} reason: {response.reason}')
    return vmid