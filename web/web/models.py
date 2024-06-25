from django.db import models


class Web(models.Model):
    """
    Represents a hypervisor in the system.

    Attributes:
        name (str): The name of the hypervisor.
        type (str): The type of the hypervisor, limited to predefined choices.
        address (str): The network address of the hypervisor.
        username (str): The username for accessing the hypervisor.
        password (str): The password for accessing the hypervisor.
    """
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
    """
    Represents a connection to a hypervisor.

    Attributes:
        type (str): The type of the hypervisor, limited to predefined choices.
        host (str): The host address of the hypervisor.
        password (str): The password for the connection.
        username (str): The username for the connection.
        http_host (str): The full HTTP host URL, optionally stored for convenience.
    """
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
        """
        Returns the host address of the hypervisor.

        Returns:
            str: The host address.
        """
        return self.host

    @staticmethod
    def everything():
        """
        Retrieves all connection instances.

        Returns:
            list: A list of all connection instances.
        """
        data = []
        for connection in Connection.objects.all():
            data.append(connection)
        return data


class Vm(models.Model):
    """
    Represents a virtual machine (VM) in the system.

    Attributes:
        name (str): The name of the VM.
        cores (int): The number of CPU cores allocated to the VM.
        memory (float): The amount of memory (in GB) allocated to the VM.
        disk_size (float): The disk size (in GB) allocated to the VM.
        storage (str): The storage identifier or path used by the VM.
        status (str): The current status of the VM.
        last_update (datetime): The timestamp of the last update to the VM's status.
        last_error (str): The last error message recorded for the VM, if any.
        ip (str): The IP address assigned to the VM, if any.
        port_spice (int): The port number used for SPICE protocol, if any.
        params (str): Additional parameters or configuration options for the VM.
        connection (ForeignKey): A reference to the Connection instance associated with this VM.
    """
    name = models.CharField(max_length=100)
    cores = models.IntegerField()
    memory = models.FloatField()
    disk_size = models.FloatField()
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
        """
        Retrieves all VM instances.

        Returns:
            list: A list of all VM instances.
        """
        data = []
        for vm in Vm.objects.all():
            data.append(vm)
        return data
