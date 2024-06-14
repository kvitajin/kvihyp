def get_nodes(self):
    data = []
    self.nodes.clear()
    vm_refs = self.server.host.get_all(self.session_id)['Value']
    for vm_ref in vm_refs:
        data.append(self.server.host.get_hostname(self.session_id, vm_ref)['Value'])
    return data

