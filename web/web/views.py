from django.shortcuts import render, get_object_or_404, redirect
from .models import Web
from .models import Connection
from .forms import HypervisorForm
from .forms import ConnectionForm
from .forms import StorageForm
from proxmox_module import Proxmox
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


# def hypervisor_edit(request, pk):
#     hypervisor = get_object_or_404(web, pk=pk)
#     if request.method == 'POST':
#         form = HypervisorForm(request.POST, instance=hypervisor)
#         if form.is_valid():
#             form.save()
#             return redirect('hypervisor_list')
#     else:
#         form = HypervisorForm(instance=hypervisor)
#     return render(request, 'hypervisors/hypervisor_form.html', {'form': form})


def proxmox_list(request):
    proxmox = Proxmox()
    data = proxmox.get_nodes()
    return render(request, 'proxmox_list.html', {'proxmox': data})

# def vm_list(request, hypervisor, node):
#     if hypervisor == 'proxmox':
#         proxmox = Proxmox()
#         data = proxmox.list_vms()
#         # print(data)
#         data = sorted(data, key=lambda item: item['vmid'])
#         return render(request, 'list_vms.html', {'vms': data, 'hypervisor': hypervisor, 'node': node})


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
        # print(data)
        # print(vars(conn))
        transfer = {"connection_id": connection.id, "type": connection.type, "nodes": data}
        # TODO potrebuju connection.type (proxmox), conn.id(1), conn.nodes(pve)
        return render(request, 'node_list.html', {'data': transfer})

def list_vms(request, db_connection_id, node_name):
    connection = get_object_or_404(Connection, id=db_connection_id)
    # print (f'Connection: {connection.type}')
    if connection.type == 'Proxmox':
        # print(f'Connection: {connection}')
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

def list_storages(request, db_connection_id, node_name):
    connection = get_object_or_404(Connection, id=db_connection_id)
    if connection.type == 'Proxmox':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Proxmox(http_host=connection.http_host,
                             password=connection.password,
                             username=connection.username,
                             ip_host=connection.host)
        proxmox = single_connections[db_connection_id]
        node_names = [node_name]
        data = proxmox.get_virt_storage(node_names=node_names)
        return render(request, 'list_storages.html',
                      {'storages': data,
                       'hypervisor': 'Proxmox',
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
        proxmox = single_connections[db_connection_id]
        proxmox.start_vm(node_name=node_name, vmid=vmid)
        return redirect('list_vms', db_connection_id=db_connection_id, node_name=node_name)


def vm_suspend(request, db_connection_id, node_name, vmid):
    connection = get_object_or_404(Connection, id=db_connection_id)
    if connection.type == 'Proxmox':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Proxmox(http_host=connection.http_host,
                                                           password=connection.password,
                                                           username=connection.username,
                                                           ip_host=connection.host)
        proxmox = single_connections[db_connection_id]
        proxmox.suspend_vm(node_name=node_name, vmid=vmid)
        return redirect('list_vms', db_connection_id=db_connection_id, node_name=node_name)

def vm_stop(request, db_connection_id, node_name, vmid):
    connection = get_object_or_404(Connection, id=db_connection_id)
    if connection.type == 'Proxmox':
        if single_connections.get(db_connection_id) is None:
            single_connections[db_connection_id] = Proxmox(http_host=connection.http_host,
                                                           password=connection.password,
                                                           username=connection.username,
                                                           ip_host=connection.host)
        proxmox = single_connections[db_connection_id]
        proxmox.stop_vm(node_name=node_name, vmid=vmid)

        return redirect('list_vms', db_connection_id=db_connection_id, node_name=node_name)

