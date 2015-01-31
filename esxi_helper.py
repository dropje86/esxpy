#!/usr/bin/env python

import fabric.api as fbapi

fbapi.env.host_string = 'esx01.xs4n1.nl'
fbapi.env.shell = "/bin/sh -l -c"
for c in ['status', 'running', 'stdout']:
    fbapi.output[c] = False


class VirtualMachines(object):
    def __init__(self):
        self._cmd = fbapi.run("vim-cmd vmsvc/getallvms")
        # Split header from "getallvms" into keys
        keys = self._cmd.splitlines()[0].lower().split()
        # ['vmid', 'name', 'file', 'guest', 'os', 'version', 'annotation']
        #
        # 'guest' 'os' elements should be 1 element
        keys.insert(3, keys.pop(3) + keys.pop(3))
        # ['vmid', 'name', 'file', 'guestos', 'version', 'annotation']
        #
        # Insert 'storage' key to refer to type of storage VM is located on
        keys.insert(2, 'storage')
        # ['vmid', 'name', 'storage', 'file', 'guestos', 'version', 'annotation']
        tmplist = self._cmd.splitlines()[1:]

        self._vmlist = self._format(keys, tmplist)

    def _format(self, keys, tmplist):
        "Build list of dicts from raw list"
        result = []
        for i in [ zip(keys, i.split()) for i in tmplist ]:
            result.append({ k:v for k,v in i })
        return result

    def list_vms(self):
        dicts = {}
        for d in self._vmlist:
            dicts[d['name']] = d
        return dicts

    def name_to_id(self, name):
        return self.list_vms()[name]['vmid']

    def get_vm_path(self, name):
        pass
