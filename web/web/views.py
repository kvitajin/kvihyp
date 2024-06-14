from django.shortcuts import render, get_object_or_404, redirect
from .models import Web
from .models import Connection
from .forms import HypervisorForm
from .forms import ConnectionForm
from proxmox_module import Proxmox

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

def vm_list(request, hypervisor, node):
    if hypervisor == 'proxmox':
        proxmox = Proxmox()
        data = proxmox.list_vms()
        # print(data)
        data = sorted(data, key=lambda item: item['vmid'])
        return render(request, 'list_vms.html', {'vms': data, 'hypervisor': hypervisor, 'node': node})

def connections(request):
    connections = Connection.everything()
    # print(f'here: {connections}')
    return render(request, 'connections.html', {'connections': connections})

def connections_detail(request, db_connection_id):
    # connections = get_object_or_404(Connection, pk=db_connection_id)
    # print(f'here: {connections}')
    # TODO - nenacita z proxmoxu, jen z db
    connection = Connection.objects.get(id=db_connection_id)
    print(f'http?host: {connection.http_host}, password: {connection.password}, username: {connection.username}, ip_host: {connection.host}')
    connections = Proxmox(http_host=connection.http_host,
                 password=connection.password,
                 username=connection.username,
                 ip_host=connection.host)
    data = connections.get_nodes()
    print(f'totok: {data}')
    return render(request, 'connections_detail.html', {'connection': connections})