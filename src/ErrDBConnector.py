from psycopg2 import sql, connect

class ErrDBConnector():

    # Constructor
    def __init__(self, database: str, username: str, password: str, host: str="127.0.0.1", port: str="5432"):
        self.conn = None
        try:
            self.conn = connect(dbname=database, user=username, password=password, host=host, port=port)
        except (Exception) as error:
            print(error)

    #
    # insert_into_error_log
    #
    # PURPOSE: insert a record into the ErrorLog table
    # INPUT:
    #   app_name - the name of the app where the error occured
    #   err_name - the name of the error
    #   server_name - the name of the server where the error occurred
    #   code_loc - the location of the error in the code
    #   var_names - an array of variable names
    #   var_vals - an array of values contained by the variables listed
    def insert_into_error_log(self, app_name, err_name, server_name, code_loc, var_names, var_vals):

        # Get the error index from the error name
        err_idx = self.get_error_idx_by_name(err_name)

        # Create the insert query
        insert = sql.SQL(
            "INSERT INTO {table} VALUES ( " +
            "DEFAULT, CURRENT_TIMESTAMP(), {app}, {server}, {err}, {code}, {name}, {value}" +
            ");"
        ).format(
            table=sql.Identifier("ErrorLog"),
            app=sql.Literal(app_name),
            server=sql.Literal(server_name),
            err=sql.Literal(err_idx),
            code=sql.Literal(code_loc),
            name=sql.Literal(var_names),
            value=sql.Literal(var_vals)
        )

        try:
            # Attempt to do the insert
            self._execute_sql(insert)
        except Exception:
            return False

        return True

    #
    # insert_into_error
    #
    # PURPOSE: inserts a record into the 'Error' table
    # INPUT:
    #   tag - a tag associated with this error
    #   name - the name of the error
    #   message - the error message produced by this error
    #   user_message - the message that is returned to the user when this error is logged
    #   author - the name of the user that created this error
    #   approved - a boolean indicating if an admin has approved this error record
    # OUTPUT:
    #   a boolean value indicating the success of the insertion
    def insert_into_error(self, tag, name, message, user_message, author, approved):

        # Create an insert query
        insert = sql.SQL(
            "INSERT INTO {table} VALUES (DEFAULT, {tag}, {name}, {msg}, {user_msg}, {author}, {approved});"
        ).format(
            table=sql.Identifier("Error"),
            tag=sql.Literal(tag),
            name=sql.Literal(name),
            msg=sql.Literal(message),
            user_msg=sql.Literal(user_message),
            author=sql.Literal(author),
            approved=sql.Literal(approved)
        )

        # Attempt to perform the insert
        try:
            self._execute_sql(insert)
        except Exception:
            return False

        return True


    #
    # get_user_message_from_error_name
    #
    # PURPOSE: retrieves the ReturnToUserMessage associated with the error
    #           with name 'name'
    # INPUT:
    #   name - a string containing the name of the error to get the message for
    # OUTPUT:
    #   string containing the ReturnToUserMessage for the specified error, or an
    #   empty string if the error was not found
    def get_user_message_from_error_name(self, name):

        # Create the select statement
        select = sql.SQL(
            "SELECT {user_msg} FROM {table} WHERE {err_name}={name};"
        ).format(
            user_msg=sql.Identifier("ReturnToUserMessage"),
            table=sql.Identifier("Error"),
            err_name=sql.Identifier("ErrorName"),
            name=sql.Literal(name)
        )

        # Declare a result string
        result = ""

        # Execute the query
        try:
            result = self._execute_sql(select)
        except Exception:
            result = ""
            return result

        # Check to make sure results have been returned
        if self._has_results(result):
            result = result[0][0]
        

        return result

    #
    # get_error_idx_by_name
    #
    # PURPOSE: retrieves the error index from the error with the specified name
    # INPUT:
    #   name - a string containing the name of the error to get the index of
    # OUTPUT:
    #   the index of the error, or -1 if the error is not found
    def get_error_idx_by_name(self, name):

        # Create the query
        select = sql.SQL(
            "SELECT {err_idx} FROM {table} WHERE {err_name}={name};"
        ).format(
            err_idx=sql.Identifier("ErrorIndex"),
            table=sql.Identifier("Error"),
            err_name=sql.Identifier("ErrorName"),
            name=sql.Literal(name)
        )

        # Declare a result
        result = -1

        # Attempt to execute the query
        try:
            result = self._execute_sql(select)
        except Exception:
            result = -1
            return result

        # Reshape the result if results were returned
        if self._has_results(result):
            result = result[0][0]

        return result



    #
    # _has_results
    #
    # PURPOSE: checks if a result set contains results
    # INPUT: 
    #   result_set - a result set as returned by _execute_sql
    # OUTPUT:
    #   True if result_set contains results, False otherwise
    def _has_results(self, result_set):
        if len(result_set) > 0 and len(result_set[0]) > 0:
            return True
        else:
            return False


    # 
    # _execute_sql
    #
    # PURPOSE: safely executes an SQL statement and returns any results
    # INPUT:
    #   statement - a Composable SQL statement
    # OUTPUT:
    #   any results returned by the SQL query
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
