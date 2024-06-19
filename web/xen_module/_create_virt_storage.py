def create_virt_storage(self, storage, vmid, size):
    config = {'devserial': 'scsi-0QEMU_QEMU_HARDDISK_drive-scsi0', 'device':'/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_drive-scsi0-part3'}
    name = f"vm-{vmid}-disk-1"
    description = "mudra sova"
    type = 'ext'
    sm_config = {}
    host = self.server.host.get_all(self.session_id)['Value']
    disc = self.server.SR.get_all_records(self.session_id)['Value']
    # size = 1024*1024*1024*size
    # print(disc)
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
