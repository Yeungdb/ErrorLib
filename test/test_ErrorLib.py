import unittest
from test.TestDB import TestDB
from src.ErrDBConnector import ErrDBConnector as EBDConn

class test_ErrDBConnector(unittest.TestCase):
    
    def test_insert_into_error_log(self):
        testdb = TestDB()
        conn = EBDConn("testdb", "", "")

        assert False

        del(testdb)

    def test_insert_into_error(self):
        testdb = TestDB()
        conn = EBDConn("testdb", "", "")
        
        assert False

        del(testdb)

    def test_get_user_message_from_error_name(self):
        testdb = TestDB()
        conn = EBDConn("testdb", "", "")
        
        assert False

        del(testdb)

    def test_get_error_idx_by_name(self):
        testdb = TestDB()
        conn = EBDConn("testdb", "", "")

        assert False

        del(testdb)

    def test_has_results(self):
        
        conn = EBDConn("testdb", "", "")
        
        assert False

if __name__ == '__main__':
    unittest.main()
