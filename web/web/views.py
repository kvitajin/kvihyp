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

# Global dictionary to store single connections to hypervisors
single_connections = {}


def wifi_check():
    """
    Checks if the current WiFi connection is to a specific network (UT99_5g).
    Prints a message if not connected to the specified network.
    """
    if "UT99_5g" not in subprocess.check_output("iw dev | grep ssid", shell=True).decode("utf-8"):
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA SPATNA WIFI')


def get_or_create_connection(connection):
    """
    Retrieves or creates a hypervisor connection object based on the connection type.

    Args:
        connection (Connection): The connection model instance from the database.

    Returns:
        object: A connection object to the specified hypervisor.
    """
    if single_connections.get(connection.id) is None:
        if connection.type == 'Proxmox':
            single_connections[connection.id] = Proxmox(http_host=connection.http_host,
                                                         password=connection.password,
                                                         username=connection.username,
                                                         ip_host=connection.host)
        elif connection.type == 'Xen':
            single_connections[connection.id] = Xen(xen_host=connection.host,
                                                    xen_username=connection.username,
                                                    xen_password=connection.password)
        elif connection.type == 'Qemu':
            single_connections[connection.id] = Qemu()
    return single_connections[connection.id]


def hypervisor_list(request):
    """
    Renders a list of all hypervisors.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered hypervisor list page.
    """
    hypervisors = Web.objects.all()
    return render(request, 'hypervisor_list.html', {'hypervisors': hypervisors})


def hypervisor_detail(request, pk):
    """
   Renders the detail view of a specific hypervisor.

   Args:
       request (HttpRequest): The request object.
       pk (int): The primary key of the hypervisor to display.

   Returns:
       HttpResponse: The rendered hypervisor detail page.
   """
    hypervisor = get_object_or_404(Web, pk=pk)
    return render(request, 'hypervisor_detail.html', {'hypervisor': hypervisor})


def connection_create(request):
    """
    Handles the creation of a new connection. If the request is POST, it processes the form data.
    Otherwise, it displays a blank form for creating a connection.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered connection creation page or redirect to hypervisor list on success.
    """
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
    """
    View for creating a new hypervisor entry.

    This view handles both GET and POST requests. For GET requests, it displays a blank form for creating a hypervisor.
    For POST requests, it processes the form data and creates a new hypervisor entry in the database. Upon successful
    creation, it redirects to the hypervisor list page.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object rendering the hypervisor creation form or redirecting to the hypervisor list page.
    """
    if request.method == 'POST':
        form = HypervisorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hypervisor_list')
    else:
        form = HypervisorForm()
    return render(request, 'hypervisor_form.html', {'form': form})


def proxmox_list(request):
    """
    View for listing all Proxmox nodes.

    This view creates a Proxmox object, retrieves a list of all nodes from the Proxmox server, and renders them
    on the 'proxmox_list.html' template.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object rendering the list of Proxmox nodes.
        """
    proxmox = Proxmox()
    data = proxmox.get_nodes()
    return render(request, 'proxmox_list.html', {'proxmox': data})


def connections(request):
    """
    View for displaying all connections.

    This view first checks the current WiFi connection. Then, it retrieves all connection objects from the database
    and renders them on the 'connections.html' template.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object rendering the list of connections.
    """
    wifi_check()
    connections = Connection.everything()
    # print(f'here: {connections}')
    return render(request, 'connections.html', {'connections': connections})


def node_list(request, db_connection_id):
    """
    View for listing nodes of a specific connection.

    This view retrieves a connection object based on the provided database connection ID. If the connection type
    is 'Proxmox', it fetches the nodes associated with that connection and renders them. For other connection types,
    it renders an empty list.

    Args:
        request: HttpRequest object.
        db_connection_id: The database ID of the connection.

    Returns:
        HttpResponse object rendering the list of nodes for the specified connection.
    """
    connection = get_object_or_404(Connection, id=db_connection_id)
    if connection.type == 'Proxmox':
        conn = get_or_create_connection(connection)
        data = conn.get_nodes()
    else:
        return render(request, 'node_list.html', {'data': []})
    transfer = {"connection_id": connection.id, "type": connection.type, "nodes": data}
    return render(request, 'node_list.html', {'data': transfer})


