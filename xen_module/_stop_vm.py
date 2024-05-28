def stop_vm(self, vmid):
    if not self.session_id:
        print("Nejste přihlášeni")
        return

    opaque_ref = self.server.VM.get_by_uuid(self.session_id, vmid)['Value']
    state = self.server.VM.get_power_state(self.session_id, opaque_ref)['Value']
    # print(f'state_from_stop_vm: {state}')
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