def get_templates(self):
    """
    Retrieves a list of available VM templates from the Xen server.

    This method queries the Xen server for all VM references and filters out the templates based on the 'is_a_template'
    attribute. It then collects the names and references of these templates. If the user is not logged in (i.e., a session ID
    does not exist), it prints a message indicating the user is not logged in and returns. If templates are found, it prints
    a list of available templates. Otherwise, it informs the user that no templates were found.

    Note:
        - This method requires that the user is already logged in (i.e., a session ID exists).
        - The method prints the results directly to the console. For a GUI application, modifications might be needed
          to display the results in the user interface.
    """
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
