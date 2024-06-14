def create_vm(self, name, cores, memory, vmid, disk_size, storage="local-lvm"):
    if not self.nodes:
        create_url = f'{self.PROXMOX_HTTP_HOST}/nodes/{self.get_nodes()[0]}/qemu'
    else:
        create_url = f'{self.PROXMOX_HTTP_HOST}/nodes/{self.nodes[0]}/qemu'

    virtio = f'{storage}:vm-{vmid}-disk-1'
    data = {
        'vmid': vmid,
        'name': name,
        'memory': memory,
        'cores': cores,
        'net0': 'virtio,bridge=vmbr0',
        'ostype': 'l26',
        'ide2': 'none,media=cdrom',     #tady asi vlepit iso z lvm-hdd
        'bootdisk': 'virtio0',
        'virtio0': virtio
    }
    self.create_virt_storage(storage=storage, size=disk_size, vmid=vmid)
    response = self.session.post(create_url,
                                 data=data,
                                 verify=False, headers=self.csrf_token, cookies=self.ticket)
    if response.status_code == 200:
        print("hurray")
    else:
        print(f'oh no {response.text} reason: {response.reason}')
