def stop_vm(self, vmid):
    """
    Attempts to stop a specified virtual machine (VM) on the Xen server.

    This method checks if the user is logged in by verifying the presence of a session ID. If not logged in, it prints a message
    and returns. It then retrieves the opaque reference for the VM using its UUID and checks the current power state of the VM.
    Depending on the power state, it either directly shuts down the VM or first resumes/unpauses the VM before shutting it down.
    The method prints messages to indicate the action taken or if the VM is already halted. If the action is successful, it prints
    a success message; otherwise, it prints an error message with the error description.

    Args:
        vmid (str): The UUID of the VM to be stopped.

    Note:
        - The user must be logged in (i.e., a session ID must exist) for this method to work.
        - The method handles VMs in 'Halted', 'Suspended', and 'Paused' states, attempting to change their state to 'Halted'.
    """
    if not self.session_id:
        print("Nejste přihlášeni")
        return

    opaque_ref = self.server.VM.get_by_uuid(self.session_id, vmid)['Value']
    state = self.server.VM.get_power_state(self.session_id, opaque_ref)['Value']
    if state == "Halted":
        print("Virtuální stroj je již zastaven")
        return
    elif state == "Suspended":
        self.server.VM.resume(self.session_id, opaque_ref, False, False)
    elif state == "Paused":
        self.server.VM.unpause(self.session_id, opaque_ref)
    result = self.server.VM.shutdown(self.session_id, opaque_ref)

    if result['Status'] == "Success":
        print("Virtuální stroj byl úspěšně zastaven")
    else:
        print(f"Nepodařilo se zastavit virtuální stroj {result['ErrorDescription']}")
