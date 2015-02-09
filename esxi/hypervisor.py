import esxi.commands as executor
import json
import re


class Hypervisor(object):
    def get_datastores(self):
        getter = executor.ESXiCommands()
        raw = getter.raw_datastores_list()
        datastores = {}
        regex = re.compile(
            r'name = "(?P<name>\w+)",\s+'
            'url = "(?P<url>.+)",\s+'
            'capacity = (?P<capacity>\d+),\s+'
            'freeSpace = (?P<freespace>\d+),\s+'
            '.*\s+'
            'accessible = (?P<accessible>\w+),\s+'
            '.*\s+'
            'type = "(?P<type>\w+)"')

        # datastores are seperated by { }, loop through them
        for block in re.finditer(r'{(.+?)}', raw, flags=re.DOTALL):
            single_block = block.group(1)
            match = re.search(regex, single_block)
            datastores[match.group('name')] = match.groupdict()

        return json.dumps(datastores, indent=4)
