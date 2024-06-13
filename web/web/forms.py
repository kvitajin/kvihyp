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