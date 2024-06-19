def delete_vm(self, vmid, node_name = None):
    if not self.session_id:
        print("Nejste přihlášeni")
        return
    opaque_ref = self.server.VM.get_by_uuid(self.session_id, vmid)['Value']
    result = self.server.VM.destroy(self.session_id, opaque_ref)
    if result['Status'] == "Success":
        print("Virtuální stroj byl úspěšně smazán")
    else:
        print(f"Nepodařilo se smazat virtuální stroj {result['ErrorDescription']}")