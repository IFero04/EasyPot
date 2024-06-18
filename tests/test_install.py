import unittest
from app.controllers.install_controller import InstallController

class TestInstallController(unittest.TestCase):
    def setUp(self):
        self.controller = InstallController()

    def test_connect_ssh(self):
        result = self.controller.connect('invalid_host', 22, 'user', 'pass')
        self.assertNotEqual(result, "Connected successfully")

if __name__ == "__main__":
    unittest.main()