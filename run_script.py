import psycopg2
import pandas as pd


def run_query(query):
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        port="5432"
    )

    # connect to the database
    cur = conn.cursor()

    #execute the query
    cur.execute(query)

    # fetch the rows
    rows = cur.fetchall()

    # extract the column names
    cols = [desc[0] for desc in cur.description]  

    # close the cursor and the connection
    cur.close()
    conn.close()

    # return a pandas dataframe of the data
    return pd.DataFrame(rows, columns=cols)  


