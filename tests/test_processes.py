
#
# Zink
#

from bin.processes import Properties
import unittest


class TestProcesses(unittest.TestCase):

    def testCheckProperties(self):
        properties = Properties("processes.properties")
        self.assertListEqual(properties.processes, ['nginx,', 'uwsgi,', 'postgres'])
        self.assertListEqual(properties.host, "smtp.glo.be")
        self.assertListEqual(properties.port, 1975)
        self.assertListEqual(properties.username, "john.doe@glo.be")
        self.assertListEqual(properties.password, "secret")

if __name__ == "__main__":
    unittest.main()
