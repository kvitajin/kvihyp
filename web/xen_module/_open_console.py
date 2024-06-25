def open_console(self, vm_ref):
    """
    Opens a console session for a specified virtual machine (VM) and returns the console's location URL.

    This method attempts to open a console session for the VM identified by its UUID. It first checks if a session ID is present,
    indicating that the user is logged in. If not, it prints a message indicating the user is not logged in and returns None.
    It then retrieves the opaque reference for the VM using its UUID and fetches all console sessions associated with the VM.
    For each console session, it retrieves the console's protocol and location. The method returns the location URL of the first
    console session found. If no console sessions are found, it returns None.

    Args:
        vm_ref (str): The UUID of the VM for which to open a console session.

    Returns:
        str or None: The location URL of the console session if available, otherwise None.

    Note:
        - This method currently returns the location of the first console session found and does not handle multiple console sessions.
        - The user must be logged in (i.e., a session ID must exist) for this method to work.
    """
    if not self.session_id:
        print("Nejste přihlášeni")
        return
    opaque_ref = self.server.VM.get_by_uuid(self.session_id, vm_ref)['Value']
    console = self.server.VM.get_consoles(self.session_id, opaque_ref)['Value']
    print(console)
    for console_ref in console:
        console_type = self.server.console.get_protocol(self.session_id, console_ref)['Value']
        print(console_type)
        console_location = self.server.console.get_location(self.session_id, console_ref)['Value']
        return console_location
    return None