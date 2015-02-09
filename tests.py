#!/usr/bin/env python
import json
import unittest
from mock import Mock
from esxi.commands import ESXiCommands

vmdk_raw  = 'scsi0:0.fileName = "dc.xs4n1.nl_2.vmdk"\r\n'
vmdk_raw += 'ide0:0.fileName = "dc.xs4n1.nl_1.vmdk"'

raw_datastores_list  = '(vim.Datastore.Summary) [\n'
raw_datastores_list += '   (vim.Datastore.Summary) {\n'
raw_datastores_list += '      dynamicType = <unset>,\n'
raw_datastores_list += '      datastore = \'vim.Datastore:525de61c-1391729a-1b74-bc5ff4c9999d\',\n'
raw_datastores_list += '      name = "storage1",\n'
raw_datastores_list += '      url = "/vmfs/volumes/525de61c-1391729a-1b74-bc5ff4c9999d",\n'
raw_datastores_list += '      capacity = 249913409536,\n'
raw_datastores_list += '      freeSpace = 90166001664,\n'
raw_datastores_list += '      uncommitted = 379201849344,\n'
raw_datastores_list += '      accessible = true,\n'
raw_datastores_list += '      multipleHostAccess = <unset>,\n'
raw_datastores_list += '      type = "VMFS",\n'
raw_datastores_list += '      maintenanceMode = <unset>,\n'
raw_datastores_list += '   },\n'
raw_datastores_list += '   (vim.Datastore.Summary) {\n'
raw_datastores_list += '      dynamicType = <unset>,\n'
raw_datastores_list += '      datastore = \'vim.Datastore:192.168.1.10:/c/data\',\n'
raw_datastores_list += '      name = "NAS",\n'
raw_datastores_list += '      url = "/vmfs/volumes/5c302bd7-7ed49668",\n'
raw_datastores_list += '      capacity = 5946967457792,\n'
raw_datastores_list += '      freeSpace = 1339094286336,\n'
raw_datastores_list += '      uncommitted = 0,\n'
raw_datastores_list += '      accessible = true,\n'
raw_datastores_list += '      multipleHostAccess = <unset>,\n'
raw_datastores_list += '      type = "NFS",\n'
raw_datastores_list += '      maintenanceMode = <unset>,\n'
raw_datastores_list += '   }\n'
raw_datastores_list += ']'

ESXiCommands.raw_vmdk_output = Mock(return_value=vmdk_raw)
ESXiCommands.raw_datastores_list = Mock(return_value=raw_datastores_list)

from esxi.hypervisor import Hypervisor
from esxi.inventory import VirtualMachines

vm_list  = "Vmid         Name                               File                               Guest OS          Version   Annotation\r\n"
vm_list += "1      reverse.xs4n1.nl   [storage1] reverse.xs4n1.nl/reverse.xs4n1.nl.vmx   other26xLinux64Guest    vmx-07\r\n"
vm_list += "10     app.xs4n1.nl       [storage1] app.xs4n1.nl/app.xs4n1.nl.vmx           otherLinux64Guest       vmx-08\r\n"
vm_list += "17     puppet.xs4n1.nl    [storage1] puppet.xs4n1.nl/puppet.xs4n1.nl.vmx     debian6_64Guest         vmx-08\r\n"
vm_list += "2      radius.xs4n1.nl    [storage1] radius.xs4n1.nl/radius.xs4n1.nl.vmx     centos64Guest           vmx-07\r\n"
vm_list += "3      vpn.xs4n1.nl       [storage1] vpn.xs4n1.nl/vpn.xs4n1.nl.vmx           other26xLinux64Guest    vmx-07\r\n"
vm_list += "4      dns.xs4n1.nl       [storage1] dns.xs4n1.nl/dns.xs4n1.nl.vmx           otherLinux64Guest       vmx-09\r\n"
vm_list += "5      dc.xs4n1.nl        [storage1] dc.xs4n1.nl/dc.xs4n1.nl.vmx             windows7Server64Guest   vmx-07"


class VirtualMachinesTest(unittest.TestCase):
    def setUp(self):
        self.vms = VirtualMachines(vm_list)

    def test_headers(self):
        self.assertEqual(self.vms.headers,
                ['vmid', 'name', 'storage', 'file', 'os', 'version', 'annotation'])

    def test_get_file(self):
        for vm_name in self.vms.inventory.iterkeys():
            self.assertRegexpMatches(self.vms.get_file(vm_name), '^[\w\/\.]+\.vmx$', msg=vm_name)

    def test_get_version(self):
        for vm_name in self.vms.inventory.iterkeys():
            self.assertRegexpMatches(self.vms.get_version(vm_name), '^vmx-\d{2}$', msg=vm_name)

    def test_name_to_id(self):
        for vm_name in self.vms.inventory.iterkeys():
            self.assertRegexpMatches(self.vms.name_to_id(vm_name), '^\d+$', msg=vm_name)

    def test_get_storage_alias(self):
        for vm_name in self.vms.inventory.iterkeys():
            self.assertRegexpMatches(self.vms.get_storage_alias(vm_name), '\w+', msg=vm_name)

    def test_get_vmx_name(self):
        for vm_name in self.vms.inventory.iterkeys():
            self.assertRegexpMatches(self.vms.get_vmx_name(vm_name), '^\w(|.)+\.vmx$', msg=vm_name)

    def test_get_vm_path(self):
        for vm_name in self.vms.inventory.iterkeys():
            self.assertEqual(self.vms.get_vm_path(vm_name), '/vmfs/volumes/{0}/{1}'.format(
                            self.vms.get_storage_alias(vm_name),
                            self.vms.get_directory(vm_name)),
                    msg=vm_name)

    def test_get_vmx_path(self):
        for vm_name in self.vms.inventory.iterkeys():
            self.assertEqual(self.vms.get_vmx_path(vm_name), '/vmfs/volumes/{0}/{1}'.format(
                            self.vms.get_storage_alias(vm_name),
                            self.vms.get_file(vm_name)),
                    msg=vm_name)

    def test_get_vmdks(self):
        for vm_name in self.vms.inventory.iterkeys():
            self.assertIsInstance(self.vms.get_vmdks(vm_name), list, msg=vm_name)


class HypervisorTest(unittest.TestCase):
    def setUp(self):
        self.hv = Hypervisor()

    def test_get_datastores(self):
        dict_keys = ['name', 'url', 'capacity', 'freespace', 'accessible', 'type']
        datastores = json.loads(self.hv.get_datastores())
        # Test if all dict_keys are available in all datastores
        for name in datastores.iterkeys():
            self.assertTrue(all(key in datastores[name] for key in dict_keys))


if __name__ == '__main__':
    unittest.main()
