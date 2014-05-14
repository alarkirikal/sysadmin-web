import psycopg2
from server import settings


class Postgres(object):
    """ Wrapper for the psycopg2 module """
    
    def __init__(self):
        """ Init the variable with data from settings """
        self.conn = None
        self.constr = "host=%s dbname=%s user=%s password=%s" % (settings.PSQL_HOST
                                                                ,settings.PSQL_NAME
                                                                ,settings.PSQL_USER
                                                                ,settings.PSQL_PASS)

    def connect(self, constr=None):
        """ Function to connect to the database (get a cursor) """

        if constr:
            self.conn = psycopg2.connect(constr)
        else:
            self.conn = psycopg2.connect(self.constr)


    def close(self):
        """ Function to close the db connection """
        if self.conn:
            self.conn.close()

    def execute(self, query, params=None, format=False):
        """ Function to execute a SQL query """

        # In case connection was not previously made
        if not self.conn:
            self.connect()

        # Get cursor object to execute the query
        cursor = self.conn.cursor()

        # Params during execution
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Whether to return data or not (Insert or select)
        if "SELECT" in query:
            data = cursor.fetchall()
            return data
        else:
            self.conn.commit()
            return None
