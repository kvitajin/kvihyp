from django.shortcuts import render, get_object_or_404, redirect
from .models import Web
from .models import Connection
from .forms import HypervisorForm
from .forms import ConnectionForm
from .forms import StorageForm
from .forms import VMForm
from .forms import EditVMForm
from proxmox_module import Proxmox
from xen_module import Xen
from qemu_module import Qemu
from .models import Vm
import subprocess
import json

single_connections = {}


def wifi_check():
    if "UT99_5g" not in subprocess.check_output("iw dev | grep ssid", shell=True).decode("utf-8"):
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA SPATNA WIFI')


def hypervisor_list(request):
    hypervisors = Web.objects.all()
    return render(request, 'hypervisor_list.html', {'hypervisors': hypervisors})


def hypervisor_detail(request, pk):
    hypervisor = get_object_or_404(Web, pk=pk)
    return render(request, 'hypervisor_detail.html', {'hypervisor': hypervisor})


def connection_create(request):
    if request.method == 'POST':
        form = ConnectionForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['type'] == 'Proxmox':
                form_with_http_host = form.save(commit=False)
                form_with_http_host.http_host = 'https://' + form.cleaned_data['host'] + ':8006/api2/json'
                form_with_http_host.save()
            elif form.cleaned_data['type'] == 'Xen':
                form.save()
            return redirect('hypervisor_list')
    else:
        form = ConnectionForm()
    return render(request, 'connection_form.html', {'form': form})


def hypervisor_create(request):
    if request.method == 'POST':
        form = HypervisorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hypervisor_list')
    else:
        form = HypervisorForm()
    return render(request, 'hypervisor_form.html', {'form': form})


def proxmox_list(request):
    proxmox = Proxmox()
    data = proxmox.get_nodes()
    return render(request, 'proxmox_list.html', {'proxmox': data})


def connections(request):
    wifi_check()
    connections = Connection.everything()
    # print(f'here: {connections}')
    return render(request, 'connections.html', {'connections': connections})


def node_list(request, db_connection_id):
    connection = get_object_or_404(Connection, id=db_connection_id)
    if connection.type == 'Proxmox':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Proxmox(http_host=connection.http_host,
                                                           password=connection.password,
                                                           username=connection.username,
                                                           ip_host=connection.host)
        proxmox = single_connections[db_connection_id]
        data = proxmox.get_nodes()

    elif connection.type == 'Xen':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Xen(xen_host=connection.host,
                                                       xen_username=connection.username,
                                                       xen_password=connection.password)
        xen = single_connections[db_connection_id]
        data = xen.get_nodes()
    elif connection.type == 'Qemu':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Qemu()
        qemu = single_connections[db_connection_id]
        data = qemu.get_nodes()
    else:
        return render(request, 'node_list.html', {'data': []})
    transfer = {"connection_id": connection.id, "type": connection.type, "nodes": data}
    return render(request, 'node_list.html', {'data': transfer})


def list_vms(request, db_connection_id, node_name):
    connection = get_object_or_404(Connection, id=db_connection_id)
    if connection.type == 'Proxmox':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Proxmox(http_host=connection.http_host,
                                                           password=connection.password,
                                                           username=connection.username,
                                                           ip_host=connection.host)
        proxmox = single_connections[db_connection_id]
        node_names = [node_name]
        data = proxmox.list_vms(node_names=node_names)
        # print("im here")
        data = sorted(data, key=lambda item: item['vmid'])
        return render(request, 'list_vms.html',
                      {'vms': data,
                       'hypervisor': 'Proxmox',
                       'node': node_name,
                       'db_connection_id': db_connection_id})
    elif connection.type == 'Xen':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Xen(xen_host=connection.host,
                                                       xen_username=connection.username,
                                                       xen_password=connection.password)
        xen = single_connections[db_connection_id]
        data = xen.get_vms(node_name=node_name)
        return render(request, 'list_vms.html',
                      {'vms': data,
                           'hypervisor': 'Xen',
                       'node': node_name,
                       'db_connection_id': db_connection_id})
    elif connection.type == 'Qemu':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Qemu()
        qemu = single_connections[db_connection_id]
        data = qemu.list_vms(node_name=node_name)
        return render(request, 'list_vms.html',
                      {'vms': data,
                       'hypervisor': 'Qemu',
                       'node': node_name,
                       'db_connection_id': db_connection_id})


