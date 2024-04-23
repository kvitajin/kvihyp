def get_vm_info(self, vm_ref):
    return self.server.VM.get_record(self.session_id, vm_ref)


def get_vm_ref(self, vm_ref):
    return self.server.VM.get_by_name_label(self.session_id, vm_ref)


def fuckit(self):
    # return self.server.VM.get_by_name_label(self.session_id)

    return self.server.VM.get_all(self.session_id)['Value']
