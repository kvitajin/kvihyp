def open_console(self, vm_ref):
    if not self.session_id:
        print("Nejste přihlášeni")
        return
    opaque_ref = self.server.VM.get_by_uuid(self.session_id, vm_ref)['Value']
    console = self.server.VM.get_consoles(self.session_id, opaque_ref)['Value']
    for console_ref in console:
        console_type = self.server.console.get_protocol(self.session_id, console_ref)['Value']
        if console_type == "spice":
            console_location = self.server.console.get_location(self.session_id, console_ref)['Value']
            return console_location
    return None