from django.db import models

class Web(models.Model):
    HYPERVISOR_TYPES = [
        ('Proxmox', 'Proxmox'),
        ('Xen', 'Xen'),
        ('Qemu', 'Qemu'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=HYPERVISOR_TYPES)
    address = models.CharField(max_length=255)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Connection(models.Model):
    HYPERVISOR_TYPES = [
        ('Proxmox', 'Proxmox'),
        ('Xen', 'Xen'),
        ('Qemu', 'Qemu'),
    ]
    type = models.CharField(max_length=10, choices=HYPERVISOR_TYPES)
    host = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    http_host = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.type

    def get_host(self):
        return self.host

    @staticmethod
    def everything():
        data = []
        for connection in Connection.objects.all():
            data.append(connection)
        return data

class Vm(models.Model):
    name = models.CharField(max_length=100)
    cores = models.IntegerField()
    memory = models.IntegerField()
    disk_size = models.IntegerField()
    storage = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    last_update = models.DateTimeField(auto_now=True)
    last_error = models.CharField(max_length=100, blank=True, null=True)
    ip = models.CharField(max_length=100, blank=True, null=True)
    port_spice = models.IntegerField(blank=True, null=True)
    params = models.CharField(max_length=100, blank=True, null=True)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)




    def __str__(self):
        return self.name

    @staticmethod
    def everything():
        data = []
        for vm in Vm.objects.all():
            data.append(vm)
        return data