def list_storages(request, db_connection_id, node_name):
    connection = get_object_or_404(Connection, id=db_connection_id)
    node_names = [node_name]
    if connection.type == 'Proxmox':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Proxmox(http_host=connection.http_host,
                                                           password=connection.password,
                                                           username=connection.username,
                                                           ip_host=connection.host)
    elif connection.type == "Xen":
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Xen(xen_host=connection.host,
                                                       xen_username=connection.username,
                                                       xen_password=connection.password)
    elif connection.type == "Qemu":
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Qemu()

    conn = single_connections[db_connection_id]
    print(f'imi in views  list storages {node_name}')
    data = conn.get_virt_storage(node_names=node_names)
    return render(request, 'list_storages.html',
                  {'storages': data,
                   'hypervisor': connection.type,
                   'node': node_name,
                   'db_connection_id': db_connection_id})


def storage_detail(request, db_connection_id, node_name, storage_name):
    connection = get_object_or_404(Connection, id=db_connection_id)
    if connection.type == 'Proxmox':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Proxmox(http_host=connection.http_host,
                                                           password=connection.password,
                                                           username=connection.username,
                                                           ip_host=connection.host)
        proxmox = single_connections[db_connection_id]
        data = proxmox.get_virt_detail(node_name=node_name, storage_name=storage_name)
        print(json.dumps(data, indent=4))

        return render(request, 'storage_detail.html',
                      {'data': data,
                       'hypervisor': 'Proxmox',
                       'node': node_name,
                       'storage': storage_name,
                       'db_connection_id': db_connection_id})


def storage_create(request, db_connection_id, node_name):
    connection = get_object_or_404(Connection, id=db_connection_id)
    if request.method == 'POST':
        form = StorageForm(request.POST)
        if form.is_valid():
            if connection.type == 'Proxmox':
                if single_connections.get(db_connection_id) is None:
                    single_connections[db_connection_id] = Proxmox(http_host=connection.http_host,
                                                                   password=connection.password,
                                                                   username=connection.username,
                                                                   ip_host=connection.host)
                proxmox = single_connections[db_connection_id]
                data = proxmox.create_virt_storage(node_name=node_name,
                                                   storage='local-hdd',
                                                   vmid=form.cleaned_data['vmid'],
                                                   size=form.cleaned_data['size'])
            elif connection.type == "Xen":
                if single_connections.get(db_connection_id) is None:
                    single_connections[db_connection_id] = Xen(xen_host=connection.host,
                                                               xen_username=connection.username,
                                                               xen_password=connection.password)
                conn = single_connections[db_connection_id]
                data = conn.create_virt_storage(storage='Local storage',
                                                vmid=form.cleaned_data['vmid'],
                                                size=form.cleaned_data['size'])
        return render(request, 'storage_create.html',
                      {'form': form})
    else:
        form = StorageForm()
    return render(request, 'storage_create.html', {'form': form})


def vm_start(request, db_connection_id, node_name, vmid):
    connection = get_object_or_404(Connection, id=db_connection_id)
    if connection.type == 'Proxmox':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Proxmox(http_host=connection.http_host,
                                                           password=connection.password,
                                                           username=connection.username,
                                                           ip_host=connection.host)
    elif connection.type == 'Xen':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Xen(xen_host=connection.host,
                                                       xen_username=connection.username,
                                                       xen_password=connection.password)

            # print("im here in side start vm")
            # print(node_name, vmid)
    elif connection.type == 'Qemu':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Qemu()
            # print(node_name, vmid)
    conn = single_connections[db_connection_id]
    # print(f'imi in views {node_name} {type(vmid)}')
    vmid = int(vmid)
    conn.start_vm(node_name=node_name, vmid=vmid)
    return redirect('list_vms', db_connection_id=db_connection_id, node_name=node_name)


