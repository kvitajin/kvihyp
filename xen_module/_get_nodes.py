def get_nodes(self, vm_ref):
    self.nodes.clear()
    data = self.server.host.get_hostname(self.session_id, vm_ref)
    print(data)
    # for row in data['Value']:
    #     self.nodes.append(row)
    # if not self.nodes:
    #     raise Exception("No nodes found")
    # return self.nodes

