from collections import defaultdict
import json

class VirtualMachines(object):
    def __init__(self, vm_list):
        self.vm_list = vm_list
        self.vm_list_normalized = self.vm_list.splitlines()[1:]
        self.headers = self._build_headers()
        self.inventory = self._build_inventory()

    def _build_headers(self):
        headers = self.vm_list.splitlines()[0].lower().split()
        headers.remove('guest')
        headers.insert(2, 'storage')
        return headers

    def _build_inventory(self):
        inventory = defaultdict(dict)
        for metadata in [ zip(self.headers, attributes.split()) for attributes in self.vm_list_normalized ]:
            # use use vm name -> metadata[1][1] as the key
            inventory[metadata[1][1]] = { name:attribute for name, attribute in metadata }
        return inventory

    def list_vms(self):
        return json.dumps(self.inventory, indent=4)

    def name_to_id(self, name):
        return self.inventory[name]['vmid']

    def get_vm_path(self, name):
        storage = self.get_storage(name)
        # Need to check file (vmx) path as VM name could be inaccurate due to renames
        vm_dir = self.get_directory(name)
        return '/vmfs/volumes/{0}/{1}'.format(storage, vm_dir)

    def get_version(self, name):
        return self.inventory[name]['version']

    def get_file(self, name):
        return self.inventory[name]['file']

    def get_directory(self, name):
        return self.inventory[name]['file'].split('/')[0]

    def get_storage(self, name):
        return self.inventory[name]['storage'].strip('][')