def list_vms(request, db_connection_id, node_name):
    """
    View for listing VMs under a specific node of a connection.

    This view retrieves a connection object based on the provided database connection ID and the node name. It then
    fetches the VMs associated with that node and connection type ('Proxmox', 'Xen', or 'Qemu') and renders them on
    the 'list_vms.html' template.

    Args:
        request: HttpRequest object.
        db_connection_id: The database ID of the connection.
        node_name: The name of the node under which VMs are listed.

    Returns:
        HttpResponse object rendering the list of VMs for the specified node and connection.
    """
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
    """
    View for listing storages under a specific node of a connection.

    This view retrieves a connection object based on the provided database connection ID and the node name. It then
    fetches the storages associated with that node and renders them on the 'list_storages.html' template.

    Args:
        request: HttpRequest object.
        db_connection_id: The database ID of the connection.
        node_name: The name of the node under which storages are listed.

    Returns:
        HttpResponse object rendering the list of storages for the specified node and connection.
    """
    connection = get_object_or_404(Connection, id=db_connection_id)
    node_names = [node_name]
    conn = get_or_create_connection(connection)
    print(f'imi in views  list storages {node_name}')
    data = conn.get_virt_storage(node_names=node_names)
    return render(request, 'list_storages.html',
                  {'storages': data,
                   'hypervisor': connection.type,
                   'node': node_name,
                   'db_connection_id': db_connection_id})


def storage_detail(request, db_connection_id, node_name, storage_name):
    """
    View for displaying details of a specific storage under a node.

    This view retrieves a connection object based on the provided database connection ID, node name, and storage name.
    It then fetches the details of the specified storage and renders them on the 'storage_detail.html' template.

    Args:
        request: HttpRequest object.
        db_connection_id: The database ID of the connection.
        node_name: The name of the node.
        storage_name: The name of the storage to display details for.

    Returns:
        HttpResponse object rendering the details of the specified storage.
    """
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
    """
    View for creating a new storage under a specific node.

    This view handles both GET and POST requests. For GET requests, it displays a blank form for creating a storage.
    For POST requests, it processes the form data and creates a new storage entry under the specified node and
    connection. It then renders the storage creation form again, possibly with validation errors.

    Args:
        request: HttpRequest object.
        db_connection_id: The database ID of the connection.
        node_name: The name of the node under which the storage is to be created.

    Returns:
        HttpResponse object rendering the storage creation form.
    """
    connection = get_object_or_404(Connection, id=db_connection_id)
    if request.method == 'POST':
        form = StorageForm(request.POST)
        if form.is_valid():
            conn = get_or_create_connection(connection)
            if connection.type == 'Proxmox':
                data = conn.create_virt_storage(node_name=node_name,
                                                   storage='local-hdd',
                                                   vmid=form.cleaned_data['vmid'],
                                                   size=form.cleaned_data['size'])
            elif connection.type == "Xen":

                data = conn.create_virt_storage(storage='Local storage',
                                                vmid=form.cleaned_data['vmid'],
                                                size=form.cleaned_data['size'])
            elif connection.type == "Qemu":
                data = conn.create_virt_storage(storage='Local storage',
                                                vmid=form.cleaned_data['vmid'],
                                                size=form.cleaned_data['size'])
        return render(request, 'storage_create.html',
                      {'form': form})
    else:
        form = StorageForm()
    return render(request, 'storage_create.html', {'form': form})


def vm_start(request, db_connection_id, node_name, vmid):
    """
    View for starting a VM under a specific node.

    This view retrieves a connection object based on the provided database connection ID and node name. It then
    starts the VM with the specified VMID and redirects to the list of VMs under the node.

    Args:
        request: HttpRequest object.
        db_connection_id: The database ID of the connection.
        node_name: The name of the node.
        vmid: The ID of the VM to start.

    Returns:
        HttpResponseRedirect object redirecting to the list of VMs.
    """
    connection = get_object_or_404(Connection, id=db_connection_id)
    conn = get_or_create_connection(connection)
    vmid = int(vmid)
    conn.start_vm(node_name=node_name, vmid=vmid)
    return redirect('list_vms', db_connection_id=db_connection_id, node_name=node_name)


