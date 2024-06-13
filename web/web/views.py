from django.shortcuts import render, get_object_or_404, redirect
from .models import Web
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

