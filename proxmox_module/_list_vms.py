import datetime


def list_vms(self, print_vms=False):
    for node_name in self.get_nodes():
        vms_url = f'{self.PROXMOX_HOST}/nodes/{node_name}/qemu/'
        vm_response = self.session.get(vms_url, verify=False)
        self.vms = vm_response.json()
        if print_vms:
            for vm in self.vms['data']:
                print(f'Name: {vm["name"]}\n\tcpus: {str(vm["cpus"])} \n\t'
                      f'Cpu usage: {str("{:.2f}".format(vm["cpu"] * 100))}%\n\t'
                      f'Max memory usage: {str(vm["maxmem"] / 1024 / 1024 / 1024)} GiB\n\t'
                      f'Mem usage: {str("{:.3f}".format(vm["mem"] / 1024 / 1024 / 1024))} GiB\n\t'
                      f'Uptime: {str(datetime.timedelta(seconds=vm["uptime"]))}')
            return
    return self.vms