import datetime


def list_vms(self, print_vms=False, node_names=None):
    """
    Lists virtual machines (VMs) on specified Proxmox nodes or all nodes if none are specified.

    This method fetches a list of VMs from the Proxmox cluster. It can either print the VM details to the console
    or return a list of VM details in a structured format. The method allows filtering of VMs by node names.

    Args:
        print_vms (bool, optional): If True, prints the VM details to the console. If False, returns a list of VM
                                    details. Defaults to False.
        node_names (list, optional): A list of node names to filter the VMs by. If None, VMs from all nodes are
                                     considered. Defaults to None.

    Returns:
        None or list: If `print_vms` is False, returns a list of dictionaries with VM details. Each dictionary
                      contains keys like 'name', 'cpus', 'cpu_usage', 'status', 'vmid', 'maxmem', 'mem_usage',
                      'uptime', and 'disk_size'. If `print_vms` is True, returns None.

    Note:
        The method utilizes the Proxmox API to fetch VM details and requires a valid session to be established.
    """
    if not node_names:
        node_names = self.get_nodes()
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
                                 'uptime': str(datetime.timedelta(seconds=vm["uptime"])),
                                 'disk_size': str(vm["maxdisk"] / 1024 / 1024 / 1024)})
            return formdata
