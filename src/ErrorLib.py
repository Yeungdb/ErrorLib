from src.ErrLibUI import ErrLibUI as ErrUI
from src.ErrDBConnector import ErrDBConnector as ErrDBConn
import yaml

class ErrorLib:

    # Constructor
    def __init__(self):
        
        # Attempt to open the config file
        try:
            config_file = open("src/ErrLibConfig.yaml")
        except FileNotFoundError as fnf:
            print(fnf)
            return
        
        # Parse the YAML config file
        errlib_config = yaml.safe_load(config_file)

        # Extract the database data
        db_info = errlib_config.get("Database")

        # Read the needed information about the db
        db_username = db_info.get("username")
        db_name = db_info.get("dbname")
        db_password = db_info.get("password")
        db_host = db_info.get("host")
        db_port = db_info.get("port")

        # Close the config file
        config_file.close()

        # Connect to the database
        self.conn = ErrDBConn(db_name, db_username, db_password, db_host, db_port)

        # Create an instance of the UI
        # ui = ErrUI()

        # Start the UI
        # ui.start_ui()

    def error(ErrorTag, variableNameArray, variableValueArray):
        print("error logged")
        # log the error and return a message

    def __del__(self):
        # Close the db connection
        del(self.conn)

ErrorLib()
