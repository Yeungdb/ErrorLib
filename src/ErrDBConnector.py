from psycopg2 import sql, connect

class ErrDBConnector():

    # Constructor
    def __init__(self, database: str, username: str, password: str, host: str="127.0.0.1", port: str="5432"):
        self.conn = None
        try:
            self.conn = connect(dbname=database, user=username, password=password, host=host, port=port)
        except (Exception) as error:
            print(error)

    def insert_into_error(self):
        return

    def _execute_sql(self, statement):

        # Create a cursor
        cursor = self.conn.cursor()

        # Attempt to execute the sql statement
        try:
            cursor.execute(statement)
        except (Exception) as error:
            print(error)

        
        # Attempt to retrieve any results
        try:
            results = cursor.fetchall()
        except(Exception):
            # If no results exist, return None
            results = None

        # Commit any changes to database
        self.conn.commit()

        # Close the cursor
        cursor.close()

        # Return the results
        return results


    # Destructor
    def __del__(self):
        if self.conn is not None:
            self.conn.close()
