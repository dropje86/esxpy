#!/usr/bin/env python

class VirtualMachines(object):
    def __init__(self, vm_list):
        self.vm_list = vm_list
        # Split header from "getvm_list" into keys
        attribute_names = self.vm_list.splitlines()[0].lower().split()
        # ['vmid', 'name', 'file', 'guest', 'os', 'version', 'annotation']
        #
        # Join 'guest' and 'os' attributes
        attribute_names.insert(3, attribute_names.pop(3) + attribute_names.pop(3))
        # ['vmid', 'name', 'file', 'guestos', 'version', 'annotation']
        #
        # Insert 'storage' key to refer to type of storage VM is located on
        attribute_names.insert(2, 'storage')
        # ['vmid', 'name', 'storage', 'file', 'guestos', 'version', 'annotation']
        vm_list_normalized = self.vm_list.splitlines()[1:]

        self.inventory = self._build_inventory(attribute_names, vm_list_normalized)

    def _build_inventory(self, attribute_names, vm_list_normalized):
        inventory = []
        for metadata in [ zip(attribute_names, attributes.split()) for attributes in vm_list_normalized ]:
            inventory.append({ name:attribute for name, attribute in metadata })
        return inventory

    def list_vms(self):
        vm_names = {}
        for vm in self.inventory:
            vm_names[vm['name']] = vm
        return vm_names

    def name_to_id(self, name):
        return self.list_vms()[name]['vmid']

    def get_vm_path(self, name):
        pass
