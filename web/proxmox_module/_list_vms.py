import datetime


def list_vms(self, print_vms=False, node_names=None):
    if not node_names:
        self.get_nodes()
    for node_name in node_names:
        vms_url = f'{self.PROXMOX_HTTP_HOST}/nodes/{node_name}/qemu/'
        vm_response = self.session.get(vms_url, verify=False)
        self.vms = vm_response.json()
        if print_vms:
            for vm in self.vms['data']:
                print(f'Name: {vm["name"]}\n\t'
                      f'cpus: {str(vm["cpus"])} \n\t'
                      f'Cpu usage: {str("{:.2f}".format(vm["cpu"] * 100))}%\n\t'
                      f'Status: {vm["status"]}\n\t'
                      f'Vmid: {str(vm["vmid"])}\n\t'
                      f'Max memory usage: {str(vm["maxmem"] / 1024 / 1024 / 1024)} GiB\n\t'
                      f'Mem usage: {str("{:.3f}".format(vm["mem"] / 1024 / 1024 / 1024))} GiB\n\t'
                      f'Uptime: {str(datetime.timedelta(seconds=vm["uptime"]))}')
            return
        else:
            formdata = []
            for vm in self.vms['data']:
                formdata.append({'name': vm['name'],
                                 'cpus': vm['cpus'],
                                 'cpu_usage': str("{:.2f}".format(vm["cpu"] * 100)),
                                 'status': vm['status'],
                                 'vmid': vm['vmid'],
                                 'maxmem': str(vm["maxmem"] / 1024 / 1024 / 1024),
                                 'mem_usage': str("{:.3f}".format(vm["mem"] / 1024 / 1024 / 1024)),
                                 'uptime': str(datetime.timedelta(seconds=vm["uptime"]))})
            return formdata
