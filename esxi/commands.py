try:
    import fabric.api as fbapi
    fbapi.env.host_string = 'esx01.xs4n1.nl'
    fbapi.env.shell = "/bin/sh -l -c"
    for c in ['status', 'running', 'stdout']:
        fbapi.output[c] = False
except ImportError:
    print("\nWARNING: Missing fabric module dependency, assuming this is a test\n")
    pass


class ESXiCommands(object):
    def _run(self, cmd):
        return fbapi.run(cmd)

    def raw_vmdk_output(self, vmx):
        cmd = "egrep '\\.vmdk\"$' {0}".format(vmx)
        return self._run(cmd)
