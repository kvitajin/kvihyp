import datetime


def create_snapshot(self, vmid, node_name=None):
    if not node_name:
        node_name = self.get_nodes()[0]
    print("IM in create snapshot")
    snapname = f"snapshot-{vmid}-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}"

    print(self.PROXMOX_HTTP_HOST)
    url = f"{self.PROXMOX_HTTP_HOST}/nodes/{node_name}/qemu/{vmid}/snapshot"
    data = {
        'snapname': snapname,
    }
    response = self.session.post(url, data=data, headers=self.csrf_token, cookies=self.ticket, verify=False)
    if response.status_code == 200:
        print(f'snapshot uspesne vytvoren')
    else:
        print(f'neco se nepovedlo, duvod: {response.reason}')
    return response
