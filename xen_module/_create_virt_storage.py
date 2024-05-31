def create_virt_storage(self, storage, vmid, size):
    config = {}
    name = f"vm-{vmid}-disk-1"
    description = "mudra sova"
    type = 'ext'
    sm_config = {}
    host = self.server.host.get_all(self.session_id)['Value']
    result = self.server.SR.create(self.session_id,
                                   host[0],
                                   config,
                                   size,
                                   name,
                                   description,
                                   type,
                                   '',
                                   False,
                                   sm_config)
    if result['Status'] == 'Success':
        print(f'uspesne vytvoreno na {storage}')
    else:
        print(f'neco se nepovedlo, duvod: {result["ErrorDescription"]}')
