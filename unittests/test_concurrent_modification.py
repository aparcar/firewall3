#!/usr/bin/env python3

import os
from multiprocessing import Process
from subprocess import call, check_call, check_output


def _concurrent_modifications():
    while True:
        call("iptables -N unittest".split())
        call("iptables -A unittest -j ACCEPT -d 127.0.0.1".split())


def test_concurrent_modifications():
    """ call `fw3 reload` while another script (outside fw3) is modifying the
        kernel table via iptables.
    """
    ret = call("fw3 reload".split())
    assert ret == 0

    for i in range(10):
        modifications = Process(target=_concurrent_modifications)
        modifications.start()
        ret = call("fw3 reload".split())
        modifications.kill()

        assert ret == 0

        # check if iptables are intact
        try:
            os.unlink("/var/run/xtables.lock")
        except:
            pass
        output = check_output("iptables -w 1 -L OUTPUT".split())
        lines = len(str(output, "utf-8").splitlines())

        # the default uci config has at least 5 entries
        assert lines > 5
