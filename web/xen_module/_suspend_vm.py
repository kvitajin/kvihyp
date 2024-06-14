def suspend_vm(self, vm_ref):
    if not self.session_id:
        print("Nejste přihlášeni")
        return
    opaque_ref = self.server.VM.get_by_uuid(self.session_id, vm_ref)['Value']
    state = self.server.VM.get_power_state(self.session_id, opaque_ref)['Value']
    # print(f'state_from_stop_vm: {state}')
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

