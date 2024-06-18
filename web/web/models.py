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
        # data = []
        # data.append(str(self.id))
        # data.append(self.type)
        # data.append(self.username)
        # data.append(self.host)
        # return ' '.join(data)
        return self.type

    @staticmethod
    def everything():
        data = []
        for connection in Connection.objects.all():
            data.append(connection)
        return data

