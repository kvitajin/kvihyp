def start_vm(self, vmid, node_name=None):
    """
    Attempts to start a specified virtual machine (VM) on the Xen server.

    This method checks if the user is logged in by verifying the presence of a session ID. If not logged in, it prints a message
    and returns. It then retrieves the opaque reference for the VM using its UUID and checks the current power state of the VM.
    Depending on the power state, it either starts, unpauses, or resumes the VM. The method prints messages to indicate the
    action taken or if the VM is already running. If the action is successful, it prints a success message; otherwise, it prints
    an error message with the error description.

    Args:
        vmid (str): The UUID of the VM to be started.
        node_name (str, optional): The name of the node where the VM is located. Currently not used in the method.

    Note:
        - The method currently does not use the `node_name` parameter, but it is included for future expansion.
        - The user must be logged in (i.e., a session ID must exist) for this method to work.
        - The method handles VMs in 'Running', 'Paused', and 'Suspended' states, attempting to change their state to 'Running'.
    """
    if not self.session_id:
        print("Nejste přihlášeni")
        return
    opaque_ref = self.server.VM.get_by_uuid(self.session_id, vmid)['Value']
    state = self.server.VM.get_power_state(self.session_id, opaque_ref)['Value']
    print(f'state_from_start_vm: {state}')
    if state == "Running":
        print("Virtuální stroj je již spuštěn")
        return
    elif state == "Paused":
        result = self.server.VM.unpause(self.session_id, opaque_ref)
    elif state == "Suspended":
        result = self.server.VM.resume(self.session_id, opaque_ref, False, False)
    else:
        result = self.server.VM.start(self.session_id, opaque_ref, False, False)

    if result['Status'] == "Success":
        print("Virtuální stroj byl úspěšně spuštěn")
    else:
        print(f"Nepodařilo se spustit virtuální stroj {result['ErrorDescription']}")