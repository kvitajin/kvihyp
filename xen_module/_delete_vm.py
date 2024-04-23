def delete_vm(self, vmid):
    if not self.session_id:
        print("Nejste přihlášeni")
        return

    result = self.server.VM.destroy(self.session_id, vmid)
    if result['Status'] == "Success":
        print("Virtuální stroj byl úspěšně smazán")
    else:
        print(f"Nepodařilo se smazat virtuální stroj {result['ErrorDescription']}")