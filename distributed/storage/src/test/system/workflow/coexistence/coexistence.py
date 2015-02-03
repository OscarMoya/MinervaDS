import unittest
import xmlrpclib
from distributed.storage.src.api.client.south import ClientSouthAPI
from distributed.storage.src.api.client.west import ClientWestAPI
from distributed.storage.src.driver.client.default.south import ClientSouthDriver
from distributed.storage.src.driver.client.default.west import ClientWestDriver
from distributed.storage.src.driver.db.file.default import DefaultFileDB
from distributed.storage.src.util.packetmanager import PacketManager
from distributed.storage.src.util.threadmanager import ThreadManager


class Coexistence(unittest.TestCase):
    def setUp(self):

        pipe = self
        #endpoint_db = DefaultEndPointDB()
        file_db = DefaultFileDB()
        wdriver = ClientWestDriver(db=file_db, pipe=pipe)
        wapi = ClientWestAPI(wdriver)
        self.west = wapi

        packet_manager = PacketManager
        sdriver = ClientSouthDriver(packet_manager, pipe)
        sapi = ClientSouthAPI(sdriver)

        self.south = sapi

        ThreadManager.start_method_in_new_thread(self.west.start, ["10.10.254.3", 9797])
        ThreadManager.start_method_in_new_thread(self.south.start, ["10.10.253.3", 9696])


    def test_should_work(self):
        sc = xmlrpclib.ServerProxy("http://10.10.253.3:9696")
        wc = xmlrpclib.ServerProxy("http://10.10.254.3:9797")

        print "West Client Call"
        print wc.ping()
        print "West Client Call OK"

        print "South Client call"
        print sc.ping()
        print "South Client call OK"



        return


    def alert(self, func, **kwargs):
        print "Alert called with kwargs", func, kwargs

if __name__ == "__main__":
    unittest.main()