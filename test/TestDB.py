from src.ErrDBConnector import ErrDBConnector as EDBConn
from psycopg2 import sql

class TestDB():
    def __init__(self):
        # Create a connection to the test db
        self.conn = EDBConn("testdb", "", "")

        # Create tables as described in ErrorLib.sql
        create_tables = sql.SQL(
            "CREATE TABLE IF NOT EXISTS \"Error\" (" +
            "\"ErrorIndex\" SERIAL NOT NULL PRIMARY KEY," +
            "\"ErrorTag\" TEXT NOT NULL," +
            "\"ErrorName\" TEXT NOT NULL," +
            "\"ErrorMessage\" TEXT NOT NULL," +
            "\"ReturnToUserMessage\" TEXT NOT NULL," +
            "\"AuthorName\" TEXT NOT NULL," +
            "\"Approved\" BOOLEAN NOT NULL" +
            "); " +

            "CREATE TABLE IF NOT EXISTS \"ErrorLog\" (" +
            "\"ErrorLogIndex\" SERIAL NOT NULL PRIMARY KEY," +
            "\"CurrentTime\" DATE," +
            "\"AppWhereErrorOccurred\" TEXT," +
            "\"Error\" INTEGER REFERENCES \"Error\"," +
            "\"ServerName\" TEXT," +
            "\"CodeWhereErrorFailed\" TEXT," +
            "\"VariableNameArray\" TEXT," +
            "\"VariableValueArray\" TEXT" +
            ");" +

            "CREATE TABLE IF NOT EXISTS \"Users\" (" +
            "\"UserID\" SERIAL NOT NULL PRIMARY KEY," +
            "\"Password\" TEXT NOT NULL," +
            "\"UserRole\" TEXT NOT NULL" +
            ");"
        )

        try:
            self.conn._execute_sql(create_tables)
        except Exception as e:
            print(e)

    def __del__(self):
        # Drop all the tables
        drop_tables = sql.SQL(
            "DROP TABLE \"ErrorLog\";" +
            "DROP TABLE \"Error\";" + 
            "DROP TABLE \"Users\";"
        )
        self.conn._execute_sql(drop_tables)

TestDB()
