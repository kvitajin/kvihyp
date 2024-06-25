from django import forms
from .models import Web, Connection

class HypervisorForm(forms.ModelForm):
    class Meta:
        model = Web
        fields = ['name', 'type', 'address', 'username', 'password']


class ConnectionForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Connection
        fields = ['type', 'host', 'username', 'password']
    def http_host(self):
        self.cleaned_data['http_host'] = 'https://' + self.cleaned_data.get('host') + ':8006/api2/json'
        return self.cleaned_data['http_host']


class StorageForm(forms.Form):
        size = forms.IntegerField(label='Size in GB')
        vmid = forms.CharField(label='VM ID')


class VMForm(forms.Form):
    name = forms.CharField(label='Name')
    cores = forms.IntegerField(label='Cores')
    memory = forms.IntegerField(label='Memory')
    disk_size = forms.IntegerField(label='Disk size')


class EditVMForm(forms.Form):
    cores = forms.IntegerField(label='Cores')
    memory = forms.FloatField(label='Memory')
    disk_size = forms.FloatField(label='Disk size')


