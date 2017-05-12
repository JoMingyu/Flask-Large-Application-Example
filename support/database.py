import pymysql
from pymysql import IntegrityError


class Database:
    host = 'localhost'
    user = 'root'
    password = ''
    db = ''
    charset = 'utf8'

    _instance = None

    def __init__(self):
        self.connection = None

    def execute(self, *args):
        self.connection = pymysql.connect(host=self.host,
                                          user=self.user,
                                          password=self.password,
                                          db=self.db,
                                          charset=self.charset)
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        query = ''
        for arg in args:
            query += arg

        try:
            if 'SELECT' in query or 'select' in query:
                cursor.execute(query)
                result = cursor.fetchall()
            else:
                cursor.execute(query)
                result = self.connection.commit()

            cursor.close()
            self.connection.close()

            return result
        except IntegrityError as e:
            print(e)