def vm_suspend(request, db_connection_id, node_name, vmid):
    connection = get_object_or_404(Connection, id=db_connection_id)
    if connection.type == 'Proxmox':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Proxmox(http_host=connection.http_host,
                                                           password=connection.password,
                                                           username=connection.username,
                                                           ip_host=connection.host)
    elif connection.type == 'Xen':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Xen(xen_host=connection.host,
                                                       xen_username=connection.username,
                                                       xen_password=connection.password)
    elif connection.type == 'Qemu':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Qemu()
    conn = single_connections[db_connection_id]
    vmid = int(vmid)
    conn.suspend_vm(node_name=node_name, vmid=vmid)
    return redirect('list_vms', db_connection_id=db_connection_id, node_name=node_name)


def vm_stop(request, db_connection_id, node_name, vmid):
    connection = get_object_or_404(Connection, id=db_connection_id)
    if connection.type == 'Proxmox':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Proxmox(http_host=connection.http_host,
                                                           password=connection.password,
                                                           username=connection.username,
                                                           ip_host=connection.host)
    elif connection.type == "Xen":
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Xen(xen_host=connection.host,
                                                       xen_username=connection.username,
                                                       xen_password=connection.password)
    elif connection.type == "Qemu":
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Qemu()
    conn = single_connections[db_connection_id]
    vmid = int(vmid)
    conn.stop_vm(node_name=node_name, vmid=vmid)
    return redirect('list_vms', db_connection_id=db_connection_id, node_name=node_name)


def vm_delete(request, db_connection_id, node_name, vmid):
    connection = get_object_or_404(Connection, id=db_connection_id)
    if connection.type == 'Proxmox':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Proxmox(http_host=connection.http_host,
                                                           password=connection.password,
                                                           username=connection.username,
                                                           ip_host=connection.host)
    elif connection.type == "Xen":
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Xen(xen_host=connection.host,
                                                       xen_username=connection.username,
                                                       xen_password=connection.password)
    conn = single_connections[db_connection_id]
    conn.delete_vm(node_name=node_name, vmid=vmid)
    return redirect('list_vms', db_connection_id=db_connection_id, node_name=node_name)


def create_vm(request, db_connection_id, node_name):
    connection = get_object_or_404(Connection, id=db_connection_id)
    if request.method == 'POST':
        form = VMForm(request.POST)
        if form.is_valid():
            if connection.type == 'Proxmox':
                if single_connections.get(db_connection_id) is None:
                    single_connections[db_connection_id] = Proxmox(http_host=connection.http_host,
                                                                   password=connection.password,
                                                                   username=connection.username,
                                                                   ip_host=connection.host)
            elif connection.type == "Xen":
                if single_connections.get(db_connection_id) is None:
                    single_connections[db_connection_id] = Xen(xen_host=connection.host,
                                                               xen_username=connection.username,
                                                               xen_password=connection.password)
            elif connection.type == "Qemu":
                if single_connections.get(db_connection_id) is None:
                    single_connections[db_connection_id] = Qemu()

            conn = single_connections[db_connection_id]
            conn.create_vm(node_name=node_name,
                           name=form.cleaned_data['name'],
                           cores=form.cleaned_data['cores'],
                           memory=form.cleaned_data['memory'],
                           disk_size=form.cleaned_data['disk_size'])
            return redirect('list_vms', db_connection_id=db_connection_id, node_name=node_name)
    else:
        form = VMForm()
    return render(request, 'create_vm.html', {'form': form})