def vm_suspend(request, db_connection_id, node_name, vmid):
    """
    View for suspending a VM under a specific node.

    This view retrieves a connection object based on the provided database connection ID and node name. It then
    suspends the VM with the specified VMID and redirects to the list of VMs under the node.

    Args:
        request: HttpRequest object.
        db_connection_id: The database ID of the connection.
        node_name: The name of the node.
        vmid: The ID of the VM to suspend.

    Returns:
        HttpResponseRedirect object redirecting to the list of VMs.
    """
    connection = get_object_or_404(Connection, id=db_connection_id)
    conn = get_or_create_connection(connection)
    vmid = int(vmid)
    conn.suspend_vm(node_name=node_name, vmid=vmid)
    return redirect('list_vms', db_connection_id=db_connection_id, node_name=node_name)


def vm_stop(request, db_connection_id, node_name, vmid):
    """
    View for stopping a VM under a specific node.

    This view retrieves a connection object based on the provided database connection ID and node name. It then
    stops the VM with the specified VMID and redirects to the list of VMs under the node.

    Args:
        request: HttpRequest object.
        db_connection_id: The database ID of the connection.
        node_name: The name of the node.
        vmid: The ID of the VM to stop.

    Returns:
        HttpResponseRedirect object redirecting to the list of VMs.
    """
    connection = get_object_or_404(Connection, id=db_connection_id)
    conn = get_or_create_connection(connection)
    vmid = int(vmid)
    conn.stop_vm(node_name=node_name, vmid=vmid)
    return redirect('list_vms', db_connection_id=db_connection_id, node_name=node_name)


def vm_delete(request, db_connection_id, node_name, vmid):
    """
    View for deleting a VM under a specific node.

    This view retrieves a connection object based on the provided database connection ID and node name. It then
    deletes the VM with the specified VMID and redirects to the list of VMs under the node.

    Args:
        request: HttpRequest object.
        db_connection_id: The database ID of the connection.
        node_name: The name of the node.
        vmid: The ID of the VM to delete.

    Returns:
        HttpResponseRedirect object redirecting to the list of VMs.
    """
    connection = get_object_or_404(Connection, id=db_connection_id)
    conn = get_or_create_connection(connection)
    conn.delete_vm(node_name=node_name, vmid=vmid)
    return redirect('list_vms', db_connection_id=db_connection_id, node_name=node_name)


def create_vm(request, db_connection_id, node_name):
    """
    View for creating a new VM under a specific node.

    This view handles both GET and POST requests. For GET requests, it displays a blank form for creating a VM.
    For POST requests, it processes the form data and creates a new VM under the specified node and connection.
    Upon successful creation, it redirects to the list of VMs under the node.

    Args:
        request: HttpRequest object.
        db_connection_id: The database ID of the connection.
        node_name: The name of the node under which the VM is to be created.

    Returns:
        HttpResponse object rendering the VM creation form or redirecting to the list of VMs.
    """
    connection = get_object_or_404(Connection, id=db_connection_id)
    if request.method == 'POST':
        form = VMForm(request.POST)
        if form.is_valid():
            conn = get_or_create_connection(connection)
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
    """
    View for creating a snapshot of a VM under a specific node.

    This view retrieves a connection object based on the provided database connection ID and node name. It then
    creates a snapshot of the VM with the specified VMID and redirects to the list of VMs under the node.

    Args:
        request: HttpRequest object.
        db_connection_id: The database ID of the connection.
        node_name: The name of the node.
        vmid: The ID of the VM to snapshot.

    Returns:
        HttpResponseRedirect object redirecting to the list of VMs.
    """
    connection = get_object_or_404(Connection, id=db_connection_id)
    conn = get_or_create_connection(connection)
    conn.create_snapshot(vmid=vmid, node_name=node_name)
    return redirect('list_vms', db_connection_id=db_connection_id, node_name=node_name)


def edit_vm(request, db_connection_id, node_name, vmid):
    """
    View for editing a VM under a specific node.

    This view handles both GET and POST requests. For GET requests, it displays a form pre-filled with the VM's
    current data for editing. For POST requests, it processes the form data and updates the VM under the specified
    node and connection. Upon successful update, it redirects to the list of VMs under the node.

    Args:
        request: HttpRequest object.
        db_connection_id: The database ID of the connection.
        node_name: The name of the node.
        vmid: The ID of the VM to edit.

    Returns:
        HttpResponse object rendering the VM edit form or redirecting to the list of VMs.
    """
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
