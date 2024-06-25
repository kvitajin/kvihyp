from datetime import datetime


def create_snapshot(self, vmid, node_name=None):
    """
    Creates a snapshot of a specified virtual machine (VM) by its UUID.

    This method attempts to create a snapshot of the VM identified by the given UUID. It constructs a snapshot name
    based on the VM's UUID and the current timestamp, then calls the Xen API to create the snapshot. If the snapshot
    creation is successful, it prints a success message along with the snapshot name. If not, it prints an error message.

    Args:
        self: The instance of the class that contains the connection to the Xen server.
        vmid (str): The UUID of the VM for which the snapshot is to be created.
        node_name (str, optional): The name of the node where the VM is located. Defaults to None.

    Returns:
        str: The reference of the created snapshot if successful, None otherwise.
    """
    opaque_ref = self.server.VM.get_by_uuid(self.session_id, vmid)['Value']
    snapshot_name = f'{vmid}_{datetime.now().strftime("%Y%m%d%H%M%S")}'
    snapshot_ref = self.server.VM.snapshot(self.session_id, opaque_ref, snapshot_name)
    if snapshot_ref['Status'] != "Success":
        print(f"Failed to create snapshot: {snapshot_ref['ErrorDescription']}")
        return
    print(f'Snapshot {snapshot_name} created successfully.')
    return snapshot_ref['Value']
