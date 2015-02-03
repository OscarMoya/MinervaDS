from SimpleXMLRPCServer import SimpleXMLRPCServer
import time
import xmlrpclib

from distributed.storage.src.module.client.manager import ClientManager
from distributed.storage.src.module.controller.manager import ControllerManager
from distributed.storage.src.module.server.manager import ServerManager
from distributed.storage.src.test.mock.client.mockedchannel import MockedChannel
from distributed.storage.src.util.threadmanager import ThreadManager

import unittest

class ClientManagerWorkFlow(unittest.TestCase):

    def setUp(self):
        self.client_id = "ClientTestID"
        self.server_id = "ServerTestID"

        self.ct_mgmt_ip =  "10.10.253.1"
        self.ct_data_ip = "10.10.254.1"

        self.s_mgmt_ip =  "10.10.253.2"
        self.s_data_ip = "10.10.254.2"

        self.cl_mgmt_ip =  "10.10.253.3"
        self.cl_data_ip = "10.10.254.3"

        self.data_port = 9696
        self.mgmt_port = 9797
        self.data = "Hello World"


        self.controller_manager = ControllerManager()
        print "Staring Controller Manager...."
        self.controller_manager.start(self.ct_mgmt_ip, self.mgmt_port)
        print "Controller OK"

        time.sleep(1)

        self.client_manager = ClientManager(id = self.client_id)
        self.server_manager = ServerManager(id = self.server_id)

        print "Staring Client_Manager...."
        self.client_manager.start(self.cl_mgmt_ip, self.mgmt_port, self.cl_data_ip, self.data_port)
        print "Client OK"


        time.sleep(1)

        print "Staring Server Manager...."
        self.server_manager.start(self.s_mgmt_ip, self.mgmt_port, self.s_data_ip, self.data_port)
        print "Server OK"

        time.sleep(1)

    def test_normal_operation(self):
        print "Checking DB before upload..."
        self.check_controller_endpoints_after_join()
        print "DB is correct. Preparing to upload a file..."
        time.sleep(1)


        print "About to upload a file..."
        result = self.client_manager.upload_file(self.data, {})
        print "File uploaded, Checking result..."
        self.check_result_is_true(result)
        print "Result OK. Checking manager statuses..."
        self.check_params_after_upload()
        print "Status OK. Preparing to download...\n\n\n"

        """
        time.sleep(1)

        print "About to download a file..."
        result = self.client_manager.download_file(self.file_id)
        print "File Downloaded. Checking Result..."
        self.check_result_is_true(result)
        print "Result OK. Checking manager statuses..."
        self.check_params_after_download()
        print "Status OK. preparing to leave..."

        time.sleep(1)
        print "Client is about to leave..."
        result = self.client_manager.leave()
        print "Client leaved the controller. Checking result..."
        self.check_result_is_true(result)
        print "Result OK. Checking manager statuses..."
        self.check_params_after_client_leave()
        print "Status OK. preparing the server to leave the controller"

        time.sleep(1)
        print "Server is about to leave..."
        result = self.server_manager.leave()
        print "Server leaved the controller. Checking result..."
        self.check_result_is_true(result)
        print "Result OK. Checking manager statuses..."
        self.check_params_after_server_leave()
        print "Status OK"
        print "Test Finalised"
        """

    def check_result_is_true(self, result):
        self.assertTrue(result)

    def check_params_after_upload(self):
        db = self.server_manager.get_db()
        print db.load()


    def check_params_after_download(self):
        pass

    def check_params_after_client_leave(self):
        pass

    def check_params_after_server_leave(self):
        pass

    def check_controller_endpoints_after_join(self):
        end_points = self.controller_manager.active_endpoints

        expected_keys = [self.server_id, self.client_id]
        expected_keys.sort()

        obtained_keys = end_points.keys()
        obtained_keys.sort()

        self.assertEquals(len(expected_keys), len(obtained_keys))
        self.assertEquals(expected_keys, obtained_keys)

        self.check_client_endpoint_result(end_points.get(self.client_id))
        self.check_server_endpoint_result(end_points.get(self.server_id))

    def check_server_endpoint_result(self, endpoint):

        self.check_generic_endpoint_structure(endpoint)

        self.assertEquals("http://10.10.254.2:9696", endpoint.get("data_url"))
        self.assertEquals("http://10.10.253.2:9797", endpoint.get("mgmt_url"))
        self.assertEquals("server", endpoint.get("type"))

    def check_client_endpoint_result(self, endpoint):

        self.check_generic_endpoint_structure(endpoint)

        self.assertEquals("http://10.10.254.3:9696", endpoint.get("data_url"))
        self.assertEquals("http://10.10.253.3:9797", endpoint.get("mgmt_url"))
        self.assertEquals("client", endpoint.get("type"))

    def check_generic_endpoint_structure(self, endpoint):

        expected_keys = ["data_url", "mgmt_url", "type"]
        expected_keys.sort()

        obtained_keys = endpoint.keys()
        obtained_keys.sort()

        self.assertEquals(len(expected_keys), len(obtained_keys))
        self.assertEquals(expected_keys, obtained_keys)


if __name__ == "__main__":
    unittest.main()
