import logging

from mysql.connector import MySQLConnection, Error

def query_mysql(host, port, user, password, database, query):
    try:
        conn = MySQLConnection(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()
        cursor.execute(query)

        logging.info('Query execution done with {} rows'.format(cursor.rowcount))

        rows = cursor.fetchall()
        
        for row in rows:
            logging.info(str(row))

    except Error as e:
        print(e)
    
    finally:
        cursor.close()
        conn.close()
