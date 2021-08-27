import logging
import pandas as pd
import psycopg2

def query_postgres(host, port, user, password, dbname, query, execution_type='cursor'):
    conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname)
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
        
    if execution_type == 'cursor':
        cursor.close()
    conn.close()
