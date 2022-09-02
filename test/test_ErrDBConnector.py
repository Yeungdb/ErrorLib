import unittest
from psycopg2 import sql
from test.TestDB import TestDB
from src.ErrDBConnector import ErrDBConnector as EBDConn

class test_ErrDBConnector(unittest.TestCase):
    
    def test_insert_into_error_log(self):
        testdb = TestDB()
        conn = EBDConn("testdb", "", "")

        # Define test data
        data = ["app", "errname", "server", "code location", "variable names", "variable values"]

        # Assert the table is empty
        get_any = sql.SQL("SELECT * FROM \"ErrorLog\";")
        assert not conn._has_results(conn._execute_sql(get_any))

        # Insert an Error
        insert_error = sql.SQL(
            "INSERT INTO \"Error\" VALUES (" +
            "DEFAULT, 'tag', 'errname', 'msg', 'user msg', 'author', TRUE" +
            ");"
        )
        try:
            conn._execute_sql(insert_error)
        except Exception as e:
            print(e)
            assert False

        # Insert a record
        conn.insert_into_error_log(*data) # use the splat operator (*) to flatten the array

        # Assert the insert was successful and correct
        results = conn._execute_sql(get_any)
        assert conn._has_results(results)
        assert len(results) == 1
        assert results[0][2] == data[0]
        assert results[0][4] == data[2]
        assert results[0][5] == data[3]
        assert results[0][6] == data[4]
        assert results[0][7] == data[5]


        del(testdb)

    def test_insert_into_error(self):
        testdb = TestDB()
        conn = EBDConn("testdb", "", "")

        # Define test data
        data = ["tag", "name", "msg", "user msg", "author", True]

        # Assert the table is empty
        get_any = sql.SQL("SELECT * FROM \"Error\";")
        assert not conn._has_results(conn._execute_sql(get_any))
        
        # Attempt to insert an error
        conn.insert_into_error(*data)

        # Assert the insert was successful and correct
        results = conn._execute_sql(get_any)
        assert conn._has_results(results)
        assert len(results) == 1
        assert results[0][1] == data[0]
        assert results[0][2] == data[1]
        assert results[0][3] == data[2]
        assert results[0][4] == data[3]
        assert results[0][5] == data[4]
        assert results[0][6] == data[5]

        del(testdb)

    def test_get_user_message_from_error_name(self):
        testdb = TestDB()
        conn = EBDConn("testdb", "", "")
        
        # Define test data
        data = [
            [1, "tag1", "name1", "msg1", "usr msg1", "author1", True],
            [2, "tag2", "name2", "msg2", "usr msg2", "author2", True]            
        ]

        # Assert the table is empty
        get_any = sql.SQL("SELECT * FROM \"Error\";")
        assert not conn._has_results(conn._execute_sql(get_any))

        # Create insert statements
        insert = sql.SQL(
            "INSERT INTO \"Error\" VALUES (" +
            "{idx}, {tag}, {name}, {msg}, {usr_msg}, {auth}, {appr}" +
            ");"
        )

        insert_1 = insert.format(
            idx=sql.Literal(data[0][0]),
            tag=sql.Literal(data[0][1]),
            name=sql.Literal(data[0][2]),
            msg=sql.Literal(data[0][3]),
            usr_msg=sql.Literal(data[0][4]),
            auth=sql.Literal(data[0][5]),
            appr=sql.Literal(data[0][6])
        )

        insert_2 = insert.format(
            idx=sql.Literal(data[1][0]),
            tag=sql.Literal(data[1][1]),
            name=sql.Literal(data[1][2]),
            msg=sql.Literal(data[1][3]),
            usr_msg=sql.Literal(data[1][4]),
            auth=sql.Literal(data[1][5]),
            appr=sql.Literal(data[1][6])
        )

        # Insert records into the table
        try:
            conn._execute_sql(insert_1)
            conn._execute_sql(insert_2)
        except Exception as e:
            print(e)
            assert False

        
        # Assert user error messages can be queried by error name
        assert conn.get_user_message_from_error_name(data[0][2]) == data[0][4]
        assert conn.get_user_message_from_error_name(data[1][2]) == data[1][4]
        assert conn.get_user_message_from_error_name(data[0][2]) != data[1][4]
        assert conn.get_user_message_from_error_name(data[1][2]) != data[0][4]


        del(testdb)

    def test_get_error_idx_by_name(self):
        testdb = TestDB()
        conn = EBDConn("testdb", "", "")

        # Define test data
        data = [
            [1, "tag1", "name1", "msg1", "usr msg1", "author1", True],
            [2, "tag2", "name2", "msg2", "usr msg2", "author2", True]            
        ]

        # Assert the table is empty
        get_any = sql.SQL("SELECT * FROM \"Error\";")
        assert not conn._has_results(conn._execute_sql(get_any))

        # Create insert statements
        insert = sql.SQL(
            "INSERT INTO \"Error\" VALUES (" +
            "{idx}, {tag}, {name}, {msg}, {usr_msg}, {auth}, {appr}" +
            ");"
        )

        insert_1 = insert.format(
            idx=sql.Literal(data[0][0]),
            tag=sql.Literal(data[0][1]),
            name=sql.Literal(data[0][2]),
            msg=sql.Literal(data[0][3]),
            usr_msg=sql.Literal(data[0][4]),
            auth=sql.Literal(data[0][5]),
            appr=sql.Literal(data[0][6])
        )

        insert_2 = insert.format(
            idx=sql.Literal(data[1][0]),
            tag=sql.Literal(data[1][1]),
            name=sql.Literal(data[1][2]),
            msg=sql.Literal(data[1][3]),
            usr_msg=sql.Literal(data[1][4]),
            auth=sql.Literal(data[1][5]),
            appr=sql.Literal(data[1][6])
        )

        # Insert records into the table
        try:
            conn._execute_sql(insert_1)
            conn._execute_sql(insert_2)
        except Exception as e:
            print(e)
            assert False

        
        # Assert error indices can be queried by error name
        assert conn.get_error_idx_by_name(data[0][2]) == data[0][0]
        assert conn.get_error_idx_by_name(data[1][2]) == data [1][0]
        assert conn.get_error_idx_by_name(data[0][2]) != data[1][0]
        assert conn.get_error_idx_by_name(data[1][2]) != data[0][0]


        del(testdb)

    def test_has_results(self):
        
        conn = EBDConn("testdb", "", "")

        # Define test data
        good_results_1 = [["some results"]]
        good_results_2 = [["more", "results"]]
        good_results_3 = [["even"], ["more"], ["results"]]
        good_results_4 = (("results"), ("in"), ("tuples"))
        bad_results_1 = []
        bad_results_2 = [[], []]

        # Assert the method works as expected
        assert conn._has_results(good_results_1)
        assert conn._has_results(good_results_2)
        assert conn._has_results(good_results_3)
        assert conn._has_results(good_results_4)
        assert not conn._has_results(bad_results_1)
        assert not conn._has_results(bad_results_2)
        
        del(conn)

if __name__ == '__main__':
    unittest.main()
