def get_templates(self):
    if not self.session_id:
        print("Nejste přihlášeni")
        return

    vm_refs = self.server.VM.get_all(self.session_id)['Value']
    templates = []
    for vm_ref in vm_refs:
        vm_record = self.server.VM.get_record(self.session_id, vm_ref)['Value']
        if vm_record['is_a_template']:
            templates.append((vm_record['name_label'], vm_ref))

    if templates:
        print("Dostupné šablony:")
        for name, ref in templates:
            print(f"{name} - {ref}")
    else:
        print("Nebyly nalezeny žádné šablony.")
