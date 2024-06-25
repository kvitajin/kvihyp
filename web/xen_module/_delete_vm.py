def delete_vm(self, vmid, node_name=None):
    """
    Deletes a virtual machine (VM) identified by its UUID.

    This method attempts to delete a VM on the Xen server using its UUID. It first checks if a session ID is present,
    indicating that the user is logged in. If not, it prints a message indicating the user is not logged in and returns.
    It then retrieves the opaque reference for the VM using its UUID and attempts to destroy the VM. If the operation
    is successful, it prints a confirmation message. Otherwise, it prints an error message with the error description.

    Args:
        vmid (str): The UUID of the VM to be deleted.
        node_name (str, optional): The name of the node where the VM is located. Defaults to None. Currently not used in the method.

    Note:
        - The `node_name` parameter is accepted for future use but is not currently utilized in the method.
        - This method requires that the user is already logged in (i.e., a session ID exists).
    """
    if not self.session_id:
        print("Nejste přihlášeni")
        return
    opaque_ref = self.server.VM.get_by_uuid(self.session_id, vmid)['Value']
    result = self.server.VM.destroy(self.session_id, opaque_ref)
    if result['Status'] == "Success":
        print("Virtuální stroj byl úspěšně smazán")
    else:
        print(f"Nepodařilo se smazat virtuální stroj {result['ErrorDescription']}")
