def start_vm(self, vmid, node_name=None):
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