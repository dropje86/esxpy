#!/usr/bin/env python

import fabric.api as fbapi

fbapi.env.host_string = 'esx01.xs4n1.nl'
fbapi.env.shell = "/bin/sh -l -c"
for c in ['status', 'running', 'stdout']:
    fbapi.output[c] = False


class VirtualMachines(object):
    def __init__(self):
        self._allvms = fbapi.run("vim-cmd vmsvc/getallvms")
        # Split header from "getallvms" into keys
        attribute_names = self._allvms.splitlines()[0].lower().split()
        # ['vmid', 'name', 'file', 'guest', 'os', 'version', 'annotation']
        #
        # Join 'guest' and 'os' attributes
        attribute_names.insert(3, attribute.pop(3) + attribute.pop(3))
        # ['vmid', 'name', 'file', 'guestos', 'version', 'annotation']
        #
        # Insert 'storage' key to refer to type of storage VM is located on
        attribute_names.insert(2, 'storage')
        # ['vmid', 'name', 'storage', 'file', 'guestos', 'version', 'annotation']
        allvms_normalized = self._allvms.splitlines()[1:]

        self._inventory = self._build_inventory(attribute_names, allvms_normalized)

    def _build_inventory(self, attributes_names, allvms_normalized):
        inventory = []
        for metadata in [ zip(attribute_names, attributes.split()) for attributes in allvms_normalized ]:
            inventory.append({ name:attribute for name, attribute in metadata })
        return inventory

    def list_vms(self):
        vm_names = {}
        for vm in self._inventory:
            vm_names[vm['name']] = vm
        return vm_names

    def name_to_id(self, name):
        return self.list_vms()[name]['vmid']

    def get_vm_path(self, name):
        pass
