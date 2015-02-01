from collections import defaultdict
import json

class VirtualMachines(object):
    def __init__(self, vm_list):
        self.vm_list = vm_list
        # Split header from "getvm_list" into keys
        self.attribute_names = self.vm_list.splitlines()[0].lower().split()
        # ['vmid', 'name', 'file', 'guest', 'os', 'version', 'annotation']
        #
        # Join 'guest' and 'os' attributes
        self.attribute_names.insert(3, self.attribute_names.pop(3) + self.attribute_names.pop(3))
        # ['vmid', 'name', 'file', 'guestos', 'version', 'annotation']
        #
        # Insert 'storage' key to refer to type of storage VM is located on
        self.attribute_names.insert(2, 'storage')
        # ['vmid', 'name', 'storage', 'file', 'guestos', 'version', 'annotation']
        self.vm_list_normalized = self.vm_list.splitlines()[1:]

        self.inventory = self._build_inventory(self.attribute_names, self.vm_list_normalized)

    def _build_inventory(self, attribute_names, vm_list_normalized):
        inventory = defaultdict(dict)
        for metadata in [ zip(attribute_names, attributes.split()) for attributes in vm_list_normalized ]:
            # use use vm name -> metadata[1][1] as the key
            inventory[metadata[1][1]] = { name:attribute for name, attribute in metadata }
        return inventory

    def list_vms(self):
        return json.dumps(self.inventory, indent=4)

    def name_to_id(self, name):
        return self.inventory[name]['vmid']

    def get_vm_path(self, name):
        pass

    def get_version(self, name):
        return self.inventory[name]['version']

    def get_file(self, name):
        return self.inventory[name]['file']
