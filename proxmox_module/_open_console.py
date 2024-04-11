import paramiko

port = 22


def open_console(self):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.PROXMOX_IP_HOST, port, self.PROXMOX_USERNAME, self.PROXMOX_PASSWORD)

        while True:
            command = str(input("Enter command: "))
            stdin, stdout, stderr = client.exec_command(command)
            print(stdout.read().decode())
            if stdin.channel.recv_exit_status():
                break
        client.close()
    except Exception as e:
        print(f"Nastala chyba: {e}")
