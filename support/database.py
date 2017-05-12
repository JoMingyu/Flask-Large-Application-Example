import pymysql
from pymysql import IntegrityError


host = 'localhost'
user = 'root'
password = ''
db = ''
charset = 'utf8'


def execute(*args):
    connection = pymysql.connect(host=host,
                                 user=user,
                                 password=password,
                                 db=db,
                                 charset=charset)
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = ''
    for arg in args:
        query += arg

    try:
        if 'SELECT' in query or 'select' in query:
            cursor.execute(query)
            result = cursor.fetchall()
        else:
            cursor.execute(query)
            result = connection.commit()

        cursor.close()
        connection.close()

        return result
    except IntegrityError as e:
        print(e)
