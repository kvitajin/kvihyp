from datetime import datetime


def create_snapshot(self, vmid, node_name=None):
    opaque_ref = self.server.VM.get_by_uuid(self.session_id, vmid)['Value']
    snapshot_name = f'{vmid}_{datetime.now().strftime("%Y%m%d%H%M%S")}'
    snapshot_ref = self.server.VM.snapshot(self.session_id, opaque_ref, snapshot_name)
    if snapshot_ref['Status'] != "Success":
        print(f"Failed to create snapshot: {snapshot_ref['ErrorDescription']}")
        return
    print(f'Snapshot {snapshot_name} created successfully.')
    return snapshot_ref['Value']
