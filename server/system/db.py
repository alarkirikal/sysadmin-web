import psycopg2
from server import settings


class Postgres(object):
    def __init__(self):
        self.conn = None
        self.constr = "host=%s dbname=%s user=%s password=%s" % (settings.PSQL_HOST
                                                                ,settings.PSQL_NAME
                                                                ,settings.PSQL_USER
                                                                ,settings.PSQL_PASS)

    def connect(self, constr=None):
        if constr:
            self.conn = psycopg2.connect(constr)
        else:
            self.conn = psycopg2.connect(self.constr)

    def close(self):
        if self.conn:
            self.conn.close()

    def execute(self, query, params=None, format=False):
        # In case connection is not yet made
        if not self.conn:
            self.connect()

        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if "SELECT" in query:
            data = cursor.fetchall()
            return data
        else:
            self.conn.commit()
            return None
