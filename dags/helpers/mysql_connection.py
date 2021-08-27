import logging
import pandas as pd

from mysql.connector import MySQLConnection, Error

def query_mysql(host, port, user, password, database, query, execution_type='cursor'):
    try:
        conn = MySQLConnection(host=host, port=port, user=user, password=password, database=database)
        if execution_type == 'cursor':
            cursor = conn.cursor()
            cursor.execute(query)

            logging.info('Query execution done with {} rows'.format(cursor.rowcount))

            rows = cursor.fetchall()
            
            for row in rows:
                logging.info(str(row))
                
        elif execution_type == 'pandas':
            result_df = pd.read_sql(sql=query, con=conn)
            logging.info(str(result_df))


    except Error as e:
        print(e)
    
    finally:
        if execution_type == 'cursor':
            cursor.close()
        conn.close()
