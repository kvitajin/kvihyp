from proxmox_module import Connection
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# TODO list
#  mazat virtualky      - DONE
#  start                - DONE
#  stop                 - DONE
#  pause                - DONE
#  pristup ke konzoli

def get_virt_pokus(self):
    storages = self.get_virt_storage()
    # print(storages)
    for storage in storages['data']:
        urlinside = f'{self.PROXMOX_HOST}/nodes/{self.get_nodes()[0]}/storage/{storage["storage"]}/content'
        response_inside = self.session.get(urlinside, verify=False)
        print(storage)
        print(f'\t{vars(response_inside)}')


if __name__ == '__main__':
    conn = Connection()
    conn.get_nodes()
    vms = conn.list_vms(False)
    print(vms['data'])
    conn.create_vm(name="pokus", cores=1, memory=512, vmid=conn.get_max_vmid() + 1, disk_size=32)
    conn.create_vm(name="pokus", cores=1, memory=512, vmid=112, disk_size=32)
    conn.delete_vm(vmid=112)
    print(conn.get_max_vmid())
    conn.start_vm(112)
    conn.stop_vm(112)
    conn.get_virt_storage()
    conn.get_virt_pokus()
    conn.create_virt_storage(storage="local-lvm", size=1024, vmid=112)
    conn.create_vm(name="vyser-si-oko",
                   cores=2,
                   memory=1024,
                   vmid=conn.get_max_vmid() + 1,
                   disk_size=1024,
                   storage="local-lvm")
    conn.list_vms(True)
    conn.start_vm(114)
    # connection.stop_vm(114)
    conn.suspend_vm(114)
