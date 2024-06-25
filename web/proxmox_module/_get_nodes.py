def get_nodes(self):
    """
    Retrieves a list of nodes from the Proxmox cluster.

    This method sends a GET request to the Proxmox API to fetch the list of nodes in the cluster.
    It updates the `self.nodes` attribute with the names of the nodes. If no nodes are found, it raises an exception.

    Returns:
        list: A list of node names in the Proxmox cluster.

    Raises:
        Exception: If no nodes are found in the response from the Proxmox API.
    """
    nodes_url = f'{self.PROXMOX_HTTP_HOST}/nodes'
    self.nodes_response = self.session.get(nodes_url, verify=False)
    data = self.nodes_response.json()
    self.nodes.clear()
    for row in data['data']:
        self.nodes.append(row['node'])
    if not self.nodes:
        raise Exception('No nodes found')
    return self.nodes
