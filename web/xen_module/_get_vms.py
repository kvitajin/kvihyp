import xmlrpc
from datetime import datetime as dt, timedelta
from humanfriendly import format_timespan



def get_vms(self, print_vms=False, node_name=None):
    data = []
    all_vm_refs = self.server.VM.get_all(self.session_id)['Value']
    for i in all_vm_refs:
        data.append(self.server.VM.get_record(self.session_id, i))

    # host_ref = self.server.host_metrics.get_all(self.session_id)
    # print(host_ref)
    # print(self.server.host_metrics.get_memory_total(self.session_id, host_ref['Value'][0]))
    # print(self.server.host_metrics.get_uuid(self.session_id, host_ref['Value'][0]))
    metrics = []
    # print("----------------------Pamet-----------------------------")
    for i in self.server.VM_metrics.get_all(self.session_id)['Value']:
        # print(f'VSE: {i}\n')
        mem_cur = (self.server.VM_metrics.get_memory_actual(self.session_id, i))        #TODO ukazuje to skutecne aktualni spotrebu ram?
        time = self.server.VM_metrics.get_start_time(self.session_id, i)
        time = dt.now() - dt.strptime(str(time['Value']), '%Y%m%dT%H:%M:%SZ')
        # cpu_usage = self.server.host_cpu.get_all(self.session_id)['Value']


        if mem_cur['Value'] != '0':
            metrics.append({"ref": i,
                            "mem": str(int(mem_cur["Value"]) / 1024 / 1024),
                            "uptime": format_timespan(time)
                            })
            # print(f' {i}: mem: {str(int(tmp["Value"])/1024/1024)}, time: {format_timespan(time)}, cpu: {cpu_usage}, '
            #       f'guest: {guest}')
    # print('------------------?---------------------------------------')
    guest_metrics = []
    for i in self.server.VM_guest_metrics.get_all(self.session_id)['Value']:
        # print(i)
        for j in data:
            if i in j['Value']['guest_metrics']:
                j['Value']['guest_metrics'] = self.server.VM_guest_metrics.get_all_records(self.session_id)['Value'][i]
        # guest_metrics.append({"ref": i,
        #                       "guest": self.server.VM_guest_metrics.get_all_records(self.session_id)['Value'][i]
        #                       })
    # for i in data:
    #
    # # for i in self.server.VM_guest_metrics.get_all(self.session_id)['Value']:
    #     guest = self.server.VM_guest_metrics.get_all_records(self.session_id)['Value'] # 'OpaqueRef:4e208302-e050-486a-9f39-6b964164afd6'
    #     # guest_memory = self.server.VM_guest_metrics.get_memory(self.session_id, i)
    #     # print(i[])
    #     if i in guest:
    #         guest = guest[i]
    #     else:
    #         # print(i)
    #         # print(guest)
    #         guest = 'N/A'           #TODO zjistit jak se dostat k guest metrikam
    # all_metrics = (self.server.VM_metrics.get_all_records(self.session_id))
    # for i in all_metrics['Value']:
    #     print(f'{i} : {all_metrics["Value"][i]}')
    # print(all)

    # print(self.server.VM_metrics.get_all(self.session_id))
    # print(self.server.VM_metrics.get_memory_actual(self.session_id, 'OpaqueRef:7a2c7cbf-6920-470b-abe5-d0599de7250a'))
    # print('--------------------------Guest-------------------------------')
    # print(self.server.host.get_all(self.session_id))
    # print(self.server.host.get_host)
    # print(self.server.host.compute_free_memory(self.session_id, 'OpaqueRef:86da3ef3-0803-4dc6-a6e6-88eabc0f3b76'))
    # all_records = self.server.VM.get_all_records(self.session_id)
    # for i in all_records['Value']:
    #     print(f'{i} : {all_records["Value"][i]}')
    print('---------------------------------------------------------')
    if print_vms:
        for row in data:
            row = row['Value']
            if row['is_a_template']:
                continue
            data_metrics = [met for met in metrics if met["ref"] == row["metrics"]]
            if not data_metrics:
                data_metrics = [{'ref': '', 'mem': '0', 'uptime': '0', 'guest': ''}]

            # print(f'guest z data metrik: {data_metrics[0]["guest"]}')
            # print(f'opaque: {row["metrics"]}')
            # network = guest[str(tmp)]
            print(f'Name: {row["name_label"]}\n\t'
                  f'vmid: {row["uuid"]}\n\t'
                  f'OpaqueRef metrics: {row["metrics"]}\n\t'
                  # f'OpaqueRef guest metrics: {row["guest_metrics"]}\n\t'
                  f'Power state: {row["power_state"]}\n\t'
                  f'Cpus: {row["VCPUs_max"]}\n\t'
                  f'Description: {row["name_description"]}\n\t'
                  f'Is template: {row["is_a_template"]}\n\t'
                  f'SMem max:{str(int(row["memory_static_max"]) / 1024 / 1024)}\n\t'
                  f'SMem min:{str(int(row["memory_static_min"]) / 1024 / 1024)}\n\t'
                  f'DMem max:{str(int(row["memory_dynamic_max"]) / 1024 / 1024)}\n\t'
                  f'DMem min:{str(int(row["memory_dynamic_min"]) / 1024 / 1024)}\n\t'
                  f'Mem used: {data_metrics[0]["mem"]}\n\t'
                  f'HVM boot params: {row["HVM_boot_params"]}\n\t'
                  f'Uptime: {data_metrics[0]["uptime"]}\n\t'
                  f'Consoles: {row["consoles"]}\n\t'

                  # f'network: {row["guest_metrics"]["networks"]}\n\t'

                  # f'netwoks: {network}\n\t'
                  # f'guest_memory: {guest_memory}\n\t'
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

            # print(f'guest z data metrik: {data_metrics[0]["guest"]}')
            # print(f'opaque: {row["metrics"]}')
            # network = guest[str(tmp)]
            formdata.append({'name': row["name_label"],
                             'vmid': row['uuid'],
                             'OpaqueRef_metrics': row['metrics'],
                             'status': row['power_state'],
                             'cpus': row['VCPUs_max'],
                             'uptime': data_metrics[0]['uptime'],
                             'consoles': row['consoles'],
                             'mem_usage': data_metrics[0]["mem"],
                             'maxmem': str(int(row["memory_dynamic_max"]) / 1024 / 1024)}
                            )
        return formdata






