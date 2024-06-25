from django import forms
from .models import Web, Connection


class HypervisorForm(forms.ModelForm):
    """
    Form for creating or updating Hypervisor instances.

    This form is linked to the `Web` model and allows for the input of hypervisor details such as name, type, address, username, and password.
    """
    class Meta:
        model = Web
        fields = ['name', 'type', 'address', 'username', 'password']


class ConnectionForm(forms.ModelForm):
    """
    Form for creating or updating Connection instances.

    This form is linked to the `Connection` model and includes a password field with a widget set to `PasswordInput` to hide the password input. It also defines a method to construct a full HTTP host URL from the host field.
    """
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Connection
        fields = ['type', 'host', 'username', 'password']

    def http_host(self):
        """
        Constructs a full HTTP host URL from the `host` field.

        Returns:
            str: The full HTTP host URL.
        """
        self.cleaned_data['http_host'] = 'https://' + self.cleaned_data.get('host') + ':8006/api2/json'
        return self.cleaned_data['http_host']


class StorageForm(forms.Form):
    """
    Form for specifying storage size and VM ID.

    This simple form collects information about the desired storage size in GB and the VM ID to which it applies.
    """
    size = forms.FloatField(label='Size in GB')
    vmid = forms.CharField(label='VM ID')


class VMForm(forms.Form):
    """
    Form for specifying basic configurations of a virtual machine.

    This form collects information about the VM's name, number of cores, memory in GB, and disk size in GB.
    """
    name = forms.CharField(label='Name')
    cores = forms.IntegerField(label='Cores')
    memory = forms.FloatField(label='Memory ')
    disk_size = forms.FloatField(label='Disk size')


class EditVMForm(forms.Form):
    """
    Form for editing the configurations of an existing virtual machine.

    Allows for the adjustment of a VM's cores, memory, and disk size, with memory and disk size accepting floating-point inputs for finer granularity.
    """
    cores = forms.IntegerField(label='Cores')
    memory = forms.FloatField(label='Memory')
    disk_size = forms.FloatField(label='Disk size')


