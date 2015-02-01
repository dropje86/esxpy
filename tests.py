#!/usr/bin/env python
import unittest
import json
from esxi_helper import VirtualMachines

class VirtualMachinesTest(unittest.TestCase):
    def setUp(self):
        self.vm_list = 'Vmid         Name                               File                               Guest OS Version   Annotation\r\n1      reverse.xs4n1.nl   [storage1] reverse.xs4n1.nl/reverse.xs4n1.nl.  vmx   other26xLinux64Guest    vmx-07              \r\n10     app.xs4n1.nl       [storage1] app.xs4n1.nl /app.xs4n1.nl.vmx           otherLinux64Guest       vmx-08              \r\n17     puppet.xs4n1.nl    [ storage1] puppet.xs4n1.nl/puppet.xs4n1.nl.vmx     debian6_64Guest         vmx-08              \r\n2 radius.xs4n1.nl    [storage1] radius.xs4n1.nl/radius.xs4n1.nl.vmx     centos64Guest           vmx-07 \r\n3      vpn.xs4n1.nl       [storage1] vpn.xs4n1.nl/vpn.xs4n1.nl.vmx           other26xL inux64Guest    vmx-07              \r\n4      dns.xs4n1.nl       [storage1] dns.xs4n1.nl/dns.xs4n1.nl.v mx           otherLinux64Guest       vmx-09              \r\n5      dc.xs4n1.nl        [storage1] dc.xs 4n1.nl/dc.xs4n1.nl.vmx             windows7Server64Guest   vmx-07'

        self.vms = VirtualMachines(self.vm_list)

    def test_list_vms(self):
        print self.vms.list_vms()

    def test_name_to_id(self):
        name = 'dc.xs4n1.nl'
        self.assertEqual(self.vms.name_to_id(name), '5')

if __name__ == '__main__':
    unittest.main()

