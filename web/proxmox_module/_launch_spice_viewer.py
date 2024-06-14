import subprocess


def launch_spice_viewer(self):
    spice_file = '/tmp/vm_spice.vv'
    with open(spice_file, 'w') as file:
        for key, value in self.spice_config.items():
            file.write(f'{key}={value}\n')
    subprocess.run(['remote-viewer', spice_file])
