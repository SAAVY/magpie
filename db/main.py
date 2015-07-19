import base64
import datetime
from sqlalchemy import create_engine, Table, MetaData, Column, String, DateTime, exc
from sqlalchemy.sql import select


class MagpieDbError(Exception):
    def __init__(self, err):
        print "MAGPIE DB ERROR!: %s" % err
        self.err = err


class MagpieData(object):
    def __init__(self, url, metadata=None):
        self.url = url
        if(metadata is not None):
            self.rowcount = 1
            self.metadata = str(metadata._row[0])
        else:
            self.rowcount = 0
            self.metadata = metadata


class DbUtils(object):
    def _establish_db_connection(self):
        # Establish connection
        connectionString = 'postgres://' + base64.b64decode(self._username) + ':' + base64.b64decode(self._password) + '@' + base64.b64decode(self._hostName) + '/' + self._dbName
        engine = create_engine(connectionString)
        self._connection = engine.connect()

    def __init__(self):
        credentials = []
        # Open credentials file. Should be stored as "username:password"
        filename = 'credentials.txt'
        try:
            with open(filename) as f:
                for line in f:
                    line = line.split("\n", 1)[0]
                    credentials.append(line.split(':', 1))
        except EnvironmentError, err:
            raise MagpieDbError(err)

        self._username = base64.b64encode(credentials[0][0])
        self._password = base64.b64encode(credentials[0][1])
        self._dbName = credentials[1][1]
        self._tableName = credentials[2][1]
        self._hostName = base64.b64encode(credentials[3][1])
        try:
            self._establish_db_connection()
        except exc.SQLAlchemyError, err:
            raise MagpieDbError(err)

        # Columns of table
        self._columns = ['url', 'metadata', 'created_date']

        # Create Table Object
        self._mydata = Table(self._tableName, MetaData(),
                             Column(self._columns[0], String, primary_key=True),
                             Column(self._columns[1], String),
                             Column(self._columns[2], DateTime, default=datetime.datetime.utcnow))

    def __del__(self):
        # Close connection if established
        if 'self._connection' in locals():
            self._connection.close()

    def add_value(self, request_url, my_metadata):
        # Check if URL already exists
        s = select([self._mydata.c.metadata]).where(self._mydata.c.url == request_url)
        result = self._connection.execute(s)

        # Do nothing if it exists
        if(result.rowcount == 1):
            return

        # Insert URL and Metadata into Table
        ins = self._mydata.insert().values(url=request_url, metadata=my_metadata)
        try:
            self._connection.execute(ins)
        except exc.SQLAlchemyError, err:
            raise MagpieDbError(err)

    def get_metadata(self, request_url):
        s = select([self._mydata.c.metadata]).where(self._mydata.c.url == request_url)
        try:
            result = self._connection.execute(s)
        except exc.SQLAlchemyError, err:
            raise MagpieDbError(err)
        return MagpieData(request_url, result.first())

if __name__ == "__main__":
        db = DbUtils()
