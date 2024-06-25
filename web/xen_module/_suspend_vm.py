def suspend_vm(self, vm_ref):
    """
    Suspends a specified virtual machine (VM) if it is currently running.

    This method checks if the user is logged in by verifying the presence of a session ID. If not logged in, it prints a message
    and returns. It then retrieves the opaque reference for the VM using its UUID and checks the current power state of the VM.
    If the VM is already paused or suspended, it returns immediately. If the VM is halted, it prints a message indicating that
    the VM is stopped and returns. If the VM is running, it attempts to pause the VM. It prints a success message if the operation
    is successful, otherwise, it prints an error message with the error description.

    Args:
        vm_ref (str): The UUID of the VM to be suspended.

    Note:
        - The user must be logged in (i.e., a session ID must exist) for this method to work.
        - The method handles VMs in 'Running', 'Paused', 'Suspended', and 'Halted' states, attempting to change their state to 'Paused'.
    """
    if not self.session_id:
        print("Nejste přihlášeni")
        return
    opaque_ref = self.server.VM.get_by_uuid(self.session_id, vm_ref)['Value']
    state = self.server.VM.get_power_state(self.session_id, opaque_ref)['Value']
    if state == "Paused":
        print("Virtuální stroj je již pozastaven")
        return
    elif state == "Suspended":
        return
    elif state == "Halted":
        print("Virtuální stroj je zastaven")
        return
    elif state == "Running":
        result = self.server.VM.pause(self.session_id, opaque_ref)

    if result['Status'] == "Success":
        print("Virtuální stroj byl úspěšně pozastaven")
    else:
        print(f"Nepodařilo se pozastavit virtuální stroj {result['ErrorDescription']}")

