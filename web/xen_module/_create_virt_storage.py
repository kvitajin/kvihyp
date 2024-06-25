def create_virt_storage(self, storage, vmid, size):
    """
    Creates virtual storage for a specified VM.

    This method interfaces with the Xen server to create a virtual storage device. It constructs a configuration
    for the storage device, including its name, description, and type, and then calls the Xen API to create the storage.
    If the storage creation is successful, it prints a success message indicating the storage location. Otherwise,
    it prints an error message detailing the reason for failure.

    Args:
        self: The instance of the class that contains the connection to the Xen server.
        storage (str): The storage repository (SR) where the virtual storage will be created.
        vmid (str): The UUID of the VM for which the storage is being created.
        size (int): The size of the virtual storage in bytes.

    Note:
        The `config` dictionary specifies the device configuration for the virtual storage. The `type` is set to 'ext'
        for an extensible file system. The `sm_config` dictionary is empty in this implementation, but can be used
        for additional storage manager configurations.
    """
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
