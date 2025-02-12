import xmlrpc
from datetime import datetime as dt, timedelta
from humanfriendly import format_timespan


def get_vms(self, print_vms=False, node_name=None):
    """
    Retrieves and optionally prints information about all virtual machines (VMs) from the Xen server.

    This method fetches records for all VMs and their metrics, including memory usage and uptime, from the Xen server.
    It can filter VMs based on a specified node name (though this functionality is currently not implemented) and
    either print the VM information to the console or return it as a list of dictionaries.

    Args:
        print_vms (bool, optional): If True, prints the VM information to the console. Otherwise, returns the information
                                    as a list of dictionaries. Defaults to False.
        node_name (str, optional): The name of the node to filter VMs by. Currently not used in the method.

    Returns:
        list: A list of dictionaries containing VM information, including name, VM ID, metrics reference, power state,
              CPU count, memory usage, and uptime. This is returned only if `print_vms` is False.

    Note:
        - The method currently does not use the `node_name` parameter, but it is included for future expansion.
        - The memory usage is reported in GiB, and uptime is formatted in a human-friendly format.
        - VM templates are excluded from the results.
    """
    data = []
    all_vm_refs = self.server.VM.get_all(self.session_id)['Value']
    for i in all_vm_refs:
        data.append(self.server.VM.get_record(self.session_id, i))

    metrics = []
    for i in self.server.VM_metrics.get_all(self.session_id)['Value']:
        mem_cur = (self.server.VM_metrics.get_memory_actual(self.session_id, i))        #TODO ukazuje to skutecne aktualni spotrebu ram?
        time = self.server.VM_metrics.get_start_time(self.session_id, i)
        time = dt.now() - dt.strptime(str(time['Value']), '%Y%m%dT%H:%M:%SZ')

        if mem_cur['Value'] != '0':
            metrics.append({"ref": i,
                            "mem": str(int(mem_cur["Value"]) / 1024 / 1024 / 1024),
                            "uptime": format_timespan(time)
                            })

    guest_metrics = []
    for i in self.server.VM_guest_metrics.get_all(self.session_id)['Value']:
        for j in data:
            if i in j['Value']['guest_metrics']:
                j['Value']['guest_metrics'] = self.server.VM_guest_metrics.get_all_records(self.session_id)['Value'][i]

    if print_vms:
        for row in data:
            row = row['Value']
            if row['is_a_template']:
                continue
            data_metrics = [met for met in metrics if met["ref"] == row["metrics"]]
            if not data_metrics:
                data_metrics = [{'ref': '', 'mem': '0', 'uptime': '0', 'guest': ''}]

            print(f'Name: {row["name_label"]}\n\t'
                  f'vmid: {row["uuid"]}\n\t'
                  f'OpaqueRef metrics: {row["metrics"]}\n\t'
                  # f'OpaqueRef guest metrics: {row["guest_metrics"]}\n\t'
                  f'Power state: {row["power_state"]}\n\t'
                  f'Cpus: {row["VCPUs_max"]}\n\t'
                  f'Description: {row["name_description"]}\n\t'
                  f'Is template: {row["is_a_template"]}\n\t'
                  f'SMem max:{str(int(row["memory_static_max"]) / 1024 / 1024 / 1024)}\n\t'
                  f'SMem min:{str(int(row["memory_static_min"]) / 1024 / 1024 / 1024)}\n\t'
                  f'DMem max:{str(int(row["memory_dynamic_max"]) / 1024 / 1024 / 1024)}\n\t'
                  f'DMem min:{str(int(row["memory_dynamic_min"]) / 1024 / 1024 / 1024)}\n\t'
                  f'Mem used: {data_metrics[0]["mem"]}\n\t'
                  f'HVM boot params: {row["HVM_boot_params"]}\n\t'
                  f'Uptime: {data_metrics[0]["uptime"]}\n\t'
                  f'Consoles: {row["consoles"]}\n\t'
                  )

    #TODO  https: // xapi - project.github.io / xen - api / classes / vm_metrics.html
    #
    else:
        formdata = []
        for row in data:
            row = row['Value']
            if row['is_a_template']:
                continue
            data_metrics = [met for met in metrics if met["ref"] == row["metrics"]]
            if not data_metrics:
                data_metrics = [{'ref': '', 'mem': '0', 'uptime': '0', 'guest': ''}]

            formdata.append({'name': row["name_label"],
                             'vmid': row['uuid'],
                             'OpaqueRef_metrics': row['metrics'],
                             'status': row['power_state'],
                             'cpus': row['VCPUs_max'],
                             'uptime': data_metrics[0]['uptime'],
                             'consoles': row['consoles'],
                             'mem_usage': data_metrics[0]["mem"],
                             'maxmem': str(int(row["memory_dynamic_max"]) / 1024 / 1024 / 1024)}
                            )
        return formdata






