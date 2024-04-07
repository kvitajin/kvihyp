def get_nodes(self):
    nodes_url = f'{self.PROXMOX_HOST}/nodes'
    self.nodes_response = self.session.get(nodes_url, verify=False)
    data = self.nodes_response.json()
    self.nodes.clear()
    for row in data['data']:
        self.nodes.append(row['node'])
    if not self.nodes:
        raise Exception('No nodes found')
    return self.nodes
