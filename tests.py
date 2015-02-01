#!/usr/bin/env python
import unittest
from esxi_helper import VirtualMachines

class VirtualMachinesTest(unittest.TestCase):
    def setUp(self):
        self.vm_list  = "Vmid         Name                               File                               Guest OS          Version   Annotation\r\n"
        self.vm_list += "1      reverse.xs4n1.nl   [storage1] reverse.xs4n1.nl/reverse.xs4n1.nl.vmx   other26xLinux64Guest    vmx-07\r\n"
        self.vm_list += "10     app.xs4n1.nl       [storage1] app.xs4n1.nl/app.xs4n1.nl.vmx           otherLinux64Guest       vmx-08\r\n"
        self.vm_list += "17     puppet.xs4n1.nl    [storage1] puppet.xs4n1.nl/puppet.xs4n1.nl.vmx     debian6_64Guest         vmx-08\r\n"
        self.vm_list += "2      radius.xs4n1.nl    [storage1] radius.xs4n1.nl/radius.xs4n1.nl.vmx     centos64Guest           vmx-07\r\n"
        self.vm_list += "3      vpn.xs4n1.nl       [storage1] vpn.xs4n1.nl/vpn.xs4n1.nl.vmx           other26xLinux64Guest    vmx-07\r\n"
        self.vm_list += "4      dns.xs4n1.nl       [storage1] dns.xs4n1.nl/dns.xs4n1.nl.vmx           otherLinux64Guest       vmx-09\r\n"
        self.vm_list += "5      dc.xs4n1.nl        [storage1] dc.xs4n1.nl/dc.xs4n1.nl.vmx             windows7Server64Guest   vmx-07"

        self.vms = VirtualMachines(self.vm_list)

    def test_inventory(self):
        for vm_name in self.vms.inventory.iterkeys():
            self.assertRegexpMatches(self.vms.get_file(vm_name), '^[\w\/\.]+\.vmx$', msg=vm_name)
            self.assertRegexpMatches(self.vms.get_version(vm_name), '^vmx-\d{2}$', msg=vm_name)
            self.assertRegexpMatches(self.vms.name_to_id(vm_name), '^\d+$', msg=vm_name)
            self.assertRegexpMatches(self.vms.get_storage(vm_name), '\[\w+\]', msg=vm_name)

if __name__ == '__main__':
    unittest.main()

