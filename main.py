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


if __name__ == '__main__':
    print("Proxmox")
    conn = Proxmox()
    # print(conn.get_nodes())
    # conn.list_vms(True)
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
    conn.get_virt_storage(True)
    xen = Xen()
    # xen_module.list_templates()
    # xen.create_vm_whithout_template(name_label="pokus weeee", name_description="tak hodne stesti")
    # xen_module.create_vm_whithout_template(name_label="pokus", name_description="tak hodne stesti")
    # template_ref="0a2d918d-f506-0c6d-5d20-e0893dc6dfc5"
    # xen_module.get_all_vm_info()
    # print(xen_module.get_VMs())
    print("Xen")
    # xen.get_vms(True)
    # xen.list_vms(True)
    # print(xen.get_templates())
    # xen.create_vm(name="pokus", cores=1, memory=512, vmid=112, disk_size=32)
        # print(i['Value'])
    # for i in fuckit:
    #     data.append(xen.get_vm_info(i))
    # xen.start_vm('3e83e4a3-767b-f74c-49d6-84a6ca37b045')
    # xen.suspend_vm('3e83e4a3-767b-f74c-49d6-84a6ca37b045')
    # xen.stop_vm('3e83e4a3-767b-f74c-49d6-84a6ca37b045')
    # xen.delete_vm('3e83e4a3-767b-f74c-49d6-84a6ca37b045')
    # print(xen.open_console('ac3f83c4-39bc-05ba-d56f-3c3847175f90'))
    # for key, value in data:
    #     print(f'{key}={value}\n')
    # print(data[0])
    xen.get_virt_storage(True)
    xen.create_virt_storage("jmenostorage", '3e83e4a3-767b-f74c-49d6-84a6ca37b045', 1024*1024)


    # print(xen.get_vm_info(xen.fuckit()[0]))
    # print(xen.fuckit())

