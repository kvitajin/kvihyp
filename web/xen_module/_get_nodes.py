def get_nodes(self):
    """
    Retrieves the hostnames of all nodes from the Xen server.

    This method queries the Xen server for all host references and then iterates over these references to fetch
    the hostname of each. It clears the instance's node list before appending the fetched hostnames to ensure
    the list is up-to-date. The hostnames are collected in a list and returned.

    Returns:
        list: A list of hostnames for all nodes available on the Xen server.
    """
    data = []
    self.nodes.clear()
    vm_refs = self.server.host.get_all(self.session_id)['Value']
    for vm_ref in vm_refs:
        data.append(self.server.host.get_hostname(self.session_id, vm_ref)['Value'])
    return data

