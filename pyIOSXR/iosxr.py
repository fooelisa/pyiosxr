import pexpect
import exceptions

#def __execute_rpc__(conn, rpc_command):
#    output = conn.rpc(str(rpc_command))
#
#    if len(output.xpath('/rpc-reply/error')) > 0:
#        raise Exception(output.tostring)
#
#    return output


class IOSXR:

    def __init__(self, hostname, user, password):
        self.hostname = hostname
        self.user = user
        self.password = password

    def open(self):
        device = pexpect.spawn('ssh ' + self.user + '@' + self.hostname)
        index = device.expect(['\(yes\/no\)\?', pexpect.TIMEOUT])
        if index == 0:
          device.sendline('yes')
        elif index == 1:
          pass
        device.expect('password:')
        device.sendline(self.password)
        device.expect('#')
        device.sendline('xml')
        device.expect('XML>')
        self.device = device

    def close(self):
        self.device.kill()

    def load_candidate_config(self, filename=None, config=None):
        raise NotImplementedError

    def compare_config(self):
        raise NotImplementedError

    def commit_config(self):
        raise NotImplementedError

    def discard_config(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError
