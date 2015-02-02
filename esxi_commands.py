import fabric.api as fbapi


class ESXiCommands(object):
    fbapi.env.host_string = 'esx01.xs4n1.nl'
    fbapi.env.shell = "/bin/sh -l -c"
    for c in ['status', 'running', 'stdout']:
        fbapi.output[c] = False

    def _run(self, cmd):
        return fbapi.run(cmd)

    def get_vmdks(self, vmxpath):
        cmd = "egrep '\\.vmdk\"$' {0}".format(vmxpath)
        raw_data = self._run(cmd)
        return [ vmdk.split('"')[1] for vmdk in raw_data.splitlines() ]
