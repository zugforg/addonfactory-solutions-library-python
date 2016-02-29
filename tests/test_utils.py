import sys
import os
import signal
import datetime
import os.path as op
import unittest as ut

sys.path.insert(0, op.dirname(op.dirname(op.abspath(__file__))))
from splunksolutionlib.common import utils as utils

should_tear_down = False


def sig_handler(signum, frame):
    global should_tear_down
    should_tear_down = True


class TestUtils(ut.TestCase):

    def test_handle_tear_down_signals(self):
        utils.handle_tear_down_signals(sig_handler)
        os.kill(os.getpid(), signal.SIGINT)
        self.assertTrue(should_tear_down)

    def test_datatime_to_seconds(self):
        total_seconds = 1456755646.0
        dt = datetime.datetime(2016, 2, 29, 14, 20, 46, 0)
        self.assertTrue(total_seconds == utils.datetime_to_seconds(dt))

    def test_is_false(self):
        for val in ('0', 'FALSE', 'F', 'N', 'NO', 'NONE', '', None):
            self.assertTrue(utils.is_false(val))

        for val in ('1', 'TRUE', 'T', 'Y', 'YES'):
            self.assertFalse(utils.is_false(val))

        for val in ('00', 'FF', 'NN', 'NONO', '434324'):
            self.assertFalse(utils.is_false(val))

    def test_is_true(self):
        for val in ('0', 'FALSE', 'F', 'N', 'NO', 'NONE', '', None):
            self.assertFalse(utils.is_true(val))

        for val in ('1', 'TRUE', 'T', 'Y', 'YES'):
            self.assertTrue(utils.is_true(val))

        for val in ('00', 'FF', 'NN', 'NONO', '434324'):
            self.assertFalse(utils.is_true(val))

    def test_get_appname_from_path(self):
        app_name = 'Splunk_TA_test'

        normal = '/opt/splunk/etc/apps/Splunk_TA_test/bin/test_mod.py'
        double_slash = '/opt/splunk/etc//apps//Splunk_TA_test/bin/test_mod.py'
        apps_prefix = '/apps/opt/splunk/etc//apps//Splunk_TA_test/bin/test_mod.py'
        slave = '/opt/splunk/etc/slave-apps/Splunk_TA_test/bin/test_mod.py'
        apps_prefix_slave = '/apps/opt/splunk/etc/slave-apps/Splunk_TA_test/bin/test_mod.py'
        double_slash_slave = '/opt/splunk/etc//slave-apps//Splunk_TA_test/bin/test_mod.py'
        master = '/opt/splunk/etc/master-apps/Splunk_TA_test/bin/test_mod.py'
        apps_prefix_master = '/apps/opt/splunk/etc/master-apps/Splunk_TA_test/bin/test_mod.py'
        double_slash_master = '/opt/splunk/etc//master-apps//Splunk_TA_test/bin/test_mod.py'
        paths = [normal, double_slash, apps_prefix,
                 slave, apps_prefix_slave, double_slash_slave,
                 master, apps_prefix_master, double_slash_master]

        for path in paths:
            name = utils.get_appname_from_path(path)
            self.assertEqual(name, app_name)

        path1 = '/apps/opt/splunk/etc2/apps/app1/bin/a.py'
        app = utils.get_appname_from_path(path1)
        self.assertEqual(app, None)

    def test_remove_http_proxy_env_vars(self):
        os.environ['HTTP_PROXY'] = 'TEST'
        os.environ['HTTPS_PROXY'] = 'TEST'
        utils.remove_http_proxy_env_vars()
        self.assertTrue('HTTP_PROXY' not in os.environ)
        self.assertTrue('HTTPS_PROXY' not in os.environ)

        os.environ['http_proxy'] = 'TEST'
        os.environ['https_proxy'] = 'TEST'
        utils.remove_http_proxy_env_vars()
        self.assertTrue('http_proxy' not in os.environ)
        self.assertTrue('https_proxy' not in os.environ)

    def test_escape_json_control_chars(self):
        str1 = r'hello\nworld'
        escaped_str1 = r'hello\\nworld'
        self.assertTrue(escaped_str1 ==
                        utils.escape_json_control_chars(str1))

        str1 = r'hello\rworld'
        escaped_str1 = r'hello\\rworld'
        self.assertTrue(escaped_str1 ==
                        utils.escape_json_control_chars(str1))

        str1 = r'hello\r\nworld'
        escaped_str1 = r'hello\\r\\nworld'
        self.assertTrue(escaped_str1 ==
                        utils.escape_json_control_chars(str1))

if __name__ == '__main__':
    ut.main()