def create_snapshot(request, db_connection_id, node_name, vmid):
    connection = get_object_or_404(Connection, id=db_connection_id)
    if connection.type == 'Proxmox':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Proxmox(http_host=connection.http_host,
                                                           password=connection.password,
                                                           username=connection.username,
                                                           ip_host=connection.host)
    elif connection.type == 'Xen':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Xen(xen_host=connection.host,
                                                       xen_username=connection.username,
                                                       xen_password=connection.password)
    elif connection.type == 'Qemu':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Qemu()
    conn = single_connections[db_connection_id]
    conn.create_snapshot(vmid=vmid, node_name=node_name)
    return redirect('list_vms', db_connection_id=db_connection_id, node_name=node_name)


def edit_vm(request, db_connection_id, node_name, vmid):
    connection = get_object_or_404(Connection, id=db_connection_id)
    if connection.type == "Qemu":
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Qemu()
        vm = Vm.objects.get(id=vmid)

        conn = single_connections[db_connection_id]
        if request.method == 'POST':
            form = EditVMForm(request.POST, initial={'cores': vm.cores, 'memory': vm.memory, 'disk_size': vm.disk_size})
            if form.is_valid():

                conn.edit_vm(vmid=vmid,
                             node_name=node_name,
                             cores=form.cleaned_data['cores'],
                             memory=form.cleaned_data['memory'],
                             disk_size=form.cleaned_data['disk_size'])
                return redirect('list_vms', db_connection_id=db_connection_id, node_name=node_name)
        else:
            form = EditVMForm(initial={'cores': vm.cores, 'memory': vm.memory, 'disk_size': vm.disk_size})
    elif connection.type == "Proxmox":
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Proxmox(http_host=connection.http_host,
                                                           password=connection.password,
                                                           username=connection.username,
                                                           ip_host=connection.host)
        conn = single_connections[db_connection_id]
        vms = conn.list_vms(node_names=[node_name])
        vm = next((vm for vm in vms if vm.get('vmid') == int(vmid)), None)
        # print(f'EDIIIIIIT {vm}, vmid: {vmid}')
        if request.method == 'POST':
            form = EditVMForm(request.POST, initial={'cores': int(vm['cpus']), 'memory': float(vm['maxmem']), 'disk_size': float(vm['disk_size'])})
            if form.is_valid():
                conn.edit_vm(vmid=vmid,
                             node_name=node_name,
                             cores=form.cleaned_data['cores'],
                             memory=form.cleaned_data['memory'],
                             disk_size=form.cleaned_data['disk_size'])
                return redirect('list_vms', db_connection_id=db_connection_id, node_name=node_name)
        else:
            form = EditVMForm(initial={'cores': int(vm['cpus']), 'memory': float(vm['maxmem']), 'disk_size': float(vm['disk_size'])})
    elif connection.type == "Xen":
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Xen(xen_host=connection.host,
                                                       xen_username=connection.username,
                                                       xen_password=connection.password)
        conn = single_connections[db_connection_id]
        vms = conn.get_vms()
        vm = next((vm for vm in vms if vm.get('vmid') == str(vmid)), None)
        print(vm)
        if request.method == 'POST':
            form = EditVMForm(request.POST, initial={'cores': int(vm['cpus']), 'memory': float(vm['maxmem']), 'disk_size': float(0.0)})
            if form.is_valid():
                conn.edit_vm(vmid=vmid,
                             node_name=node_name,
                             cores=form.cleaned_data['cores'],
                             memory=form.cleaned_data['memory'],
                             disk_size=form.cleaned_data['disk_size'])
                return redirect('list_vms', db_connection_id=db_connection_id, node_name=node_name)
        else:
            form = EditVMForm(initial={'cores': int(vm['cpus']), 'memory': float(vm['maxmem']), 'disk_size': float(0.0)})

    return render(request, 'edit_vm.html', {'form': form})
