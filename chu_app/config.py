def get_db_config():
    """Returns a dictionary containing database's informations, which are used
    by the following method : mysql.connector.connect()"""
    config = {
            "host" : "localhost",
            "user" : "root",
            "password" : "example",
            "port" : "3307",
            "database" : "CHU_Caen"
    }

    return config