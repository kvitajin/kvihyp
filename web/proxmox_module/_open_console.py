import paramiko

port = 22


def open_console(self):
    """
    Opens an interactive SSH console to the Proxmox server.

    This method establishes an SSH connection to the Proxmox server using the IP address, username, and password
    stored in the instance variables. It then enters an interactive loop, allowing the user to execute commands
    directly on the server. The output of each command is printed to the console. The loop continues until a command
    returns a non-zero exit status, indicating an error or the end of the session, at which point the connection is
    closed.

    Exceptions:
        - Catches and prints any exceptions that occur during the connection or command execution process, such as
          authentication failures or network issues.

    Note:
        - This method uses the Paramiko library to handle the SSH connection.
        - The `PROXMOX_IP_HOST`, `PROXMOX_USERNAME`, and `PROXMOX_PASSWORD` instance variables must be set before
          calling this method.
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.PROXMOX_IP_HOST, port, self.PROXMOX_USERNAME, self.PROXMOX_PASSWORD)

        while True:
            command = str(input("#:"))
            stdin, stdout, stderr = client.exec_command(command)
            print(stdout.read().decode())
            if stdin.channel.recv_exit_status():
                break
        client.close()
    except Exception as e:
        print(f"Nastala chyba: {e}")
